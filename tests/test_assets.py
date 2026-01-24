from models import Asset, Log
from utils import login_as_admin, login_as_user


def test_assets_page_loads(client, seed_assets):
    login_as_admin(client)
    response = client.get("/assets", follow_redirects=True)

    assert response.status_code == 200
    assert b"Create New Asset" in response.data


def test_asset_edit(client, seed_assets):
    login_as_admin(client)

    response = client.post(
        "/asset/edit/2",
        data={
            "name": "iphone 14 pro max test",
            "description": "test",
            "type": "Phone",
            "serial_number": "SN32346CA1111dddeee0909lkop",
            "in_use": "1",
            "department_id": "1",
            "assigned_user_id": "2",
            "approved": "0",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Asset updated" in response.data

    log = Log.query.filter(
        Log.action.contains("iphone 14 pro max test")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "updated" in log.action
    assert "iphone 14 pro max test" in log.action


def test_asset_delete(client, seed_assets):
    login_as_admin(client)

    response = client.post("/asset/delete/2", follow_redirects=True)

    assert response.status_code == 200
    assert b"Asset deleted" in response.data

    log = Log.query.filter(
        Log.action.contains("deleted")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "deleted" in log.action
    assert "2" in log.action or "Asset" in log.action


def test_create_asset(client, seed_assets):
    login_as_admin(client)

    response = client.post(
        "/asset/create",
        data={
            "name": "iphone 14 pro max test test",
            "description": "test",
            "type": "Phone",
            "serial_number": "SN32346CA1111dddeeeefffff2pl432dj1",
            "in_use": "1",
            "department_id": "1",
            "assigned_user_id": "2",
            "approved": "0",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Asset created and awaiting approval" in response.data

    log = Log.query.filter(
        Log.action.contains("iphone 14 pro max test test")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "Asset" in log.action
    assert "created" in log.action
    assert "iphone 14 pro max test test" in log.action


def test_create_asset_requires_login(client, seed_assets):
    response = client.post(
        "/asset/create",
        data={
            "name": "unauth asset",
            "description": "test",
            "type": "Phone",
            "serial_number": "SN000000TEST",
            "in_use": "1",
            "department_id": "1",
            "assigned_user_id": "2",
            "approved": "0",
        },
        follow_redirects=True,
    )

    assert b"Login" in response.data or response.status_code == 403


def test_asset_user_cannot_approve(client, seed_assets):
    login_as_user(client)

    response = client.post("/asset/approve/3", follow_redirects=True)

    assert b"Unauthorised Access" in response.data
    log = Log.query.filter(
        Log.action.contains("Asset (ID: 3) tried to be approved")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "tried to be approved" in log.action


def test_asset_approve(client, seed_assets):
    login_as_admin(client)

    unapproved_asset = Asset.query.filter_by(approved=False).first()
    assert unapproved_asset is not None

    response = client.post(
        f"/asset/approve/{unapproved_asset.id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Asset approved" in response.data

    asset_id = unapproved_asset.id
    asset_name = unapproved_asset.name
    log = Log.query.filter(
        Log.action.contains(
            f"Asset (ID: {asset_id}, Name: {asset_name}) approved by"
        )
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert (
        f"Asset (ID: {asset_id}, Name: {asset_name}) approved by"
        in log.action
    )

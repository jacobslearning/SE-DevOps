import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash

from database import db
from models import User, Department, Asset
from utils import login_as_admin, login_as_user

@pytest.fixture(autouse=True)
def seed_assets(client):
    password_hash = generate_password_hash("password")

    admin = User(username="admin", password_hash=password_hash, role="Admin")
    user = User(username="user", password_hash=password_hash, role="User")

    it = Department(name="IT")
    cs = Department(name="Customer Service")

    db.session.add_all([admin, user, it, cs])
    db.session.commit()

    assets = [
        Asset(
            name="Lenovo XP5 15",
            description="Work laptop",
            type="Laptop",
            serial_number="SN12345AL32323jjjj",
            date_created=datetime.utcnow(),
            in_use=True,
            approved=True,
            owner_id=user.id,
            department_id=it.id,
        ),
        Asset(
            name="Iphone 15 Pro Max",
            description="Company phone",
            type="Phone",
            serial_number="SN12346AL31ddddeaaac",
            date_created=datetime.utcnow(),
            in_use=True,
            approved=True,
            owner_id=user.id,
            department_id=it.id,
        ),
        Asset(
            name="Windows 10 PC",
            description="Office desktop",
            type="Desktop",
            serial_number="SN22345BO38791389173",
            date_created=datetime.utcnow(),
            in_use=True,
            approved=False,
            owner_id=user.id,
            department_id=cs.id,
        ),
    ]

    db.session.add_all(assets)
    db.session.commit()

    yield

    db.session.rollback()

def test_assets_page_loads(client):
    login_as_admin(client)
    response = client.get("/assets", follow_redirects=True)

    assert response.status_code == 200
    assert b"Create New Asset" in response.data

def test_asset_edit(client):
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

def test_asset_delete(client):
    login_as_admin(client)

    response = client.post("/asset/delete/2", follow_redirects=True)

    assert response.status_code == 200
    assert b"Asset deleted" in response.data

def test_create_asset(client):
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

def test_create_asset_requires_login(client):
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

def test_asset_user_cannot_approve(client):
    login_as_user(client)

    response = client.post("/asset/approve/3", follow_redirects=True)

    assert b"Unauthorised Access" in response.data

def test_asset_approve(client):
    login_as_admin(client)

    response = client.post("/asset/approve/3", follow_redirects=True)

    assert response.status_code == 200
    assert b"Asset approved" in response.data
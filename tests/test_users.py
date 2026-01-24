from utils import login_as_admin
from models import Log


def test_users_page_loads(client, seed_users):
    login_as_admin(client)
    response = client.get("/users", follow_redirects=True)
    assert response.status_code == 200
    assert b"Create New User" in response.data

    log = Log.query.filter(
        Log.action.contains("Users viewed")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "Users viewed" in log.action


def test_admin_approval(client, seed_users):
    login_as_admin(client)
    response = client.post("/user/promote/2", follow_redirects=True)
    assert response.status_code == 200

    log = Log.query.filter(
        Log.action.contains("promoted to Admin by")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "promoted to Admin by" in log.action


def test_user_edit(client, seed_users):
    login_as_admin(client)
    response = client.post("/user/edit/2", data={
        "username": "user",
        "password": "[HIDDEN]",
        "role": "Admin"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"User user updated" in response.data

    log = Log.query.filter(
        Log.action.contains("updated by")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "updated by" in log.action


def test_user_delete(client, seed_users):
    login_as_admin(client)
    response = client.post("/user/delete/2", follow_redirects=True)
    assert response.status_code == 200
    assert b"User deleted" in response.data

    log = Log.query.filter(
        Log.action.contains("deleted by")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "deleted by" in log.action


def test_create_user(client, seed_users):
    login_as_admin(client)
    response = client.post("/user/create", data={
        "username": "new_user",
        "password": "password",
        "role": "User"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"new_user" in response.data

    log = Log.query.filter(
        Log.action.contains("created by")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "created by" in log.action


def test_create_user_requires_login(client, seed_users):
    response = client.post("/user/create", data={
        "username": "unknown_user",
        "password": "password",
        "role": "User"
    }, follow_redirects=True)
    assert b"Login" in response.data or response.status_code == 403


def test_edit_user_form_access(client, seed_users):
    login_as_admin(client)
    response = client.get("/users")
    assert b"Edit" in response.data

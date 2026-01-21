import pytest
from werkzeug.security import generate_password_hash
from utils import login_as_admin
from models import User, db

@pytest.fixture(autouse=True)
def seed_users(client):
    password_hash = generate_password_hash("password")

    admin = User(username="admin", password_hash=password_hash, role="Admin")
    user = User(username="user", password_hash=password_hash, role="User")

    db.session.add_all([admin, user])
    db.session.commit()

    yield

    db.session.rollback()

def test_users_page_loads(client):
    login_as_admin(client)
    response = client.get("/users", follow_redirects=True)
    assert response.status_code == 200
    assert b"Create New User" in response.data

def test_admin_approval(client):
    login_as_admin(client)
    response = client.post("/user/promote/2", follow_redirects=True)
    assert response.status_code == 200

def test_user_edit(client):
    login_as_admin(client)
    response = client.post("/user/edit/2", data={
        "username": "user",
        "password": "[HIDDEN]",
        "role": "Admin"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"User user updated" in response.data

def test_user_delete(client):
    login_as_admin(client)
    response = client.post("/user/delete/2", follow_redirects=True)
    assert response.status_code == 200
    assert b"User deleted" in response.data

def test_create_user(client):
    login_as_admin(client)
    response = client.post("/user/create", data={
        "username": "new_user",
        "password": "password",
        "role": "User"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"new_user" in response.data

def test_create_user_requires_login(client):
    response = client.post("/user/create", data={
        "username": "unknown_user",
        "password": "password",
        "role": "User"
    }, follow_redirects=True)
    assert b"Login" in response.data or response.status_code == 403

def test_edit_user_form_access(client):
    login_as_admin(client)
    response = client.get("/users")
    assert b"Edit" in response.data
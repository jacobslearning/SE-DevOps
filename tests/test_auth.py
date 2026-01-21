import pytest
from werkzeug.security import generate_password_hash
from utils import login_as_user
from models import User, db

@pytest.fixture(autouse=True)
def seed_auth(client):
    password_hash = generate_password_hash("password")

    admin = User(username="admin", password_hash=password_hash, role="Admin")
    user = User(username="user", password_hash=password_hash, role="User")

    db.session.add_all([admin, user])
    db.session.commit()

    yield 

    db.session.rollback()

def test_login_page_loads(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Register" in response.data

def test_register_user(client):
    response = client.post(
        "/register",
        data={"username": "test_user", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Registration successful. Please log in" in response.data

def test_register_user_no_details(client):
    response = client.post("/register", follow_redirects=True)
    assert response.status_code == 200
    assert b"Username and password are required." in response.data

def test_register_username_taken(client):
    response = client.post(
        "/register",
        data={"username": "user", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Username is already taken." in response.data

def test_login_incorrect_username(client):
    response = client.post(
        "/login",
        data={"username": "no_user", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Incorrect username." in response.data

def test_login_incorrect_password(client):
    response = client.post(
        "/login",
        data={"username": "user", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Incorrect password." in response.data

def test_login(client):
    response = client.post(
        "/login",
        data={"username": "user", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome, user!" in response.data

def test_logout(client):
    login_as_user(client)
    response = client.post("/logout", data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out." in response.data
    assert b"Login" in response.data
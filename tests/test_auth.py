from utils import login_as_user
from models import Log


def test_login_page_loads(client, seed_auth):
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Register" in response.data


def test_register_user(client, seed_auth):
    response = client.post(
        "/register",
        data={"username": "test_user", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Registration successful. Please log in" in response.data

    log = (
        Log.query.filter(Log.action.contains("Registered account"))
        .order_by(Log.timestamp.desc())
        .first()
    )
    assert log is not None
    assert "Registered account" in log.action


def test_register_user_no_details(client, seed_auth):
    response = client.post("/register", follow_redirects=True)
    assert response.status_code == 200
    assert b"Username and password are required." in response.data


def test_register_username_taken(client, seed_auth):
    response = client.post(
        "/register",
        data={"username": "user", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Username is already taken." in response.data


def test_login_incorrect_username(client, seed_auth):
    response = client.post(
        "/login",
        data={"username": "no_user", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Incorrect username." in response.data


def test_login_incorrect_password(client, seed_auth):
    response = client.post(
        "/login",
        data={"username": "user", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Incorrect password." in response.data


def test_login(client, seed_auth):
    response = client.post(
        "/login",
        data={"username": "user", "password": "password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Welcome, user!" in response.data

    log = (
        Log.query.filter(Log.action.contains("Logged in"))
        .order_by(Log.timestamp.desc())
        .first()
    )
    assert log is not None
    assert "Logged in" in log.action


def test_logout(client, seed_auth):
    login_as_user(client)
    response = client.post("/logout", data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out." in response.data
    assert b"Login" in response.data

    log = (
        Log.query.filter(Log.action.contains("Logged out"))
        .order_by(Log.timestamp.desc())
        .first()
    )
    assert log is not None
    assert "Logged out" in log.action

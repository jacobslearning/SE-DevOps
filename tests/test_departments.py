import pytest
from werkzeug.security import generate_password_hash
from utils import login_as_admin, login_as_user
from models import User, Department, Log, db
from app import app


@pytest.fixture(autouse=True)
def seed_departments(client):
    with app.app_context():
        db.drop_all()
        db.create_all()
        password_hash = generate_password_hash("password")

        admin = User(
            username="admin",
            password_hash=password_hash,
            role="Admin"
        )
        user = User(
            username="user",
            password_hash=password_hash,
            role="User"
        )

        hr = Department(name="HR")
        cs = Department(name="Customer Service")
        it = Department(name="IT")
        store_ops = Department(name="Store Operations")
        security = Department(name="Security")
        marketing = Department(name="Marketing")

        db.session.add_all(
            [admin, user, hr, cs, it, store_ops, security, marketing]
        )
        db.session.commit()


def test_departments_page_loads(client):
    login_as_admin(client)
    response = client.get("/departments", follow_redirects=True)
    assert response.status_code == 200
    assert b"Add Department" in response.data

    log = Log.query.filter(
        Log.action.contains("Departments viewed")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "Departments viewed" in log.action


def test_department_edit(client):
    login_as_admin(client)
    response = client.post("/department/edit/2", data={
        "name": "new department",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Department new department updated" in response.data

    log = Log.query.filter(
        Log.action.contains("Department (ID: 2) updated")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "updated" in log.action


def test_department_delete(client):
    login_as_admin(client)
    response = client.post("/department/delete/2", follow_redirects=True)
    assert response.status_code == 200
    assert b"Department deleted" in response.data

    log = Log.query.filter(
        Log.action.contains("deleted by")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "deleted" in log.action


def test_create_department(client):
    login_as_admin(client)
    response = client.post("/department/create", data={
        "name": "new department",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"new department" in response.data

    log = Log.query.filter(
        Log.action.contains("Department new department created")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "created" in log.action


def test_create_department_requires_login(client):
    response = client.post("/department/create", data={
        "name": "department name",
    }, follow_redirects=True)
    assert b"Login" in response.data or response.status_code == 403


def test_department_user_can_not_add(client):
    login_as_user(client)
    response = client.get("/departments", follow_redirects=True)
    assert response.status_code == 200
    assert b"Add Department" not in response.data

    response = client.post(
        "/department/create", data={"name": "test"},
        follow_redirects=True
    )
    log = Log.query.filter(
        Log.action.contains("Unauthorised department creation attempt")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "Unauthorised department creation attempt" in log.action

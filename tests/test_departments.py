import pytest
from werkzeug.security import generate_password_hash
from utils import login_as_admin, login_as_user
from models import User, Department, db

@pytest.fixture(autouse=True)
def seed_departments(client):
    password_hash = generate_password_hash("password")

    admin = User(username="admin", password_hash=password_hash, role="Admin")
    user = User(username="user", password_hash=password_hash, role="User")

    hr = Department(name="HR")
    cs = Department(name="Customer Service")
    it = Department(name="IT")
    store_ops = Department(name="Store Operations")
    security = Department(name="Security")
    marketing = Department(name="Marketing")

    db.session.add_all([admin, user, hr, cs, it, store_ops, security, marketing])
    db.session.commit()

    yield

    db.session.rollback()

def test_departments_page_loads(client):
    login_as_admin(client)
    response = client.get("/departments", follow_redirects=True)
    assert response.status_code == 200
    assert b"Add Department" in response.data

def test_department_edit(client):
    login_as_admin(client)
    response = client.post("/department/edit/2", data={
        "name": "new department",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Department new department updated" in response.data

def test_department_delete(client):
    login_as_admin(client)
    response = client.post("/department/delete/2", follow_redirects=True)
    assert response.status_code == 200
    assert b"Department deleted" in response.data

def test_create_department(client):
    login_as_admin(client)
    response = client.post("/department/create", data={
        "name": "new department",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"new department" in response.data

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
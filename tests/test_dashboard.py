import pytest
from werkzeug.security import generate_password_hash
from utils import login_as_admin, login_as_user
from models import User, Department, Asset, db
from datetime import datetime
from app import app


@pytest.fixture(autouse=True)
def seed_dashboard():
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

        it = Department(name="IT")
        cs = Department(name="Customer Service")

        db.session.add_all([admin, user, it, cs])
        db.session.commit()

        assets = [
            Asset(
                name="Lenova XP5 15",
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


def test_dashboard_page_loads(client):
    login_as_admin(client)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"All Pending Assets" in response.data
    assert b"Welcome, admin!" in response.data


def test_metrics_load(client):
    login_as_admin(client)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Total Assets" in response.data
    assert b"Pending Approvals" in response.data
    assert b"Total Users" in response.data
    assert b"Departments" in response.data
    assert b"3" in response.data
    assert b"1" in response.data
    assert b"2" in response.data
    assert b"6" in response.data


def test_role_loads_as_admin(client):
    login_as_admin(client)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Role: Admin" in response.data


def test_role_loads_as_user(client):
    login_as_user(client)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Role: User" in response.data

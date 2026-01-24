import pytest
from werkzeug.security import generate_password_hash
from utils import login_as_admin, login_as_user
from models import User, Log
from datetime import datetime
from database import db


@pytest.fixture(autouse=True)
def seed_logs(app):
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

        db.session.add_all([admin, user])
        db.session.commit()

        logs = [
            Log(
                user_id=admin.id,
                action=f"Logged in as {admin.username} (ID:{admin.id})",
                timestamp=datetime.utcnow(),
            ),
            Log(
                user_id=user.id,
                action=f"Logged in as {user.username} (ID:{user.id})",
                timestamp=datetime.utcnow(),
            ),
        ]

        db.session.add_all(logs)
        db.session.commit()


def test_logs_page_loads_admin(client):
    login_as_admin(client)
    response = client.get("/logs", follow_redirects=True)
    assert response.status_code == 200
    assert b"Activity Logs" in response.data
    assert b"Logged in as admin (ID:1)" in response.data


def test_logs_page_loads_user(client):
    login_as_user(client)
    response = client.get("/logs", follow_redirects=True)
    assert response.status_code == 200
    assert b"dashboard" in response.data

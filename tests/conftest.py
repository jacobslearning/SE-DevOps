import pytest
from database import db
from app import create_app
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from models import User, Department, Asset, Log


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def seed_assets(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

        password_hash = generate_password_hash("password")
        admin = User(
            username="admin", password_hash=password_hash, role="Admin"
        )
        user = User(
            username="user", password_hash=password_hash, role="User"
        )
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
                date_created=datetime.now(timezone.utc),
                in_use=True,
                approved=True,
                owner_id=user.id,
                department_id=it.id
            ),
            Asset(
                name="Iphone 15 Pro Max",
                description="Company phone",
                type="Phone",
                serial_number="SN12346AL31ddddeaaac",
                date_created=datetime.now(timezone.utc),
                in_use=True,
                approved=True,
                owner_id=user.id,
                department_id=it.id
            ),
            Asset(
                name="Windows 10 PC",
                description="Office desktop",
                type="Desktop",
                serial_number="SN22345BO38791389173",
                date_created=datetime.now(timezone.utc),
                in_use=True,
                approved=False,
                owner_id=user.id,
                department_id=cs.id
            ),
        ]
        db.session.add_all(assets)
        db.session.commit()

        yield
        db.session.remove()


@pytest.fixture(scope="module")
def seed_auth(app):
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

        yield
        db.session.remove()


@pytest.fixture(scope="module")
def seed_dashboard(app):
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
                date_created=datetime.now(timezone.utc),
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
                date_created=datetime.now(timezone.utc),
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
                date_created=datetime.now(timezone.utc),
                in_use=True,
                approved=False,
                owner_id=user.id,
                department_id=cs.id,
            ),
        ]
        db.session.add_all(assets)
        db.session.commit()

        yield
        db.session.remove()


@pytest.fixture(scope="module")
def seed_departments(app):
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

        db.session.add_all([
            admin, user, hr, cs, it, store_ops, security, marketing
        ])
        db.session.commit()

        yield
        db.session.remove()


@pytest.fixture(scope="module")
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
                timestamp=datetime.now(timezone.utc),
            ),
            Log(
                user_id=user.id,
                action=f"Logged in as {user.username} (ID:{user.id})",
                timestamp=datetime.now(timezone.utc),
            ),
        ]
        db.session.add_all(logs)
        db.session.commit()

        yield
        db.session.remove()


@pytest.fixture(scope="module")
def seed_users(app):
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

        yield
        db.session.remove()

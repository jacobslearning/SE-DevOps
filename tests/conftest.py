import pytest
from database import db
from app import create_app
from tests.utils import (
    TEST_DB_URL,
)


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = TEST_DB_URL
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(autouse=True)
def database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()

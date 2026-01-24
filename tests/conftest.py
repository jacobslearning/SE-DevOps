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
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

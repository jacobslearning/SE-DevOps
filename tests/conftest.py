import pytest
from database import db
from app import create_app
from tests.utils import (
    create_test_database,
    drop_test_database,
    TEST_DB_URL,
)


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = TEST_DB_URL
    WTF_CSRF_ENABLED = False


@pytest.fixture(scope="session", autouse=True)
def database():
    create_test_database()
    yield
    drop_test_database()


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

import pytest
from app import app, db
from tests.utils import (
    create_test_database,
    drop_test_database,
    TEST_DB_URL,
)

@pytest.fixture(scope="session", autouse=True)
def database():
    create_test_database()
    yield
    drop_test_database()

@pytest.fixture
def client():
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=TEST_DB_URL,
    )

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
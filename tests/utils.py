import os
from psycopg2 import ProgrammingError
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()
ADMIN_DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URI"
)
TEST_DB_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URI"
).replace("itam", "tests")  # test


def create_test_database():
    engine = create_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        try:
            conn.execute(text('CREATE DATABASE "tests"'))
        except ProgrammingError:
            print("Database already exists, skipping")


def login_as_admin(client):
    client.post('/login', data={
        'username': 'admin',
        'password': 'password'
    }, follow_redirects=True)


def login_as_user(client):
    client.post('/login', data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)

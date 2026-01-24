from utils import login_as_admin, login_as_user


def test_logs_page_loads_admin(client, seed_logs):
    login_as_admin(client)
    response = client.get("/logs", follow_redirects=True)
    assert response.status_code == 200
    assert b"Activity Logs" in response.data
    assert b"Logged in as admin (ID:1)" in response.data


def test_logs_page_loads_user(client, seed_logs):
    login_as_user(client)
    response = client.get("/logs", follow_redirects=True)
    assert response.status_code == 200
    assert b"dashboard" in response.data

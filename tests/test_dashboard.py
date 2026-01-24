from utils import login_as_admin, login_as_user


def test_dashboard_page_loads(client, seed_dashboard):
    login_as_admin(client)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"All Pending Assets" in response.data
    assert b"Welcome, admin!" in response.data


def test_metrics_load(client, seed_dashboard):
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


def test_role_loads_as_admin(client, seed_dashboard):
    login_as_admin(client)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Role: Admin" in response.data


def test_role_loads_as_user(client, seed_dashboard):
    login_as_user(client)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Role: User" in response.data

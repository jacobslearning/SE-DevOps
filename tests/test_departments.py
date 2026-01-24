from utils import login_as_admin, login_as_user
from models import Log


def test_departments_page_loads(client, seed_departments):
    login_as_admin(client)
    response = client.get("/departments", follow_redirects=True)
    assert response.status_code == 200
    assert b"Add Department" in response.data

    log = Log.query.filter(
        Log.action.contains("Departments viewed")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "Departments viewed" in log.action


def test_department_edit(client, seed_departments):
    login_as_admin(client)
    response = client.post("/department/edit/2", data={
        "name": "new department",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Department new department updated" in response.data

    log = Log.query.filter(
        Log.action.contains("Department (ID: 2) updated")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "updated" in log.action


def test_department_delete(client, seed_departments):
    login_as_admin(client)
    response = client.post("/department/delete/2", follow_redirects=True)
    assert response.status_code == 200
    assert b"Department deleted" in response.data

    log = Log.query.filter(
        Log.action.contains("deleted by")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "deleted" in log.action


def test_create_department(client, seed_departments):
    login_as_admin(client)
    response = client.post("/department/create", data={
        "name": "new department",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"new department" in response.data

    log = Log.query.filter(
        Log.action.contains("Department new department created")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "created" in log.action


def test_create_department_requires_login(client, seed_departments):
    response = client.post("/department/create", data={
        "name": "department name",
    }, follow_redirects=True)
    assert b"Login" in response.data or response.status_code == 403


def test_department_user_can_not_add(client, seed_departments):
    login_as_user(client)
    response = client.get("/departments", follow_redirects=True)
    assert response.status_code == 200
    assert b"Add Department" not in response.data

    response = client.post(
        "/department/create", data={"name": "test"},
        follow_redirects=True
    )
    log = Log.query.filter(
        Log.action.contains("Unauthorised department creation attempt")
    ).order_by(Log.timestamp.desc()).first()
    assert log is not None
    assert "Unauthorised department creation attempt" in log.action

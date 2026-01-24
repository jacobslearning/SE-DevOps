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

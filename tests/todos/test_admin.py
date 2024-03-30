from .utils import *

def test_admin_not_admin(test_db, user_header):
    # Try to read all users
    response = client.get("/admin/users", headers=user_header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to read itself
    response = client.get("/admin/users/1", headers=user_header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to read other user
    response = client.get("/admin/users/2", headers=user_header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to read non-existing user
    response = client.get("/admin/users/3", headers=user_header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to read all todos
    response = client.get("/admin/todos", headers=user_header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Try to create a user
    response = client.post("/admin/users", headers=user_header, json={
        "username": "Foo",
        "email": "Bar",
        "first_name": "Baz",
        "last_name": "Qux",
        "password": "123qwe",
        "role": "user",
        "is_active": True
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_read_all_users_admin(test_db, admin_header):
    response = client.get("/admin/users", headers=admin_header)
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) == 2
    assert users[0].get('username') == 'Sven'
    assert users[1].get('username') == 'Arne'
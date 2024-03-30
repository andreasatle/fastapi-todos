from .utils import *

def test_user(test_db, user_header):
    response = client.get("/user", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    user = models.Users(**response.json())
    assert user.username == "Sven"
    assert user.email == "sven@svenson.com"
    assert user.first_name == "Sven"
    assert user.last_name == "Svenson"
    assert user.is_active == True
    assert user.role == "user"
    assert user.id == 1


def test_admin(test_db, admin_header):
    response = client.get("/user", headers=admin_header)
    assert response.status_code == status.HTTP_200_OK
    user = models.Users(**response.json())
    assert user.username == "Arne"
    assert user.email == "arne@arneson.com"
    assert user.first_name == "Arne"
    assert user.last_name == "Arneson"
    assert user.is_active == False
    assert user.role == "admin"
    assert user.id == 2

def test_user_timeout(test_db, user_header_timeout):
    response = client.get("/user", headers=user_header_timeout)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get('detail') == 'Invalid JWT-token: Signature has expired.'

def test_change_password(test_db, user_header):
    # Change password
    response = client.put("/user/change_password", headers=user_header, json={'old_password':'qwe123','new_password':'123qwe'})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Login with old password fails
    response = client.post('auth/token', data={'username': 'Sven', 'password': 'qwe123'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Login with new password succeeds
    response = client.post('auth/token', data={'username': 'Sven', 'password': '123qwe'})
    new_user_header = {"Authorization": f"Bearer {response.json().get('access_token')}"}
    assert response.status_code == status.HTTP_201_CREATED

    # Get user succeeds
    response = client.get("/user", headers=new_user_header)
    response.status_code == status.HTTP_200_OK
    assert response.json().get('email') == 'sven@svenson.com'


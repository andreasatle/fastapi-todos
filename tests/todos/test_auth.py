from .utils import *

def test_login_no_user(test_db):
    response = client.post("/auth/token", data={"username": "Svenne", "password": "123ewq"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Authentication failed"

def test_login_user(test_db):
    response = client.post("/auth/token", data={"username": "Sven", "password": "qwe123"})
    assert response.status_code == status.HTTP_201_CREATED
    token = response.json()
    cred = auth.jwt_token.decode(token.get("access_token"))
    assert cred.get("sub") == "Sven"
    assert cred.get("id") == 1

def test_login_admin(test_db):
    response = client.post("/auth/token", data={"username": "Arne", "password": "123ewq"})
    assert response.status_code == status.HTTP_201_CREATED
    token = response.json()
    cred = auth.jwt_token.decode(token.get("access_token"))
    assert cred.get("sub") == "Arne"
    assert cred.get("id") == 2


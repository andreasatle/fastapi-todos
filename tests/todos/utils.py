import pytest

# To read database info from env
import os
from dotenv import load_dotenv
from datetime import timedelta

# To create a test database
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# FastAPI related stuff
from fastapi import status, HTTPException
from fastapi.testclient import TestClient

# Importing modules from the todos app
import todos.database as database
import todos.main as main
import todos.models as models
import todos.requests as requests
import todos.routes.auth as auth

# Load the environment variables for the test db
load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# Setting up the tesing database
engine = create_engine(TEST_DATABASE_URL, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database.Base.metadata.create_all(bind=engine)

def override_get_db():
    with TestingSessionLocal() as db:
        yield db
main.app.dependency_overrides[database.get_db] = override_get_db


# def override_get_current_user():
#     return models.Users(
#         id=2,
#         username="Svenne",
#         email="a@b.com",
#         first_name="Sven",
#         last_name="Ekberg",
#         hashed_password="qwe123",
#         is_active=True,
#         role="user")
# main.app.dependency_overrides[get_current_user] = override_get_current_user


def create_entries():
    user_request1 = requests.UserRequest(
        username = "Sven",
        email = "sven@svenson.com",
        first_name = "Sven",
        last_name = "Svenson",
        phone_number = "123-456-7890",
        password = "qwe123",
        is_active = True,
        role = "user"
    )
    user_request2 = requests.UserRequest(
        username = "Arne",
        email = "arne@arneson.com",
        first_name = "Arne",
        last_name = "Arneson",
        phone_number = "321-654-9876",
        password = "123ewq",
        is_active = False,
        role = "admin"
    )

    user1 = models.Users(**user_request1.model_dump(),id=1)
    user2 = models.Users(**user_request2.model_dump(),id=2)

    todo1 = models.Todos(**requests.TodoRequest(
        title = "Todo1",
        description = "This is a test todo 1",
        priority = 1,
        completed = False
    ).model_dump(), id=1, owner_id=1)

    todo2 = models.Todos(**requests.TodoRequest(
        title = "Todo2",
        description = "This is a test todo 2",
        priority = 2,
        completed = True,
    ).model_dump(), id=2, owner_id=2)

    todo3 = models.Todos(**requests.TodoRequest(
        title = "Todo3",
        description = "This is a test todo 3",
        priority = 3,
        completed = False,
    ).model_dump(), id=3, owner_id=1)

    todo4 = models.Todos(**requests.TodoRequest(
        title = "Todo4",
        description = "This is a test todo 4",
        priority = 4,
        completed = True,
    ).model_dump(), id=4, owner_id=2)

    with TestingSessionLocal() as db:
        db.add(user1)
        db.add(user2)
        db.add(todo1)
        db.add(todo2)
        db.add(todo3)
        db.add(todo4)
        db.commit()


def clear_tables():
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM todos;'))
        conn.execute(text('DELETE FROM users;'))
        conn.commit()


@pytest.fixture
def test_db():
    create_entries()
    yield
    clear_tables()

def override_get_current_no_user():
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials")

client = TestClient(main.app)

@pytest.fixture
def user_header():
    response = client.post('auth/token', data={'username': 'Sven', 'password': 'qwe123'})
    return {"Authorization": f"Bearer {response.json().get('access_token')}"}

@pytest.fixture
def admin_header():
    response = client.post('auth/token', data={'username': 'Arne', 'password': '123ewq'})
    return {"Authorization": f"Bearer {response.json().get('access_token')}"}

@pytest.fixture
def user_header_timeout():
    old_duration = auth.jwt_token.duration
    auth.jwt_token.duration = timedelta(seconds=-1)
    response = client.post('auth/token', data={'username': 'Sven', 'password': 'qwe123'})
    yield {"Authorization": f"Bearer {response.json().get('access_token')}"}
    auth.jwt_token.duration = old_duration

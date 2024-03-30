from pydantic import BaseModel, Field, field_validator, AfterValidator
from typing import Annotated
from passlib.context import CryptContext

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    return bcrypt.hash(password)

HashType = Annotated[str, Field(min_length=3, max_length=64), AfterValidator(hash)]
PasswordType = Annotated[HashType, Field(alias="password")]
OldPasswordType = Annotated[HashType, Field(alias="old_password")]
NewPasswordType = Annotated[HashType, Field(alias="new_password")]

class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    hashed_password: PasswordType
    is_active: bool = True
    role: str

    model_config = {
        "json_schema_extra":  {
            "example": {
                "username": "codingwithatle",
                "email": "codingwith@atle72.com",
                "first_name": "Andreas",
                "last_name": "Atle",
                "password": "password",
                "is_active": True,
                "role": "user"
            }
        }
    }

class PartialUserRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    hashed_password: PasswordType | None = None
    is_active: bool | None = None
    role: str | None = None

    model_config = {
        "json_schema_extra":  {
            "example": {
                "username": "codingwithatle",
                "email": "codingwith@atle72.com",
                "first_name": "Andreas",
                "last_name": "Atle",
                "password": "password",
                "is_active": True,
                "role": "user"
            }
        }
    }
class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int
    completed: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "This is my ToDo",
                "description": "This is my description of my ToDo",
                "priority": 4,
                "completed": False,
            }
        }
    }

class PartialTodoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = None
    completed: bool | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "This is my ToDo",
                "description": "This is my description of my ToDo",
                "priority": 4,
                "completed": False,
            }
        }
    }

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "old_password": "password",
                "new_password": "new_password",
            }
        }
    }
    

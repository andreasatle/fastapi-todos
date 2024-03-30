from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from dotenv import load_dotenv
import os
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import todos.database as db
import todos.models as models
import todos.requests as requests
import todos.jwt_tokens as jwt_tokens

router = APIRouter(prefix="/auth", tags=["auth"])
RequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
jwt_token = jwt_tokens.JWTToken()
Oauth2Dep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))]

def authenticate_user(username: str, password: str, db: db.SessionDep):
    # Read user from database
    user = db.query(models.Users).filter(models.Users.username == username).first()

    # Check if user doesn't exists or if the password is incorrect
    if not user or not requests.bcrypt.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    # When user exist and password is correct, return the user
    return user

async def get_current_user(token: Oauth2Dep, db: db.SessionDep):
    try:
        payload = jwt_token.decode(token)
        username = payload["sub"]
        exp = payload["exp"]
        user_id = payload["id"]
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid JWT-token: {e}")

    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    return user

async def get_current_admin_user(token: Oauth2Dep, db: db.SessionDep):
    user = await get_current_user(token, db)
    if user is not None and user.role != "admin":
        user = None
    return user

@router.post('/token', response_model=jwt_tokens.Token, status_code=status.HTTP_201_CREATED)
async def create_token(form: RequestFormDep, db: db.SessionDep):
    user = authenticate_user(form.username, form.password, db)
    return jwt_token.encode(user)
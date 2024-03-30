from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated
import todos.database as db
import todos.models as models
import todos.requests as requests
from todos.routes.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])
UserDep = Annotated[models.Users, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_user(user: UserDep, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    return user

@router.get("/", status_code=status.HTTP_200_OK)
async def read_user(user: UserDep, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    return user

@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def change_user(user: UserDep, change_user: requests.PartialUserRequest, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    user.update_with(change_user)
    db.commit()

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(user: UserDep, passwords: requests.ChangePasswordRequest, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    if not requests.bcrypt.verify(passwords.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password is incorrect")

    user.hashed_password = requests.hash(passwords.new_password)
    db.commit()
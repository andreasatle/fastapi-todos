from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated
import todos.database as db
import todos.models as models
import todos.requests as requests
from todos.routes.auth import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])
AdminDep = Annotated[models.Users, Depends(get_current_admin_user)]

@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(admin: AdminDep, db: db.SessionDep):
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin user not authenticated")

    return db.query(models.Users).all()

@router.get("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_user(user_id: int, admin: AdminDep, db: db.SessionDep):
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin user not authenticated")

    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User (id: {user_id}) not found")
    return user

@router.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(admin: AdminDep, user: models.requests.UserRequest, db: db.SessionDep):
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin user not authenticated")

    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, admin: AdminDep, db: db.SessionDep):
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin user not authenticated")

    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User (id: {user_id}) not found")
    db.delete(user)
    db.commit()

@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all_todos(admin: AdminDep, db: db.SessionDep):
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin user not authenticated")

    return db.query(models.Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, admin: AdminDep, db: db.SessionDep):
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin user not authenticated")

    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo (id: {todo_id}) not found")
    db.delete(todo)
    db.commit()


from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
import todos.database as db
import todos.models as models
import todos.requests as requests
from todos.routes.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])
UserDep = Annotated[models.Users, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(user: UserDep, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    return user.todos

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: requests.TodoRequest, user: UserDep, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    new_todo = models.Todos(**todo.model_dump(), owner_id=user.id)
    db.add(new_todo)
    db.commit()

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int, user: UserDep, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    todo = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .filter(models.Todos.owner_id == user.id) \
        .first()

    # If the todo is not found, raise an HTTPException
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo (id: {todo_id}) not found")

    # Update the todo with the new data
    return todo

@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo_id: int, user: UserDep, new_todo: requests.PartialTodoRequest, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    updated_todo = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .filter(models.Todos.owner_id == user.id) \
        .first()

    # If the todo is not found, raise an HTTPException
    if updated_todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo (id: {todo_id}) not found")

    # Update the todo with the new data
    updated_todo.update_with(new_todo)
    db.commit()

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, user: UserDep, db: db.SessionDep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

    todo = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .filter(models.Todos.owner_id == user.id) \
        .first()

    # If the todo is not found, raise an HTTPException
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo (id: {todo_id}) not found")

    db.delete(todo)
    db.commit()

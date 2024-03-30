from .utils import *

def test_user_read_todos(test_db, user_header): 
    response = client.get("/todos", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    todos = response.json()
    assert len(todos) == 2

    assert todos[0].get('id') == 1
    assert todos[0].get('title') == "Todo1"
    assert todos[0].get('description') == "This is a test todo 1"
    assert todos[0].get('priority') == 1
    assert todos[0].get('completed') == False
    assert todos[0].get('owner_id') == 1

    assert todos[1].get('id') == 3
    assert todos[1].get('title') == "Todo3"
    assert todos[1].get('description') == "This is a test todo 3"
    assert todos[1].get('priority') == 3
    assert todos[1].get('completed') == False
    assert todos[1].get('owner_id') == 1

def test_admin_read_todos(test_db, admin_header): 
    response = client.get("/todos", headers=admin_header)
    assert response.status_code == status.HTTP_200_OK
    todos = response.json()
    assert len(todos) == 2

    assert todos[0].get('id') == 2
    assert todos[0].get('title') == "Todo2"
    assert todos[0].get('description') == "This is a test todo 2"
    assert todos[0].get('priority') == 2
    assert todos[0].get('completed') == True
    assert todos[0].get('owner_id') == 2

    assert todos[1].get('id') == 4
    assert todos[1].get('title') == "Todo4"
    assert todos[1].get('description') == "This is a test todo 4"
    assert todos[1].get('priority') == 4
    assert todos[1].get('completed') == True
    assert todos[1].get('owner_id') == 2

def test_user_read_todo_by_invalid_id(test_db, user_header):
    response = client.get("/todos/5", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_user_create_todos(test_db, user_header):
    # Create a new todo
    response = client.post("/todos", headers=user_header, json={
        "title": "Todo5",
        "description": "This is a test todo 5",
        "priority": 5,
        "completed": False
    })

    # Check status code
    assert response.status_code == status.HTTP_201_CREATED

    # Read the todos for the user
    response = client.get("/todos", headers=user_header)
    todos = response.json()

    # Check that the new todo is in the list (avoid checking id)
    assert len(todos) == 3
    assert todos[2].get('title') == "Todo5"
    assert todos[2].get('description') == "This is a test todo 5"
    assert todos[2].get('priority') == 5
    assert todos[2].get('completed') == False
    assert todos[2].get('owner_id') == 1

def test_user_update_todos(test_db, user_header):
    # Update a todo with non-valid id
    response = client.put("/todos/2", headers=user_header, json={
        "title": "Todo5",
        "description": "This is a test todo 5",
        "priority": 5,
        "completed": False
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Update a todo with valid id
    response = client.put("/todos/1", headers=user_header, json={
        "title": "Todo5",
        "description": "This is a test todo 5",
        "priority": 5,
        "completed": False
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/todos/1", headers=user_header)
    assert response.status_code == status.HTTP_200_OK
    todo = response.json()
    
    assert todo.get('title') == "Todo5"
    assert todo.get('description') == "This is a test todo 5"
    assert todo.get('priority') == 5
    assert todo.get('completed') == False
    assert todo.get('owner_id') == 1

def test_user_delete_todos(test_db, user_header):
    # Delete a todo with non-valid id
    response = client.delete("/todos/2", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Check that the todo exists
    response = client.get("/todos/1", headers=user_header)
    assert response.status_code == status.HTTP_200_OK

    # Delete a todo with valid id
    response = client.delete("/todos/1", headers=user_header)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check that the todo is deleted
    response = client.get("/todos/1", headers=user_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
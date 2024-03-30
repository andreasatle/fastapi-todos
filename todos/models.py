from todos.database import Base
import todos.requests as requests
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    hashed_password = Column(String(64))
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default="user")

    todos = relationship("Todos", back_populates="owner")

    def __str__(self):
        return f"Users(id: {self.id}, username: '{self.username}', email: '{self.email}', first_name: '{self.first_name}', last_name: '{self.last_name}', is_active: {self.is_active}, role: '{self.role}')"

    def update_with(self, user: requests.UserRequest):
        self.username = user.username
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.hashed_password = user.hashed_password
        self.is_active = user.is_active
        self.role = user.role

    def update_with(self, user: requests.PartialUserRequest):
        if user.username:
            self.username = user.username
        if user.email:
            self.email = user.email
        if user.first_name:
            self.first_name = user.first_name
        if user.last_name:
            self.last_name = user.last_name
        if user.hashed_password:
            self.hashed_password = user.hashed_password
        if user.is_active:
            self.is_active = user.is_active
        if user.role:
            self.role = user.role

class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(50))
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")

    def update_with(self, todo: requests.TodoRequest):
        self.title = todo.title
        self.description = todo.description
        self.priority = todo.priority
        self.completed = todo.completed

    def update_with(self, todo: requests.PartialTodoRequest):
        if todo.title:
            self.title = todo.title
        if todo.description:
            self.description = todo.description
        if todo.priority:
            self.priority = todo.priority
        if todo.completed:
            self.completed = todo.completed

from fastapi import FastAPI, status
import todos.database as db
from todos.routes import admin, auth, user, todos

# Create db tables if not already exists
db.Base.metadata.create_all(bind=db.engine)

# Create a FastAPI instance
app = FastAPI()

# Add routes to the FastAPI instance
app.include_router(todos.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/healthy", status_code=status.HTTP_200_OK, tags=["health"])
def health_check():
    return {"status": "ok"}
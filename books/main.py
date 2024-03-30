from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
import database
import models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

IdType = Annotated[int, Field(description="The unique identifier of the book", ge=1)]
RatingType = Annotated[int, Field(description="The rating of the book", ge=1, le=5)]

class Book:
    id: IdType
    title: str
    author: str
    description: str
    rating: RatingType

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1)
    rating: RatingType

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI for Beginners",
                "author": "codingwithatle",
                "description": "Learn FastAPI in Python",
                "rating": 5
            }
        }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithruby', 'Learn computer science with Python', 5),
    Book(2, 'Fast with FastAPI', 'codingwithsven', 'Learn FastAPI in Python', 5),
    Book(3, 'Django for Beginners', 'codingwithsven', 'Learn Django in Python', 4),
    Book(4, 'Flask for Beginners', 'codingwitharne', 'Learn Flask in Python', 5),
    Book(5, 'Python for Beginners', 'codingwitharne', 'Learn Python programming', 3),
]

def next_unique_book_id():
    next_id = 0
    for book in BOOKS:
        if book.id > next_id:
            next_id = book.id
    return next_id + 1


@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get('/books/', status_code=status.HTTP_200_OK)
async def query_books_by_rating(rating: int):
    return [book for book in BOOKS if book.rating == rating]

@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id: IdType):

    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found")

@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    BOOKS.append(Book(**book_request.model_dump(),id=next_unique_book_id()))

@app.put('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: IdType, book_request: BookRequest):

    for idx in range(len(BOOKS)):
        if BOOKS[idx].id == book_id:
            BOOKS[idx] = Book(**book_request.model_dump(),id=book_id)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found")

@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: IdType):
    for idx in range(len(BOOKS)):
        if BOOKS[idx].id == book_id:
            BOOKS.pop(idx)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book {book_id} not found")

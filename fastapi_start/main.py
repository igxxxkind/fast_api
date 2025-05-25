from bookstore.books import router_books
from bookstore.authors import router_authors
from bookstore.models import Book

from pydantic import BaseModel
from fastapi import FastAPI

class BookResponse(BaseModel):
    title: str
    author: str


app = FastAPI()
app.include_router(router_books.router)
app.include_router(router_authors.router)

@app.post("/book")
async def create_book(book: Book):
    return book

@app.get("/allbooks")
async def read_all_books() -> list[BookResponse]:
    return [
        {"id": 1,
        "title": "1984",
        "author": "George Orwell"},
        {"id": 2, 
         "title": "The Great Gatsby",
         "author": "F. Scott Fitzgerald"}
    ]
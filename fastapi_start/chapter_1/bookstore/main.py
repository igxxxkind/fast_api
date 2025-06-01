import json

from bookstore.books import router_books
from bookstore.authors import router_authors
from bookstore.models import Book

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.responses import JSONResponse

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

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content = {"message": "Oops! Somthing went wrong!"},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(
        "This is a plain text response:" f" /n {json.dumps(exc.errors(), indent=2)}",
        status_code=status.HTTP_400_BAD_REQUEST,
    )

@app.get("/error_endpoint")
async def raise_exception():
    raise HTTPException(status_code=400)



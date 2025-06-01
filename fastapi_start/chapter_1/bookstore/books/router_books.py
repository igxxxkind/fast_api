from fastapi import APIRouter

router = APIRouter()

@router.get("/books/{book_id}")
async def read_book(book_id: int):
    return {"book_id": book_id,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald"
            }
    
@router.get("/books")
async def read_books(year: int=None):
    if year:
        return{
            "year": year,
            "books": ["Book 1", "Book 2"]
        }
    return {"books": ["All books"]}


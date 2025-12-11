from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query, Request, status
from db import get_db, engine, Base
from models import Book, UpdateBook, CreateBook, BookResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import uvicorn
import logging
from fastapi.responses import JSONResponse

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
    yield

app = FastAPI(lifespan = lifespan)

@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    """
        Handler for 500 Internal Server Error.
        Logs the traceback and returns a JSON response to the client.
        """
    logger.error(f"FATAL 500 ERROR: Request to {request.url} failed.", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."})

@app.get("/books")
def get_books(db: Session =  Depends(get_db)) -> list[BookResponse]:
    """
    Retrieves a list of all books from the database.

    Args:
        db: SQLAlchemy session dependency.

    Returns:
        A list of BookResponse objects.
    """
    return db.query(Book).all() #type: ignore

@app.post("/books")
def add_book(create_data: CreateBook, db: Session = Depends(get_db)) -> dict[str,str]:
    """
        Adds a new book record to the database.
        Args:
            create_data: Pydantic model containing book details (title, author, year).
            db: SQLAlchemy session dependency.
        Returns:
            Confirmation message.
        """
    book: Book = Book(**create_data.model_dump(exclude_none=True))
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"message": "New book created"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """
        Deletes a specific book by its ID.
        Args:
            book_id: The ID of the book to delete.
            db: SQLAlchemy session dependency.
        Raises:
            HTTPException: 404 Not Found if the book does not exist.
        Returns:
            Confirmation message.
        """
    book: Book | None = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(404, f"Book {book_id} is not found")
    db.delete(book)
    db.commit()
    return {"message": f"Book {book_id} deleted"}

@app.put("/books/{book_id}")
def update_books(book_id: int, update_data: UpdateBook, db: Session = Depends(get_db)) -> dict[str,str]:
    """
        Updates an existing book record by its ID.
        Args:
            book_id: The ID of the book to update.
            update_data: Pydantic model with fields to update (Optional).
            db: SQLAlchemy session dependency.
        Raises:
            HTTPException: 404 Not Found if the book does not exist.
        Returns:
            Confirmation message.
        """
    book: Book | None = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(404, f"Book {book_id} is not found")
    update_fields = update_data.model_dump(exclude_none = True)
    for key, value in update_fields.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return {"message": f"Book {book_id} updated"}

@app.get("/books/search")
def search_books(title: str | None = Query(None), author: str | None = Query(None),
    year: int | None = Query(None), db: Session = Depends(get_db)) -> list[BookResponse]:
    """
        Searches for books based on optional criteria.
        The search for title and author is case-insensitive and exact match.
        Args:
            title: Title to search for (case-insensitive, exact match).
            author: Author to search for (case-insensitive, exact match).
            year: Year of publication (exact match).
            db: SQLAlchemy session dependency.
        Returns:
            A list of BookResponse objects matching the criteria.
        """
    query = db.query(Book)
    if title:
        query = query.filter(title.strip().lower() == func.lower(Book.title))
    if author:
        query = query.filter(author.strip().lower() == func.lower(Book.author))
    if year:
        query = query.filter(Book.year == year)
    return query.all() #type: ignore



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
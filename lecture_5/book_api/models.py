from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
from typing import Optional
from db import Base
from pydantic import BaseModel

class Book(Base):
    """
        SQLAlchemy ORM model which represents the 'books' table in the database.
        Attributes:
            id: Primary key, automatically incremented integer.
            title: The title of the book (string, max 40 chars).
            author: The author of the book (string, max 40 chars).
            year: The year of publication (integer, nullable).
        """
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    title: Mapped[str] = mapped_column(String(40))
    author: Mapped[str] = mapped_column(String(40))
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable = True)

class UpdateBook(BaseModel):
    """
        Pydantic model for updating an existing book (HTTP PUT request).
        Attributes:
            title: New title of the book (optional string).
            author: New author of the book (optional string).
            year: New year of publication (optional integer).
        """
    title: str | None = None
    author: str | None = None
    year: int | None = None

class CreateBook(BaseModel):
    """
        Pydantic model for creating a new book (HTTP POST request).
        Attributes:
            title: The title of the book (required string).
            author: The author of the book (required string).
            year: The year of publication (optional integer).
        """
    title: str
    author: str
    year: int | None = None

class BookResponse(BaseModel):
    """
        Pydantic model used for API responses (HTTP GET, PUT, DELETE returns).  It converts SQLAlchemy objects to JSON.
        Attributes:
            id: The unique identifier of the book.
            title: The title of the book.
            author: The author of the book.
            year: The year of publication.
        """
    id: int
    title: str
    author: str
    year: Optional[int] = None
    class Config:
        from_attributes = True

    def __repr__(self) -> str:
        """
        Provides a readable representation of the Book object
        for debugging and logging.
        """
        return f"Book(id = {self.id}, title = '{self.title}', author = '{self.author}', year = '{self.year}')"



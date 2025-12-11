from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """
        Base class for all ORM models in the application.
        All model classes must inherit from this class.
        """
    pass

Database_url = "sqlite:///./books.db"
engine = create_engine(Database_url, connect_args={"check_same_thread": False}, echo = True)
local_session = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    """
        Dependency function for managing the database session lifecycle.
        This function is used by FastAPI's Depends() to provide a database session.
        It ensures the session is closed after the request is finished.
        """
    db = local_session()
    try:
        yield db
    finally:
        db.close()
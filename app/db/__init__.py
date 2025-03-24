import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=True, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db(logger_instance=logger):
    """
    Initialises the database by creating all tables based on the defined models.
    Importing app.models ensures that all models are registered with Base.metadata.

    :param logger_instance: Logger instance to use. Defaults to the module-level logger.
    """
    import app.models  # noqa: F401

    logger_instance.info("Initializing the database")
    Base.metadata.create_all(bind=engine)
    logger_instance.info("Database initialization complete.")


def get_db(logger_instance=logger):
    """
    Dependency injection function to yield a new database session.
    This function is typically used in FastAPI endpoint dependencies.

    :param logger_instance: Logger instance to use. Defaults to the module-level logger.
    :yield: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as exc:
        logger_instance.error("An error occurred during DB session: %s", exc)
        raise
    finally:
        db.close()
        logger_instance.info("Database session closed.")

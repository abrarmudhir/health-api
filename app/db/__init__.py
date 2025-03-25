import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the DATABASE_URL from the environment, defaulting to SQLite if not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


def get_app_db_url() -> str:
    """
    Returns the database URL to be used by the application.
    If the URL contains '@db:' (used for Docker internal networking),
    it replaces it with '@localhost:' so that the host machine can connect.
    """
    url = DATABASE_URL
    if "@db:" in url:
        logger.info("Replacing 'db' with 'localhost' for app connection")
        url = url.replace("@db:", "@localhost:")
    return url


adjusted_db_url = get_app_db_url()
connect_args = (
    {"check_same_thread": False} if adjusted_db_url.startswith("sqlite") else {}
)
engine = create_engine(
    adjusted_db_url, echo=True, future=True, connect_args=connect_args
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db(logger_instance=logger):
    """
    Initializes the database by creating all tables based on the defined models.
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

import logging
import os

from dotenv import load_dotenv

load_dotenv()


def configure_logger(name=__name__, level=logging.INFO):
    """Configure and return a logger with the specified name and level."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

    return logger


logger = configure_logger()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://healthuser:healthpass@db:5432/healthdb"
)

logger.info("DATABASE_URL loaded: %s", DATABASE_URL)

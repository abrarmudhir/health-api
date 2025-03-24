import logging


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

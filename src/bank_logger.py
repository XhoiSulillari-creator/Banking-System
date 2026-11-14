import logging


def get_bank_logger():
    logger = logging.getLogger("banking_system")

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(
            "data/banking.log"
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
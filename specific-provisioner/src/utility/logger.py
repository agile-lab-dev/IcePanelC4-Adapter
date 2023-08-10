import logging


def get_logger(name=""):
    default_log_args = {
        "level": logging.INFO,
        "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        "datefmt": "%d-%b-%y %H:%M",
        "force": True,
    }
    logging.basicConfig(**default_log_args)
    logger = logging.getLogger(name)
    return logger

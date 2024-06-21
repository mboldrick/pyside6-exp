import logging

logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("log_formatter.log")

logger.addHandler(file_handler)

formatter = logging.Formatter(("%(asctime)s - %(name)s - %(levelname)s - "
                              "%(message)s"))
file_handler.setFormatter(formatter)

logger.debug("This is a debug statement")
logger.info("This is info")

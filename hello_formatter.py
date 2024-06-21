import logging

logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("hello_formatter.log")

logger.addHandler(file_handler)

formatter = logging.Formatter()
file_handler.setFormatter(formatter)

logger.debug("This is a debug statement")
logger.info("This is info")

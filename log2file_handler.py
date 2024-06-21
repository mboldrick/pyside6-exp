import logging

logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("log2file_handler.log")

logger.addHandler(file_handler)

logger.debug("This is a debug statement")
logger.info("This is info")

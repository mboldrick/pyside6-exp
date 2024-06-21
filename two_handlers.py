import logging

logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("two_handlers.log")
stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.debug("This is a debug statement")
logger.info("This is info")

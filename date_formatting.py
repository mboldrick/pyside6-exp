import logging

logger = logging.getLogger("date_formatting")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("date_formatting.log")

logger.addHandler(file_handler)

fmt = ("%(asctime)s - %(filename)s - lineno: %(lineno)s"
       " - %(message)s")
datefmt = "%a %d %b %Y"

formatter = logging.Formatter(fmt, datefmt=datefmt)
file_handler.setFormatter(formatter)

logger.debug("This is a debug statement")
logger.info("This is info")

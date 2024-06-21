import logging

logger = logging.getLogger("formatting")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("more_log_formatter.log")

logger.addHandler(file_handler)

fmt = ("%(asctime)s - %(filename)s - lineno: %(lineno)s"
       " - %(message)s")
formatter = logging.Formatter(fmt)
file_handler.setFormatter(formatter)

logger.debug("This is a debug statement")
logger.info("This is info")

import logging

logging.basicConfig(filename="log_levels.log", level=logging.DEBUG)

logging.debug("Hello debug")
logging.info("This is info")
logging.warning("This is a warning")
logging.error("This is an error")
logging.critical("This is critical!!")

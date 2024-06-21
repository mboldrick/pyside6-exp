import logging

logging.basicConfig(filename="hello.log", level=logging.INFO)

logging.debug("Hello debug")
logging.info("This is info")
logging.warning("This is a warning")
logging.error("This is an error")
logging.critical("This is critical!!")

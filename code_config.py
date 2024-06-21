import logging
import time


def main():
    """
    The main entry point of the application
    """
    logger = logging.getLogger("example_app")
    logger.setLevel(logging.INFO)

    # Create the logging file handler
    file_handler = logging.FileHandler("code_config_example.log")
    fmt = ("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter(fmt=fmt)
    file_handler.setFormatter(formatter)

    # Create the stream handler
    stream_handler = logging.StreamHandler()
    fmt_stream = ("%(asctime)s - %(filename)s - %(lineno)d - "
                  "%(message)s")
    stream_formatter = logging.Formatter(fmt=fmt_stream)
    stream_handler.setFormatter(stream_formatter)

    # Add handlers to logger object
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info("Program started")

    # Pretend to do some processing
    time.sleep(2)

    logger.info("Done!")


if __name__ == '__main__':
    main()

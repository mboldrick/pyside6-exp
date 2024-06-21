import logging

logger = logging.getLogger("excepter")
logger.setLevel(logging.INFO)

def divide(a: object, b: object) -> object:
    try:
        result = a / b
    except ZeroDivisionError:
        logger.exception("A divide by zero error has occurred")
    except TypeError:
        logger.exception("A non-numeric value was used")
    else:
        return result


def divide2(a: object, b: object) -> object:
    return a / b


if __name__ == '__main__':
    divide(1, 0)

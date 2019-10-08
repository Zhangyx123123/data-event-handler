from functools import wraps
import logging


def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = str(e)
            logging.error("exception in {}.{}: {}".format(func.__class__, func.__name__, message))
            return {
                'status': 'fail',
                'message': 'Other Error: %s' % message
            }

    return wrapper

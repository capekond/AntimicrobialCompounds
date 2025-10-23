import db
import logging
from nicegui import ui


def has_records(func):
    def wrapper(*args, **kwargs):
        result = None
        x, res = db.get_all_records()
        if not res:
            logging.warning ("Access to empty database")
            ui.navigate.to("/welcome")
        else:
            result = func(*args, **kwargs)
        return result
    return wrapper


@has_records
def add(a, b):
    return a + b
print(add(5, 3))

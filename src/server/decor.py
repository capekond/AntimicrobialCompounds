import db
import logging
from nicegui import ui
import data_change
from config import *

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

def logged(func):
    def wrapper(*args, **kwargs):
        result = None
        logging.info(f"User access is turn {'on.' if LOGIN_ON else  'off.'}")
        role: str = data_change.get_login_role()
        if role or (not LOGIN_ON):
            result = func(*args, **kwargs)
        else:
            logging.warning("No login user")
            ui.navigate.to("/login")
        return result
    return wrapper

@has_records
def add(a, b):
    return a + b
print(add(5, 3))

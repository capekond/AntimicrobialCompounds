import csv
import logging
import numbers
from logging.handlers import RotatingFileHandler
from nicegui import app, ui
import db
from src.server.config import *

def is_number(s, ba: ui.button):
    try:
        float(s)
        ba.enable()
        return True
    except ValueError:
        ba.disable()
        return False

def add_status(selection, ab: ui.button, ad: ui.button):
    global selected_ids
    selected_ids = selection
    if len(selected_ids) > 0:
        ab.enable()
        ad.enable()
    else:
        ab.disable()
        ad.disable()
    logging.debug(f"In table data selected row(s): {selected_ids}")

def set_logs():
    log_formatter = logging.Formatter(LOG_FORMAT)
    my_handler = RotatingFileHandler('../../log/debug.log', mode='a', maxBytes=5*1024, backupCount=2, encoding=None)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(LOG_LEVEL)
    app_log = logging.getLogger('root')
    app_log.setLevel(LOG_LEVEL)
    app_log.addHandler(my_handler)

def tbl_data(cols, rval):
    columns = rows = []
    try:
        rows = [dict(zip(cols, row)) for row in rval]
        columns = [ {'name': col,
                     'label': col.capitalize(),
                     'field': col,
                     'required': True,
                     'sortable': True,
                     'align':  'right' if isinstance(rows[0][col], numbers.Number) else 'left' }
                    for col in cols]
    except TypeError:
        pass
    return columns, rows

def export_csv():
    FILE_PATH = '../../tmp/data.csv'
    logging.info("Export / download file")
    with open(FILE_PATH, 'w', newline='') as file:
        cols, rows = db.get_all_records()
        writer = csv.writer(file,doublequote=True, lineterminator="\n")
        writer.writerow(cols)
        writer.writerows(rows)
    ui.download(FILE_PATH)

def set_login_role(role: str = ""):
    app.storage.user['role'] =  role
    logging.info ("User role is set to " + app.storage.user.get('role', ""))

def get_login_role() -> str:
    return app.storage.user.get('role', "")

def is_admin() -> bool:
    r = app.storage.user.get('role', "") == 'admin'
    logging.info(f'User is { "" if r else "NOT "}admin' if LOGIN_ON else "User access is switch off")
    return r or (not LOGIN_ON)
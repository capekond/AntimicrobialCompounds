import csv
import logging
import numbers
from logging.handlers import RotatingFileHandler
import db

def set_logs():
    log_formatter = logging.Formatter('%(asctime)s - [%(levelname)6s] - %(funcName)s - %(message)s')
    my_handler = RotatingFileHandler('../../log/debug.log', mode='a', maxBytes=5*1024, backupCount=2, encoding=None)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.DEBUG)
    app_log = logging.getLogger('root')
    app_log.setLevel(logging.DEBUG)
    app_log.addHandler(my_handler)

def tbl_data(cols, rval):
    rows = [dict(zip(cols[0], row)) for row in rval]
    columns = [ {'name': col,
                 'label': col.capitalize(),
                 'field': col,
                 'required': True,
                 'sortable': True,
                 'align':  'right' if isinstance(rows[0][col], numbers.Number) else 'left' }
                for col in cols[0]]
    return columns, rows

def export_csv(ui):
    logging.info("Export / download file")
    with open('data.csv', 'w') as file:
        c, rows = db.get_all_records()
        export_file = csv.writer(file)
        export_file.writerows(rows)
    ui.download('data.csv')
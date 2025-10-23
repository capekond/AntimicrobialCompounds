import csv
import os
import numbers
from logging.handlers import RotatingFileHandler
from nicegui import ui
import db
from src.server.config import *


FILE_PATH = '../../tmp/data.csv'

with open(FILE_PATH, 'w', newline='') as file:
    cols, rows = db.get_all_records()
    print(cols)
    print(rows)
    writer = csv.writer(file, doublequote=True, lineterminator="\n")
    writer.writerow(cols)
    writer.writerows(rows)
# ui.download(FILE_PATH)
# os.remove(FILE_PATH)
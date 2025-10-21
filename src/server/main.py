import statistics
from nicegui import ui, events
import data_change
import db
from src.server.config import *
from io import StringIO
import pandas as pd

selected_ids = []

def root():
    ui.sub_pages({'/': main, '/add_page': add_page })

def main():
    res = db.get_active_records()
    ui.label('Information about active data').classes("title")
    with ui.grid(columns=2):
        ui.label("Sum:")
        ui.label(sum(res))
        ui.label("Count:")
        ui.label(str(len(res)))
        ui.label("Average: ")
        ui.label(f"{statistics.mean(res)}")
        ui.link('Go to add page', '/add_page')


def add_page():
    ui.label('Main page content')
    ui.link('Go to main page', '/')

data_change.set_logs()
logging.info("Start application...")
ui.add_css(shared=True, content="style.css")
ui.run(root, reload=False)
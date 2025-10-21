import statistics
from nicegui import ui, events
import data_change
import db
from src.server.config import *
from io import StringIO
import pandas as pd

selected_ids = []

def root():
    ui.sub_pages({'/': main, '/add_page': add_page, '/log_page': log_page })

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
    with ui.row():
        ui.link('Go to add page', '/add_page')
        ui.link('Go to log page', '/log_page')


async def add_page():
    logging.debug("Visit add page")
    ui.label('Add record').classes("title")
    val = ui.input(label='Type number', placeholder='0.0',
                   validation=lambda value: None if data_change.is_number(value, ba) else 'Not Number!')
    ba = ui.button('Add record', on_click=lambda: ui.notify(f'value {val.value} added'))
    ba.disable()
    ui.link('Go to main page', '/')
    while True:
        await ba.clicked()
        db.add_value(val.value)

def log_page():
    logging.debug("Visit log page")
    ui.label('Log page').classes("title")
    f = open("../../log/debug.log")
    log = ui.log(max_lines=100).classes("w-screen")
    log.push("\n".join(f.readlines()[-100:]))
    ui.link('Go to main page', '/')

data_change.set_logs()
logging.info("Start application...")
ui.add_css(shared=True, content="style.css")
ui.run(root, reload=False)
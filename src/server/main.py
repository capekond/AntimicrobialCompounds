import statistics
from nicegui import ui
import data_change
import db
import logging

@ui.page('/add_page')
async def add_page():
    logging.debug("Visit add page")
    ui.label('Add record')
    val = ui.input(label='Type number', placeholder='0.0', value="0.0")
    b = ui.button('Add record', on_click=lambda:  ui.notify(f'value {val.value} added'))
    ui.link('Go to main page', '/')
    while True:
        await b.clicked()
        db.add_value(val.value)

@ui.page('/see_page')
def see_page():
    logging.debug("Visit see page")
    ui.label('See records')
    cols, rows = db.get_all_records()
    columns, rows = data_change.tbl_data(cols, rows)
    tbl = ui.table(columns=columns, rows=rows, selection='multiple')
    ab = ui.button("Activate selected")
    x = ui.button("Delete selected")
    ui.link('Go to main page', '/')

@ui.page('/csv_page')
def csv_page():
    logging.debug("Visit csv page")
    ui.label('Export / import records')
    ui.checkbox("delete old data before import",value=False)
    ui.button(text="Export data")
    ui.button(text="Import data")
    ui.link('Go to main page', '/')

@ui.page('/log_page')
def log_page():
    logging.debug("Visit log page")
    ui.label('Log')
    f = open("../../log/debug.log")
    log = ui.log()
    log.push("\n".join(f.readlines()[-100:]))
    ui.button(text="Delete log", on_click=clear_log(log))
    ui.link('Go to main page', '/')

def clear_log(log) -> None:
    with open("../../log/debug.log", "r+") as f:
        f.seek(0)
        f.truncate()
        print("xxxxx")
        log.push("\n".join(f.readlines()[-100:]))

FORMAT = '%(asctime)s - [%(levelname)6s] - %(funcName)s - %(message)s'
logging.basicConfig(format=FORMAT, filename="../../log/debug.log", level=logging.DEBUG)
logging.info("Start application")
res = db.get_active_records()
ui.html('<strong>Information about active data<strong>')
ui.label(f"Sum: {sum(res)}")
ui.label(f"Count: {len(res)}")
ui.label(f"Average: {statistics.mean(res)}")
ui.link('Add records', add_page)
ui.link('See records', see_page)
ui.link('Export / import data', csv_page)
ui.link('See log', log_page)

ui.run(reload=False)
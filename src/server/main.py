import statistics
from nicegui import ui
import data_change
import db
import logging
from logging.handlers import RotatingFileHandler

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
    ui.input(placeholder="Add filter value").bind_value_to(tbl, 'filter')
    with ui.row():
        ab = ui.button("Activate selected", on_click=db.update_status(tbl.selected))
        x = ui.button("Delete selected")
        ui.link('Go to main page', '/')


@ui.page('/csv_page')
def csv_page():
    logging.debug("Visit csv page")
    ui.label('Export / import records')
    ui.checkbox("delete old data before import",value=False)
    ui.button(text="Export data", on_click=data_change.export_csv(ui))
    ui.button(text="Import data")
    ui.link('Go to main page', '/')

@ui.page('/log_page')
def log_page():
    logging.debug("Visit log page")
    ui.label('Log')
    f = open("../../log/debug.log")
    log = ui.log()
    log.push("\n".join(f.readlines()[-100:]))
    ui.link('Go to main page', '/')

data_change.set_logs()
logging.info("Start application...")
ui.add_css(shared=True,content="style.css")
res = db.get_active_records()
ui.label('Information about active data').classes("title")
with ui.grid(columns=2):
    ui.label(f"Sum:")
    ui.label(sum(res))
    ui.label(f"Count:")
    ui.label(str(len(res)))
    ui.label(f"Average: ")
    ui.label(f"{statistics.mean(res)}")
with ui.row():
    ui.link('\nAdd records', add_page)
    ui.link('See records', see_page)
    ui.link('Export / import data', csv_page)
    ui.link('See log', log_page)

ui.run(reload=False)
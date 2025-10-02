import statistics
from nicegui import ui
import data_change
import db

@ui.page('/add_page')
async def add_page():
    ui.label('Add record')
    val = ui.input(label='Type number', placeholder='0.0', value="0.0")
    b = ui.button('Add record', on_click=lambda:  ui.notify(f'value {val.value} added'))
    ui.link('Go to main page', '/')
    while True:
        await b.clicked()
        db.add_value(val.value)

@ui.page('/see_page')
def see_page():
    ui.label('See records')
    cols, rows = db.get_all_records()
    columns, rows = data_change.tbl_data(cols, rows)
    tbl = ui.table(columns=columns, rows=rows, selection='multiple')
    ab = ui.button("Activate selected")
    x = ui.button("Delete selected")
    ui.link('Go to main page', '/')

@ui.page('/csv_page')
def csv_page():
    ui.label('Export / import records')
    ui.checkbox("delete old data before import",value=False)
    ui.button(text="Export data")
    ui.button(text="Import data")
    ui.link('Go to main page', '/')

@ui.page('/log_page')
def log_page():
    ui.label('Log')
    ui.button(text="Delete log")
    ui.link('Go to main page', '/')

res = db.get_active_records()
ui.html('<strong>Information about active data<strong>')
ui.label(f"Sum: {sum(res)}")
ui.label(f"Count: {len(res)}")
ui.label(f"Average: {statistics.mean(res)}")
ui.link('Add records', add_page)
ui.link('See records', see_page)
ui.link('Export / import data', csv_page)
ui.link('See log', log_page)

ui.run()
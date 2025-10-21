import statistics
from nicegui import ui, events
import data_change
import db
from src.server.config import *
from io import StringIO
import pandas as pd

selected_ids = []

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


def is_number(s, ba: ui.button):
    try:
        float(s)
        ba.enable()
        return True
    except ValueError:
        ba.disable()
        return False

async def add_page():
    logging.debug("Visit add page")
    ui.label('Add record').classes("title")
    val = ui.input(label='Type number', placeholder='0.0',
                   validation=lambda value: None if is_number(value, ba) else 'Not Number!')
    ba = ui.button('Add record', on_click=lambda: ui.notify(f'value {val.value} added'))
    ba.disable()
    ui.link('Go to main page', '/')
    while True:
        await ba.clicked()
        db.add_value(val.value)

def see_page():
    with ui.dialog() as dialog, ui.card():
        d_label = ui.label()
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit(True))
            ui.button('No', on_click=lambda: dialog.submit(False))

    async def approve_activate():
        d_label.set_text(f"Activate {len(selected_ids)} records?")
        approve = await dialog
        if approve:
            db.update_status([sid['id'] for sid in selected_ids], "ACTIVE")
            ui.navigate.to('/see_page', new_tab=False)

    async def approve_delete():
        d_label.set_text(f"Delete {len(selected_ids)} records?")
        approve = await dialog
        if approve:
            db.delete_rows([sid['id'] for sid in selected_ids])
            ui.navigate.to('/see_page', new_tab=False)

    logging.debug("Visit see page")
    ui.label('See records').classes("title")
    cols, rows = db.get_all_records()
    columns, rows = data_change.tbl_data(cols, rows)
    tbl = ui.table(columns=columns, rows=rows, selection='multiple', pagination=TBL_ROW_COUNT,
                   on_select=lambda e: add_status(e.selection, ab, ad))
    ui.input(placeholder="Add filter value").bind_value_to(tbl, 'filter')
    with ui.row():
        ab = ui.button("Activate selected", on_click=approve_activate)
        ad = ui.button("Delete selected", on_click=approve_delete)
        ab.disable()
        ad.disable()
        ui.link('Go to main page', '/')

def csv_page():
    columns = [{'name': 'row_cnt', 'label': 'Added rows', 'field': 'row_cnt'}]
    logging.debug("Visit csv page")
    ui.label('Export / import records').classes("title")
    def handle_upload(e: events.UploadEventArguments):
        file_data = e.content.read()
        data_str = file_data.decode('utf-8')
        pd_data = pd.read_csv(StringIO(data_str))
        print(pd_data)
        tbl.set_visibility(True)
        upload_info = db.upload_data(import_scope.value, pd_data)
        tbl.add_row({'row_cnt': upload_info})
    with ui.row():
        with ui.column():
            ui.button(text="Export data", on_click=None)
        with ui.column():
            import_scope = ui.radio({'delete': "Delete old", 'update': "Update old", 'leave': "Leave old values"})
            ui.upload(on_upload=handle_upload, max_file_size=1_000_000).props('accept=.csv')
            tbl = ui.table(columns=columns, rows=[]).classes('h-52').props('virtual-scroll')
            tbl.set_visibility(False)
        ui.link('Go to main page', '/')

def log_page():
    logging.debug("Visit log page")
    ui.label('Log page').classes("title")
    f = open("../../log/debug.log")
    log = ui.log()
    log.push("\n".join(f.readlines()[-100:]))
    ui.link('Go to main page', '/')

def root():
    data_change.set_logs()
    logging.info("Start application...")
    ui.add_css(shared=True, content="style.css")
    ui.sub_pages({'/add_page': add_page, '/see_page': see_page, '/csv_page' : csv_page, 'log_page' :log_page })
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
        ui.link('\nAdd records', add_page)
        ui.link('See records', see_page)
        ui.link('Export / import data', csv_page)
        ui.link('See log', log_page)

ui.run(root, reload=False)

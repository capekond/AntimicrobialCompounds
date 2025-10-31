import statistics
from decor import *
from nicegui import ui, events
import data_change
from data_change import is_admin
import db
from src.server.config import *
from io import StringIO
import pandas as pd
import web_part as web

def root():
    ui.sub_pages({'/': main, '/add_page': add_page, '/see_page': see_page, '/import_page': import_page, '/export_page': export_page, '/log_page': log_page, "/welcome": welcome_page, "/login": login_page, "/logout_page": logout_page})

def logout_page():
    if not LOGIN_ON:
        ui.navigate.to("/")
    with ui.dialog() as dialog, ui.card():
        logging.info("Logout done")
        ui.label("Logout done")
        ui.button('OK', on_click=dialog.close)
    data_change.set_login_role()
    dialog.open()
    ui.navigate.to("/")


async def login_page():
    if not LOGIN_ON:
        ui.navigate.to("/")
    err = "Cannot log name not exists or wrong password"
    with ui.dialog() as dialog, ui.card():
        ui.label(err)
        ui.button('OK', on_click=dialog.close)
    ui.label('Login page').classes("title")
    name = ui.input("Name:")
    pwd = ui.input("Password:", password=True, password_toggle_button=True)
    go = ui.button("Login")
    await go.clicked()
    role: str = db.get_rule(name.value, pwd.value)
    if role:
        logging.info(f"Login ok as {role}")
        data_change.set_login_role(role)
    else:
        logging.error(err)
        dialog.open()
        await dialog
    ui.navigate.to("/")

@logged
@has_records
def main():
    res = db.get_records_ids()
    ui.label('Information about active data').classes("title")
    if not res:
        logging.warning("No active data in database.")
        ui.label("No active data in database. Nothing can be calculated.").classes("warning")
    else:
        with ui.grid(columns=2):
            ui.label("Sum:")
            ui.label(str(sum(res)))
            ui.label("Count:")
            ui.label(str(len(res)))
            ui.label("Average: ")
            ui.label(f"{statistics.mean(res)}")
    web.footer(True,False,True,True,True, True, True)

@logged
def welcome_page():
    if db.no_data():
        logging.warning("Useless access to welcome page via deep link")
        ui.navigate.to("/")
    ui.label('Welcome new user, let put some data first').classes("title")
    web.footer(True, False, True, False, True, False, True)

@logged
async def add_page():
    logging.debug("Visit add page")
    ui.label('Add record').classes("title")
    if is_admin():
        val = ui.input(label='Type number', placeholder='0.0', validation=lambda value: None if data_change.is_number(value, ba) else 'Not Number!')
        ba = ui.button('Add record', on_click=lambda: ui.notify(f'value {val.value} added'))
        ba.disable()
        web.footer(True, True)
        while True:
            await ba.clicked()
            db.add_value(val.value)
    else:
        ui.label('Sorry, only admin can add records.')
        web.footer(True, True)

@logged
@has_records
def see_page():
    with ui.dialog() as dialog, ui.card():
        d_label = ui.label()
        with ui.row():
            ui.button('Yes', on_click=lambda: dialog.submit(True))
            ui.button('No', on_click=lambda: dialog.submit(False))

    async def approve_activate():
        d_label.set_text(f"Activate {len(web.selected_ids)} records?")
        approve = await dialog
        if approve:
            db.update_status([sid['id'] for sid in web.selected_ids], "ACTIVE")
            ui.navigate.reload()

    async def approve_delete():
        d_label.set_text(f"Delete {len(web.selected_ids)} records?")
        approve = await dialog
        if approve:
            db.delete_rows([sid['id'] for sid in web.selected_ids])
            ui.navigate.reload()

    logging.debug("Visit see page")
    ui.label('See records').classes("title")
    cols, rows = db.get_all_records()
    columns, rows = data_change.tbl_data(cols, rows)
    tbl = ui.table(columns=columns, rows=rows, selection= 'multiple' if is_admin() else None, pagination=TBL_ROW_COUNT,
                   on_select=lambda e: web.add_status(e.selection, ab, ad))
    ui.input(placeholder="Add filter value").bind_value_to(tbl, 'filter')
    if is_admin():
        with ui.row():
            ab = ui.button("Activate selected", on_click=approve_activate)
            ad = ui.button("Delete selected", on_click=approve_delete)
            ab.disable()
            ad.disable()
    web.footer(True, True)

@logged
def import_page():

    async def handle_upload(e: events.UploadEventArguments):
        file_data = await e.file.text()
        pd_data = pd.read_csv(StringIO(file_data))
        tbl.set_visibility(True)
        upload_info = db.upload_data(import_scope.value, pd_data)
        tbl.add_row({'row_cnt': upload_info})

    columns = [{'name': 'row_cnt', 'label': 'Added rows', 'field': 'row_cnt'}]
    logging.debug("Visit import page")
    ui.label('Import records').classes("title")
    if is_admin():
        import_scope = ui.radio({'delete': "Delete old", 'update': "Update old", 'leave': "Leave old values"}, value='update')
        ui.upload(on_upload=handle_upload, max_file_size=1_000_000).props('accept=.csv')
        tbl = ui.table(columns=columns, rows=[]).classes('h-52').props('virtual-scroll')
        tbl.set_visibility(False)
    else:
        ui.label("Only admin can import data.")
    web.footer(True, True)

@logged
@has_records
async def export_page():
    logging.debug("Visit export page")
    ui.label('Export records').classes("title")
    ed = ui.button(text="Export data")
    web.footer(True, True)
    while True:
        await ed.clicked()
        data_change.export_csv()

@logged
def log_page():
    logging.debug("Visit log page")
    ui.label('Log page').classes("title")
    f = open("../../log/debug.log")
    log = ui.log(max_lines=100).classes("w-screen")
    log.push("\n".join(f.readlines()[-100:]))
    web.footer(True, True)

data_change.set_logs()
logging.info("Start application...")
ui.add_css(shared=True, content="style.css")
ui.run(root, reload=False, storage_secret='6546546875321564654324')
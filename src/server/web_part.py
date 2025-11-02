import statistics
import db
from nicegui import ui
from config import *
from data_change import is_admin

selected_ids = []

def sys_info(title: str = "About..."):
    async def show_edit():
        with ui.dialog() as dialog, ui.card():
            with open("../../data/sys_info.html", "r") as file:
                cnt = file.read()
            editor = ui.editor(value=cnt)
            with ui.row():
                ui.button('Save', on_click=lambda: dialog.submit(True))
                ui.button('Cancel', on_click=lambda: dialog.submit(False))
        approve = await dialog
        if approve:
            with open("../../data/sys_info.html", "w") as file:
                file.write(editor.value)
            ui.navigate.reload()

    with open("../../data/sys_info.html", "r") as file:
        content = file.read()
    ui.label(title).classes('title')
    with ui.row():
        ui.html(content, sanitize=False)
        edit = ui.button("Edit", on_click=show_edit)
        edit.visible = is_admin()

def data_info(title:str = 'Information about active data'):
    res = db.get_records_ids()
    ui.label(title).classes("title")
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

def footer(logout: bool = False, main: bool = False, add: bool = False, see: bool = False, inport: bool = False,
           export: bool = False, log: bool = False, users: bool = False):
    with ui.row():
        ui.link('logout', '/logout_page').visible = LOGIN_ON and logout
        ui.link('Go to main page', '/').visible = main
        ui.link('Go to add page', '/add_page').visible = add
        ui.link('Go to see page', '/see_page').visible = see
        ui.link('Go to import page', '/import_page').visible = inport
        ui.link('Go to export page', '/export_page').visible = export
        ui.link('Go to log page', '/log_page').visible = log
        ui.link('Go to users management', '/users_page').visible = users

def add_status(selection, buttons: list[ui.button]):
    global selected_ids
    selected_ids = selection
    for button in buttons:
        button.enable() if len(selected_ids) > 0 else button.disable()
    logging.debug(f"In table data selected row(s): {selected_ids}")
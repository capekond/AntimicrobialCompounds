from nicegui import ui


def footer(logout: bool = False, main: bool = False, add: bool = False, see: bool = False, inport: bool = False,
           export: bool = False, log: bool = False):
    with ui.row():
        ui.link('logout', '/logout_page').visible = logout
        ui.link('Go to main page', '/').visible = main
        ui.link('Go to add page', '/add_page').visible = add
        ui.link('Go to see page', '/see_page').visible = see
        ui.link('Go to import page', '/import_page').visible = inport
        ui.link('Go to export page', '/export_page').visible = export
        ui.link('Go to log page', '/log_page').visible = log

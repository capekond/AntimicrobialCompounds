from nicegui import ui
import db

@ui.page('/add_page')
def add_page():
    ui.label('Add records')

@ui.page('/see_page')
def see_page():
    ui.label('See records')

db = db.Db
rec = db.get_active_records(db())

ui.link('Add records', add_page)
ui.link('See records', add_page)

ui.run()
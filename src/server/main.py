import statistics
from nicegui import ui
import data_change
import db

@ui.page('/add_page')
def add_page():
    ui.label('Add record')
    ui.input(label='Type number', placeholder='0.0', validation={'Must be real number': lambda value: len(value) < 20})
    ui.link('Go to main page', '/')

@ui.page('/see_page')
def see_page():
    ui.label('See records')
    import db
    db = db.Db
    cols, rows = db.get_all_records(db())
    columns, rows = data_change.tbl_data(cols, rows)
    ui.table(columns=columns, rows=rows)
    ui.link('Go to main page', '/')


db = db.Db
res = db.get_active_records(db())
ui.html('<strong>Information about data<strong>')
ui.label(f"Sum: {sum(res)}")
ui.label(f"Count: {len(res)}")
ui.label(f"Average: {statistics.mean(res)}")
ui.html("<h1>Navigation</h1>")
ui.link('Add records', add_page)
ui.link('See records', see_page)



ui.run()
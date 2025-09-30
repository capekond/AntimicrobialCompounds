from nicegui import ui
import sqlite3

@ui.page('/other_page')
def other_page():
    ui.label('Add records')

@ui.page('/dark_page')
def dark_page():
    ui.label('See records')

ui.link('Add records', other_page)
ui.link('See records', dark_page)

ui.run()
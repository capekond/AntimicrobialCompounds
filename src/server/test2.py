from io import StringIO
import pandas as pd
from nicegui import events, ui

def handle_upload(e: events.UploadEventArguments):
    file_data = e.content.read()
    data_str = file_data.decode('utf-8')
    pd_data = pd.read_csv(StringIO(data_str))
    tbl.set_visibility(True)
    tbl.add_row({'row_cnt': len(pd_data)})

ui.upload(on_upload=handle_upload, max_file_size=1_000_000).props('accept=.csv')
columns = [{'name': 'row_cnt', 'label': 'Added rows', 'field': 'row_cnt'}]
tbl = ui.table(columns=columns, rows=[]).classes('h-52').props('virtual-scroll')
tbl.set_visibility(False)

ui.run(title="Compounds")
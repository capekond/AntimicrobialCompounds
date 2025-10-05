import csv
import logging
import numbers
import db

def tbl_data(cols, rval):
    rows = [dict(zip(cols[0], row)) for row in rval]
    columns = [ {'name': col,
                 'label': col.capitalize(),
                 'field': col,
                 'required': True,
                 'sortable': True,
                 'align':  'right' if isinstance(rows[0][col], numbers.Number) else 'left' }
                for col in cols[0]]
    return columns, rows

def export_csv(ui):
    logging.info("Export / download file")
    with open('data.csv', 'w') as file:
        c, rows = db.get_all_records()
        export_file = csv.writer(file)
        export_file.writerows(rows)
    ui.download('data.csv')
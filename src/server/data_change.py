import numbers

import db
import statistics

# db = db.Db
#
#
# cols, rval = db.get_all_records(db())
def tbl_data(cols, rval):
    rows = [dict(zip(cols, row)) for row in rval]
    columns = [ {'name': col, 'label': col.capitalize(), 'field': col, 'required': True, 'sortable': True, 'align':  'right' if isinstance(rows[0][col], numbers.Number) else 'left' } for col in cols]
    return columns, rows
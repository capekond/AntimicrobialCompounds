import numbers

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


import data_change
import db
from src.server.config import *

data_change.export_xls()

import pandas as pd

df = pd.DataFrame({'status': ["NEW", "ACTIVE"], 'value': [3.3, "4.AA03"], 'id': [1, 2]})
# df = pd.DataFrame()
# print (df)
# print(df.columns)
# print(df.dtypes)
# print(df.columns.values)
# print(len(df.columns.values))
dff, err = db.data_import_error(df, IMPORT_COLS)
print(err)
print(dff)

# t = int
# cell = "a"
# if not type(cell) is t:
#     print("OK")

# s_type = TypeVar('SetType', int, int)
# def set_type(val) -> s_type:
#     return int(val)
# print(set_type(cell))

# a = int
# print(type(a))
# print(type(a) == type)
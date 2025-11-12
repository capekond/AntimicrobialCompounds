import sqlite3
from io import StringIO
from typing import Any
from nicegui import ui
from pandas import DataFrame
from sqlalchemy import create_engine
import pandas as pd
from config import *

def data_import_error(data: pd.DataFrame, cols: dict) -> tuple[DataFrame, str]:
    err = []
    if data.empty:
        err.append(f"Missing data")
    if not set(cols.keys()) == set(data.columns.values):
        err.append(f"Wrong data headers. Expected: {cols.keys()}  Received: {data.columns.values}")
    for col in cols.items():
        try:
            for rowid, cell in  enumerate(data[col[0]].tolist()):
                if type(col[1]) == type:
                    if not type(cell) is col[1]:
                        err.append(f"Value {cell} in column {col[0]} and row {rowid} is not expected type {col[1]}  but {type(cell)}.")
                elif not cell in col[1]:
                    err.append(f"Value {cell} in column '{col[0]}' and row {rowid} is not in list of supported values {col[1]}.")
        except KeyError:
            err.append(f"No column named '{col[0]}'")
    return data, "Data errors:\n\t" + "\n\t".join(err) if err else ""

def _execute_sql(sql:str):
    logging.info(f"Try execute SQL: {sql}")
    con = sqlite3.connect("../../data/data.db")
    cur = con.cursor()
    cur.execute(sql)
    try:
        cols = [i[0] for i in cur.description]
    except TypeError:
        cols = []
        logging.warning("No data in table")
    rows = cur.fetchall()
    con.commit()
    con.close()
    return cols, rows

def get_records_ids(status = 'ACTIVE') -> list[int]:
    cols, rows =_execute_sql(f"SELECT value FROM data WHERE status='{status}' ORDER BY id;")
    res = [int(i[0]) for i in rows]
    logging.info(f"Get {len(res)} ids for status '{status}")
    return res

def get_all_records() -> tuple[list[Any], list[Any]]:
    return  _execute_sql("SELECT id, value, status FROM data ORDER BY id;")

def add_value(val):
    _execute_sql(f"INSERT INTO data(value, status) VALUES('{val}', 'NEW');")

def update_status(sids:str, status: str):
    _execute_sql(f"UPDATE data SET status = '{status}' WHERE ID IN ({sids});")

def delete_rows(sids:str):
    _execute_sql(f"DELETE FROM data WHERE id IN ({sids});")

def delete_all():
    _execute_sql("DELETE FROM data;")

def no_data() -> bool:
    c, r = get_all_records()
    return True if r else False

def upload_data(import_scope:str, file_data: bytes, extension: str  ) -> str:
    pd_data: pd.DataFrame
    if extension == ".csv":
        pd_data = pd.read_csv(StringIO(str(file_data)))
    else:
        pd_data = pd.read_excel(file_data)
    res = data_import_error(pd_data, IMPORT_COLS)
    if res:
        err = f"Cannot upload data: {res}"
        logging.error(err)
        return err
    ids = "'" + "','".join(pd_data["id"])  + "'"
    if import_scope == 'update':
        delete_rows(ids)
    if import_scope == 'leave':
        cols, rows = get_all_records()
        idx = [i[0] for i in rows]
        pd_data = pd_data[~pd_data['id'].isin(idx)]
    if import_scope == 'delete':
        delete_all()
        logging.info("data table content is deleted")
    pd_data.set_index('id', inplace=True)
    engine = create_engine('sqlite:///../../data/data.db', echo=False)
    info = pd_data.to_sql('data', con=engine, if_exists='append')
    logging.info(f"Update affect {info} rows in data table.")
    return str(info)

def get_role(name: str, pwd: str = "") -> str:
    if pwd:
        c, r = _execute_sql(f"SELECT * FROM users WHERE id='{name}' AND pwd = '{pwd}';")
    else:
        c, r = _execute_sql(f"SELECT * FROM users WHERE id='{name}';")
        ui.notify(f"User {name} exists.")
    return r[0][2] if r else ""

def get_users():
    return _execute_sql("SELECT id, role FROM users ORDER BY id;")

def add_user(username: str ,new_pwd: str,role: str):
    _execute_sql(f"INSERT INTO users(id, pwd, role) VALUES('{username}','{new_pwd}','{role}');")

def delete_user(usernames: str):
    _execute_sql(f"DELETE FROM users WHERE id IN ({usernames});")

def change_pwd(username: str, new_pwd: str):
    _execute_sql(f"UPDATE users SET pwd = '{new_pwd}' WHERE ID = {username};")
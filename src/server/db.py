import logging
import sqlite3
from sqlalchemy import create_engine
import pandas as pd
from config import *


def _data_import_error(df: pd.DataFrame):
    err = []
    if df.empty:
        err.append(f"Missing data")
    for col in ['id', 'status', 'value']:
        if not col in df.columns:
            err.append(f"Missing excepted field '{col}'")
    try:
        if not df.dtypes['value'] in ['float64', 'int64']:
            err.append(f"Field 'value' is not numeric ")
        if not pd.Series(df['id']).is_unique:
            err.append(f"Index id is not unique ")
    except:
        pass
    return err

def _execute_sql(sql:str):
    con = sqlite3.connect("../../data/data.db")
    cur = con.cursor()
    cur.execute(sql)
    try:
        cols = [i[0] for i in cur.description],
    except TypeError:
        cols = []
    rows = cur.fetchall()
    con.commit()
    con.close()
    logging.info(f"SQL: {sql}")
    return cols, rows

def get_active_records():
    cols, rows =_execute_sql("SELECT value FROM data WHERE status='ACTIVE' ORDER BY id;")
    return [i[0] for i in rows]

def get_all_records():
    return  _execute_sql("SELECT id, value, status FROM data ORDER BY id;")

def add_value(val):
    _execute_sql(f"INSERT INTO data(value, status) VALUES('{val}', 'NEW');")

def update_status(sids:list[int], status: str):
    _execute_sql(f"UPDATE data SET status = '{status}' WHERE ID IN ({",".join([str(ssid) for ssid in sids] ) });")

def delete_rows(sids:list[int]):
    _execute_sql(f"DELETE FROM data WHERE id IN ({",".join([str(ssid) for ssid in sids])});")

def delete_all():
    _execute_sql("DELETE FROM data;")

# def export_data():
#     d = get_all_records()


def upload_data(import_scope:str, df: pd.DataFrame) -> str:
    logging.info(f"Try to pload {len(pd.DataFrame)} records in scope {import_scope}")
    res = _data_import_error(df)
    if res:
        err = f"Cannot upload data: {res}"
        logging.error(err)
        return err
    ids = df["id"].to_list()
    if import_scope == 'update':
        delete_rows(ids)
    if import_scope == 'leave':
        cols, rows = get_all_records()
        idx = [i[0] for i in rows]
        df = df[~df['id'].isin(idx)]
    if import_scope == 'delete':
        delete_all()
        logging.info("data table content is deleted")
    df.set_index('id', inplace=True)
    engine = create_engine('sqlite:///../../data/data.db', echo=False)
    info = df.to_sql('data', con=engine, if_exists='append')
    logging.info(f"Update affect {info} rows in data table.")
    return str(info)
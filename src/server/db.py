import logging
import sqlite3

def _execute_sql(sql:str):
    con = sqlite3.connect("data.db")
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

def upload_data(delete_old:bool):
    pass
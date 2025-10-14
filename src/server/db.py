import logging
import pprint
import sqlite3

def get_active_records():
    sql="SELECT value FROM data WHERE status='ACTIVE' ORDER BY id;"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    res = [i[0] for i in cur.fetchall()]
    con.close()
    logging.info(f"SQL: {sql}")
    logging.debug(f"Data: {res}")
    return res


def get_all_records():
    sql="SELECT id, value, status FROM data ORDER BY id;"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    cols =  [i[0] for i in cur.description],
    rows =  cur.fetchall()
    con.close()
    logging.info(f"SQL: {sql}")
    return  cols, rows

def add_value(val):
    sql = f"INSERT INTO data(value, status) VALUES('{val}', 'NEW');"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    logging.info(f"SQL: {sql}")

def update_status(sids:list[int], status: str):
    sql = f"UPDATE data SET status = '{status}' WHERE ID IN ({",".join([str(ssid) for ssid in sids] ) });"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    logging.info(f"SQL: {sql}")

def delete_rows(sids:list[int]):
    sql = f"DELETE FROM data WHERE id IN ({",".join([str(ssid) for ssid in sids])});"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    logging.info(f"SQL: {sql}")

def upload_data(delete_old:bool):
    pass
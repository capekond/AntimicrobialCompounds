import logging
import sqlite3

def get_active_records():
    sql="SELECT value FROM data WHERE status='ACTIVE' ORDER BY id;"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    res = [i[0] for i in cur.fetchall()]
    con.close()
    logging.info(f"SQL: {sql}")
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


def download_data():
    pass

def add_value(val):
    sql = f"INSERT INTO data(value, status) VALUES('{val}', 'NEW');"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    logging.info(f"SQL: {sql}")

def set_status(idx, status):
    sql = f"UPDATE data SET status='{status}' WHERE id='{idx}';"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    logging.info(f"SQL: {sql}")

def delete_rec(ids:list):
    sql = f"DELETE FROM data WHERE id IN ({",".join(ids)});"
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    logging.info(f"SQL: {sql}")

def upload_data(delete_old:bool):
    pass
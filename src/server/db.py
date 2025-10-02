import sqlite3

def get_active_records():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT value FROM data WHERE status='ACTIVE' ORDER BY id;")
    res = [i[0] for i in cur.fetchall()]
    con.close()
    return res

def get_all_records():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT id, value, status FROM data ORDER BY id;")
    cols =  [i[0] for i in cur.description],
    rows =  cur.fetchall()
    con.close()
    return  cols, rows


def download_data():
    pass

def add_value(val):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    sql = f"INSERT INTO data(value, status) VALUES('{val}', 'NEW');"
    cur.execute(sql)
    con.commit()
    con.close()

def set_status(idx, status):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    sql = f"UPDATE data SET status='{status}' WHERE id='{idx}';"
    cur.execute(sql)
    con.commit()
    con.close()

def delete_rec(ids:list):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    sql = f"DELETE FROM data WHERE id IN ({",".join(ids)});"
    cur.execute(sql)
    con.commit()
    con.close()

def upload_data(delete_old:bool):
    pass
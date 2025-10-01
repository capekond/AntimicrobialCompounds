import sqlite3

class Db:
    def __init__(self):
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()

    def get_active_records(self):
        self.cur.execute("SELECT value FROM data WHERE status='ACTIVE' ORDER BY id;")
        return self.cur.fetchall()

    def get_all_records(self):
        self.cur.execute("SELECT value FROM data ORDER BY id;")
        return self.cur.fetchall()

    def add_value(self, val):
        self.cur.execute(f"INSERT INTO data(value, status) VALUES('{val}', 'NEW');")
        self.con.commit()

    def set_status(self, idx, status):
        sql = f"UPDATE data SET status='{status}' WHERE id='{idx}';"
        s = self.cur.execute(sql)
        self.con.commit()
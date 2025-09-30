import sqlite3

class Db:
    def __init__(self):
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()

    def get_active_records(self):
        self.cur.execute("SELECT values FROM data WHERE status='ACTIVE' ORDER BY id;")
        return self.cur.fetchall()

    def get_all_records(self):
        self.cur.execute("SELECT values FROM data ORDER BY id;")
        return self.cur.fetchall()

    def add_value(self, val):
        self.cur.execute("INSERT INTO data(value, status) VALUES(?, 'NEW');", val.value)
        self.con.commit()

    def set_status(self, idx, status):
        self.cur.execute("UPDATE data SET status=? WHERE id=?;", (status.value,  idx.value))
        self.con.commit()
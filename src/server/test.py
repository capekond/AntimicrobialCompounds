import statistics
import db
import data_change

db = db.Db
cols, rows = db.get_all_records(db())
columns, rows = data_change.tbl_data(cols, rows)

print(columns)
print(rows)


res = db.get_active_records(db())

print(res)
print(f"Sum: {sum(res)}")
print(f"Len: {len(res)}")
print(f"Average: {statistics.mean(res)}")
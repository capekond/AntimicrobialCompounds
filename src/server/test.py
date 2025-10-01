import db
import statistics

db = db.Db
db.add_value(db(), 10.3)
# rec = db.get_active_records(db())
# print(rec)
rec = db.get_all_records(db())
print(rec)
# db.set_status(db(),8,"ACTIVE")
rec = db.get_active_records(db())
print(rec)
print(sum(rec))
print(statistics.mean(rec))
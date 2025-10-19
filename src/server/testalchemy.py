from sqlalchemy import create_engine
import pandas as pd
import db

def data_import_error(df: pd.DataFrame):
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

print(db.get_all_records())

update = True # if true update existing values else ylu leave it
dataset = {'id': [90,95, 57], 'value': [1000,1000, 7444], 'status': ["ACTIVE", "NEW", "NEW"]}
df = pd.DataFrame(data=dataset)
ids = df["id"].to_list()

res = data_import_error(df)
if res:
    print("\n".join(res))
    exit(1)


if update:
    db.delete_rows(ids)
else:
    cols, rows = db.get_all_records()
    idx = [i[0] for i in rows]
    df = df[~df['id'].isin(idx) ]

df.set_index('id', inplace=True)
engine = create_engine('sqlite:///../../data/data.db', echo=False)
df.to_sql('data',  con=engine, if_exists='append')
print(db.get_all_records())
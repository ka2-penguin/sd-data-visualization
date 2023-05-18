import sqlite3
import json

DB_FILE = "data.db"

db = None

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def db_close():
    db.commit()
    db.close()

def get_month_histogram_data() -> dict:
    # {month: (total,non_members)}
    data = dict()
    c = db_connect()
    last_max_id = 0
    try:
        for month in range(1,13):
            # total = int(tuple(c.execute('SELECT count(1) FROM trips WHERE month=?',(month,)))[0][0])
            max_id = int(tuple(c.execute('SELECT max(rowid) FROM trips WHERE month=?',(month,)))[0][0])
            total = max_id - last_max_id
            last_max_id = max_id

            non_members_count = int(tuple(c.execute('SELECT count(1) FROM trips WHERE month=? and is_member=0',(month,)))[0][0])
            data_pair = (total,non_members_count)
            print(f'{data_pair = }')
            data[month] = data_pair
    except:
        db_close()
        raise
    db_close()
    return data

def load_json():
    data = get_month_histogram_data()
    with open('monthly_data.json','w') as f:
        json.dump(data,f)


if __name__ == '__main__':
    # print(get_month_histogram_data())
    load_json()
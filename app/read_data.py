import sqlite3

DB_FILE = "data.db"

db = None

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def db_close():
    db.commit()
    db.close()

def get_trips(trip_duration,year,month,day,hour,minute,is_member,start_station_id,end_station_id):
    c = db_connect()
    c.execute('SELECT * FROM TRIPS WHERE year=?,month=?, by year SORT BY DEC', ())
    db_close()

def create_filter(filters):
    filter = "SELECT * FROM TRIPS WHERE"


def get_ridership_by_month():
    c = db_connect()
    for year in (2021,2022,2023):
        year_data = []
        for month in range(1,13):
            if year == 2023 and month == 5:
                break

            num_of_rides = tuple(c.execute('SELECT count(1) FROM TRIPS WHERE year=? and month=?',(year,month)))[0][0]
            # print(num_of_rides[0][0])
            print(num_of_rides)
            year_data.append(num_of_rides)
            # break
    db_close()
    print(year_data)
    return year_data

if __name__ == '__main__':
    get_ridership_by_month()


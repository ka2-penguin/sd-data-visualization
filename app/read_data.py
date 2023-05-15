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

def get_trips(filters):
    c = db_connect()
    filter = create_sql_filter(filters)
    c.execute(filter, ())
    db_close()

def create_sql_filter(filters: dict[str, str]) -> str:
    filter = "SELECT * FROM TRIPS"
    # will not work becuase the dict still has stuff inside, even if they are empty strings
    # possible solution is a try catch statement that defaults to getting the 100 most recent trips
    if filters: 
        filter += " WHERE"
    if filters["min_trip_duration"]:
        filter += f", trip_duration >= " + filters["min_trip_duration"]
    if filters["max_trip_duration"]:
        filter += f", trip_duration <= " + filters["max_trip_duration"]

    if filter["min_date"]:
        date = filter["min_date"].split(",")
        filter += f", year >= {date[0]}, month >= {date[1]}, day >= {date[2]}, hour >= {date[3]}, min >= {date[4]}"
    if filter["max_date"]:
        date = filter["min_date"].split(",")
        filter += f", year <= {date[0]}, month <= {date[1]}, day <= {date[2]}, hour <= {date[3]}, min <= {date[4]}"

    if filter["is_member"]:
        filter += ", is_member = " + filter["is_member"]

    if filter["start_station_id"]:
        filter += ", start_station_id = " + filter["start_station_id"]
    if filter["end_station_id"]:
        filter += ", end_station_id = " + filter["end_station_id"]
    
    filter += ",BY year SORT BY dec"
    return filter


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


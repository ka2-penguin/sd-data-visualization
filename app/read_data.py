import sqlite3

DB_FILE = "data.db"
MAX_RESULTS = 100
db = None

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def db_close():
    db.commit()
    db.close()

def get_trips(filters) -> list[list[str]]:
    c = db_connect()
    filter = create_sql_filter(filters)
    results = list(c.execute(filter, ()))
    db_close()
    return results

def create_sql_filter(filters: dict[str, str]) -> str:
    # LIMIT {MAX_RESULTS}
    filter = f"SELECT * FROM trips"
    # will not work becuase the dict still has stuff inside, even if they are empty strings
    # possible solution is a try catch statement that defaults to getting the 100 most recent trips
    if filters: 
        filter += " WHERE"
    if filters["min_trip_duration"]:
        filter += f" AND trip_duration >= " + filters["min_trip_duration"]
    if filters["max_trip_duration"]:
        filter += f" AND trip_duration <= " + filters["max_trip_duration"]

    if filters["min_date"]:
        date = filters["min_date"].split("-")
        filter += f" AND year >= {date[0]} AND month >= {date[1]} AND day >= {date[2]}"
    if filters["max_date"]:
        date = filters["max_date"].split("T")[0].split("-")
        filter += f" AND year <= {date[0]} AND month <= {date[1]} AND day <= {date[2]}"

    if filters["min_time"]:
        time = filters["min_time"].split(":")
        filter += f" AND hour >= {time[0]} AND min >= {time[1]}"
    if filters["max_time"]:
        time = filters["max_time"].split(":")
        filter += f" AND hour <= {time[0]} AND min <= {time[1]}"


    if filters["is_member"]:
        filter += " AND is_member = " + str(filters["is_member"]) # might have to format boolean to match sqlite

    if filters["start_station_id"]:
        filter += " AND start_station_id = " + filters["start_station_id"]
    if filters["end_station_id"]:
        filter += " AND end_station_id = " + filters["end_station_id"]
    
    filter += " ORDER BY year DESC"

    # remove extra comma at the start of filter
    i = filter.find("WHERE") + len("WHERE")
    filter = filter[:i] + filter[i+len("AND")+1:]

    print(f"SQL filter: {filter}")
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


"""SELECT * FROM TRIPS LIMIT 100 WHERE trip_duration >= 1 AND trip_duration <= 2 AND year >= 2023 AND month >= 05 AND day >= 10 AND year <= 2023 AND month <= 05 AND day <= 19 AND hour >= 03 AND min >= 04 AND hour <= 05 AND min <= 06 AND start_station_id = C AND end_station_id = test ORDER BY year DESC"""
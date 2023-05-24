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
    print(results)
    db_close()
    return results

def get_coord_from_id(station_id):
    c = db_connect()
    # filter = create_sql_filter(filters)
    coord = tuple(c.execute('SELECT latitude,longitude FROM stations WHERE rowid=?', (station_id,)))[0]
    db_close()
    # print(coord)
    return coord

def get_csv_coords(id1,id2):
    coord1 = get_coord_from_id(id1)
    coord2 = get_coord_from_id(id2)

    return f'{coord1[0]},{coord1[1]},{coord2[0]},{coord2[1]}'

def get_csv_coords_list(data):
    csv_list = []
    for row in data:
        csv_row = get_csv_coords(row[-2],row[-1])
        csv_list.append(csv_row)
    return csv_list

def create_sql_filter(filters: dict[str, str]) -> str:
    filter = f"SELECT * FROM trips"
    # will not work becuase the dict still has stuff inside, even if they are empty strings
    # possible solution is a try catch statement that defaults to getting the 100 most recent trips

    if not are_filters_empty(filters): 
        filter += " WHERE"
    if filters["min_trip_duration"]:
        filter += f" AND trip_duration >= " + filters["min_trip_duration"]
    if filters["max_trip_duration"]:
        filter += f" AND trip_duration <= " + filters["max_trip_duration"]

    if filters["min_date"]:
        date = filters["min_date"].split("-")
        # filter += f" AND year >= {date[0]} AND month >= {date[1]} AND day >= {date[2]}"
        filter += f" AND month >= {date[1]} AND day >= {date[2]}"
    if filters["max_date"]:
        date = filters["max_date"].split("T")[0].split("-")
        # filter += f" AND year <= {date[0]} AND month <= {date[1]} AND day <= {date[2]}"
        filter += f" AND month >= {date[1]} AND day >= {date[2]}"

    if filters["min_time"]:
        time = filters["min_time"].split(":")
        filter += f" AND hour >= {time[0]} AND minute >= {time[1]}"
        filter += f" AND hour >= {time[0]} AND minute >= {time[1]}"
    if filters["max_time"]:
        time = filters["max_time"].split(":")
        filter += f" AND hour <= {time[0]} AND minute <= {time[1]}"


    if filters["is_member"]:
        filter += " AND is_member = " + str(filters["is_member"]) # might have to format boolean to match sqlite

    if filters["start_station_id"]:
        filter += " AND start_station_id = " + filters["start_station_id"]
    if filters["end_station_id"]:
        filter += " AND end_station_id = " + filters["end_station_id"]
    
    # if not are_filters_empty(filters):
        # filter += f" ORDER BY year DESC LIMIT {MAX_RESULTS}"
    filter += f" ORDER BY month, day, hour, minute"
    print(f'{filter = }')
    
    # remove extra AND at the start of filter
    find_index = filter.find("WHERE AND")
    if find_index != -1:
        i = find_index + len("WHERE")
        filter = filter[:i] + filter[i+len("AND")+1:]

    filter += f"LIMIT {MAX_RESULTS}"
    print(f"SQL filter: {filter}")
    return filter

def are_filters_empty(filters):
    for i in filters.values():
        if i != "":
            return False
    return True

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

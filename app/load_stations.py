import sqlite3
import csv
# from datetime import datetime

FILENAMES = (
    '202201-citibike-tripdata.csv',
    '202202-citibike-tripdata.csv',
    '202203-citibike-tripdata.csv',
    '202204-citibike-tripdata.csv',
    '202205-citibike-tripdata.csv',
    '202206-citbike-tripdata.csv',
    '202207-citbike-tripdata.csv',
    '202208-citibike-tripdata.csv',
    '202209-citibike-tripdata.csv',
    '202210-citibike-tripdata.csv',
    '202211-citibike-tripdata.csv',
    '202212-citibike-tripdata.csv',
)

DB_FILE = "data.db"

db = None

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def db_close():
    db.commit()
    db.close()

# creates a table if it doesn't exist
# rowid starts from 1 and increments ++
def db_table_inits():
    c = db_connect()

    c.execute("CREATE TABLE IF NOT EXISTS stations (station_name text, \
        latitude float, longitude float)")
    db_close()


def get_trip_duration(start_date, start_time, end_date, end_time):
    start_hms = (int(start_time[:2]), int(start_time[3:5]), int(start_time[6:]))
    end_hms = (int(end_time[:2]), int(end_time[3:5]), int(end_time[6:]))

    start_secs = start_hms[0] * 3600 + start_hms[1] * 60 + start_hms[2]
    end_secs = end_hms[0] * 3600 + end_hms[1] * 60 + end_hms[2]
    if start_date == end_date:
        return end_secs - start_secs

    start_day = int(start_date[-2:])
    end_day = int(end_date[-2:])

    # months are the same
    if start_date[5:7] == end_date[5:7] and end_day - start_day == 1:
        return 24*(60**2) + end_secs - start_secs
    
    # no rides inbetween months or over a day
    return -1

def round_coord(loc_value):
    # round(loc_value,4)
    # loc_value*1000 % 10
    if loc_value < 0:
        negative = True
        loc_value *= -1
        # print(loc_value)
    else:
        negative = False

    thousanth = int(loc_value * 1000 % 10)
    # print(thousanth)
    if thousanth % 2 == 0:
        abs_ans = int(loc_value * 1000) / 1000
        if negative:
            return -1 * abs_ans
        return abs_ans

    abs_ans = round(loc_value + 0.0005,3)
    # print(abs_ans)
    if negative:
        return -1 * abs_ans
    return abs_ans

def get_stations(row):
    start_station_name = row[4]
    end_station_name = row[6]
    try:
        start_lat = round_coord(float(row[8]))
        start_long = round_coord(float(row[9]))
    except:
        # raise
        return ()

    try:
        end_lat = round_coord(float(row[10]))
        end_long = round_coord(float(row[11]))
    except:
        return ()
    # return (start_lat, start_long, end_lat, end_long), start_name, end_name
    return (start_station_name,start_lat, start_long),(end_station_name,end_lat, end_long)

def add_stations_from_dict(stations):
    c = db_connect()
    try:
        index = 0
        for station in stations.items():
            lat,longitude = station[0]
            name = station[1]
            # if station[0] != '':
            c.execute('INSERT INTO stations VALUES (?,?,?)',(name,lat,longitude))
            index += 1
    except:
        db_close()
        print(station)
        raise
    db_close()

db_table_inits()
# print(get_trip_duration('2022-09-10','00:00:00', '2022-09-10', '12:34:56'))

def faster_get_trip_data(row):
    start_timestamp = row[2].split(' ')
    start_date = start_timestamp[0]
    start_time = start_timestamp[1]

    end_timestamp = row[3].split(' ')
    end_date = end_timestamp[0]
    end_time = end_timestamp[1]
    
    trip_duration = get_trip_duration(start_date, start_time, end_date, end_time)

    start_station_name = row[4]
    end_station_name = row[6]
    is_member = (row[12] == "member")
    # new_row = (trip_duration, start_date, start_time, start_station_name, end_station_name, is_member)
    new_row = (trip_duration, start_date, start_time, is_member)
    # new_row = (trip_duration, start_date, start_time, start_station_lat, \
    # start_station_long, end_station_lat, end_station_long, is_member)
    # print(new_row)
    return new_row

def load_stations_db():
    # stations = set()
    stations = dict()
    # station_names = set()
    # stations_coords = set()     #rounded to the 1000th to avoid duplicates

    # trimmed_data = []
    for filename in FILENAMES:
    # for filename in ['202201-citibike-tripdata.csv',]:
        filename_with_folder = 'data/' + filename
        with open(filename_with_folder) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            info_row = next(csv_reader)
            for row in csv_reader:
                trip_stations = get_stations(row)
                for i in range(len(trip_stations)):
                    station = trip_stations[i]
                    coord = (station[1],station[2])
                    name = station[0]
                    # print(coord)
                    # coords += coord
                    if name == '':

                        break
                    try:
                        # names = stations[coord]
                        # shortest_name = get_shortest_name((stations[coord], name))
                        stations[coord].add(name)
                    except KeyError:
                        stations[coord] = {name,}
                        # stations[coord] = name

            print(f'got data for {filename[:6]}')
            print(f'{len(stations) = }')
    # add_new_trip(trimmed_data)
    # print(trimmed_data)
    print(f'{len(stations) = }')

    coord_to_name = dict()
    coord_to_id = dict()
    index = 1                   # rowid starts at 1
    for coord,names in stations.items():
        # print(pair)
        name = get_shortest_name(names)
        coord_to_name[coord] = name
        coord_to_id[coord] = index
        index += 1
    # print(coord_to_name)
    # # print(coord_to_id)

    add_stations_from_dict(coord_to_name)
    # return coord_to_id


def get_shortest_name(names):
    min_len = 100
    # shortest_name = names[0]
    for name in names:
        try:
            float(name)
        except:
            if len(name) < min_len and '\t' not in name:
                min_len = len(name)
                shortest_name = name
    # return shortest_name.replace('\\t','HELLO')
    return shortest_name.replace('\\t',' ')




if __name__ == '__main__':
    # coord_to_id = load_stations_db()
    load_stations_db()

            



import sqlite3
import csv

FILENAMES = (
    '202102-citibike-tripdata.csv',
    '202103-citibike-tripdata.csv',
    '202104-citibike-tripdata.csv',
    '202105-citibike-tripdata.csv',
    '202106-citibike-tripdata.csv',
    '202107-citibike-tripdata.csv',
    '202108-citibike-tripdata.csv',
    '202109-citibike-tripdata.csv',
    '202110-citibike-tripdata.csv',
    '202111-citibike-tripdata.csv',
    '202112-citibike-tripdata.csv',
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
    '202301-citibike-tripdata.csv',
    '202302-citibike-tripdata.csv',
    '202303-citibike-tripdata.csv',
    '202304-citibike-tripdata.csv',
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
    # c.execute("CREATE TABLE IF NOT EXISTS trips (trip_duration int, start_date string, \
    #     start_time string, is_member bool, start_station_id int,\
    #     end_station_id int)")
    c.execute("CREATE TABLE IF NOT EXISTS trips (trip_duration int, year int, month int,\
    day int, hour int, minute int, is_member bool, start_station_id int,\
        end_station_id int)")
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

db_table_inits()
# print(get_trip_duration('2022-09-10','00:00:00', '2022-09-10', '12:34:56'))


'''trip_duration int, year int, month int,\
    day int, hour int, minute int, is_member bool, start_station_id int,\
        end_station_id int'''
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

    year,month,day = map(int,start_date.split('-'))
    hour,minute,sec = map(int,start_time.split(':'))

    new_row = (trip_duration, year,month,day, hour,minute, is_member)
    # new_row = (trip_duration, start_date, start_time, start_station_name, end_station_name, is_member)
    # new_row = (trip_duration, start_date, start_time, is_member)
    # new_row = (trip_duration, start_date, start_time, start_station_lat, \
    # start_station_long, end_station_lat, end_station_long, is_member)
    # print(new_row)
    return new_row


def load_trips(coord_to_id):
    # stations = set()
    # stations = dict()
    # station_names = set()
    # stations_coords = set()     #rounded to the 1000th to avoid duplicates

    # trimmed_data = []
    for filename in FILENAMES:
    # for filename in ['202201-citibike-tripdata.csv',]:
        trimmed_data = set()
        filename_with_folder = 'data/' + filename
        with open(filename_with_folder) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            info_row = next(csv_reader)
            # index = 0
            for row in csv_reader:
                # if index > 10:
                #     break
                # index += 1
                scrap_trip = False  # if this trip should be ignored
                # for station in get_stations(row):
                coords = ()
                trip_stations = get_stations(row)
                for i in range(len(trip_stations)):
                    station = trip_stations[i]
                    coord = (station[1:])
                    # name = station[0]
                    # print(coord)
                    coords += coord
                    if station[0] == '':
                        scrap_trip = True
                        # print(f'{station}')
                        break
                
                new_row = faster_get_trip_data(row)

                # if new_row[4] != '' and new_row[0] < 60*60*5 and new_row[0] != -1:            # if end station exists
                if not scrap_trip and new_row[0] < 60*60*5 and new_row[0] != -1 and len(coords) == 4:
                    trimmed_data.add(new_row+coords)
                # break

            print(f'got data for {filename[:6]}')
            # print(f'{len(stations) = }')
            print(f'{len(trimmed_data) = }')
        add_trips_with_coords(trimmed_data, coord_to_id)
        # add_new_trip(trimmed_data)
    # print(trimmed_data)
    # print(stations)

#{(266, '2022-01-18', '08:23:52', True, 40.688, -73.991, 40.692, -73.993)}
def add_trips_with_coords(data, coord_to_id):
    c = db_connect()
    # print(start_id)
    try:
        for trip in data:
            # print(trip)
            if len(trip) < 8:
                print(f'{trip = }')
            # start_id = get_station_id(trip[4], trip[5])
            # end_id = get_station_id(trip[6], trip[7])
            start_id = coord_to_id[(trip[-4], trip[-3])]
            end_id = coord_to_id[(trip[-2], trip[-1])]
            # print(f'{type(trip[:4]) = }')
            # print(f'{start_id = }')
            # print(f'{end_id = }')
            rowid = c.execute('INSERT INTO trips VALUES (?,?,?,?,?,?,?,?,?)',(*trip[:-4],start_id,end_id))
    except:
        db_close()
        raise
    db_close()

def get_coord_to_id():
    c = db_connect()
    # print(start_id)
    try:
        stations = tuple(c.execute('SELECT latitude,longitude FROM stations order by rowid ASC'))
    except:
        db_close()
        raise
    db_close()

    coord_to_id = dict()
    index = 1
    for coord in stations:
        # print(index, coord)
        coord_to_id[coord] = index
        index += 1
    return coord_to_id

if __name__ == '__main__':
    coord_to_id = get_coord_to_id()
    load_trips(coord_to_id)
    # get_coord_to_id()
            



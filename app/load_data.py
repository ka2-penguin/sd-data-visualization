import sqlite3
import csv
from datetime import datetime

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
def db_table_inits():
    c = db_connect()

    c.execute("CREATE TABLE IF NOT EXISTS stations (station_name text, \
        latitude float, longitude float)")

    c.execute("CREATE TABLE IF NOT EXISTS trips (trip_duration int, start_date string, \
        start_time string, start_station_id float,\
        end_station_id float, is_member bool)")
    db_close()

'''"tripduration","starttime","stoptime","start station id",
"start station name","start station latitude","start station longitude",
"end station id","end station name","end station latitude",
"end station longitude","bikeid","usertype","birth year","gender"'''


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
    new_row = (trip_duration, start_date, start_time, start_station_name, end_station_name, is_member)
    # print(new_row)
    return new_row

def add_new_trip(trimmed_data):
    c = db_connect()
    try:
        for row in trimmed_data:
            # c.execute('INSERT INTO trips VALUES (?,?,?,?,?,?)',(trip_duration, start_date, start_time, start_station_id, end_station_id, is_member))
            c.execute('INSERT INTO trips VALUES (?,?,?,?,?,?)',row)
    except:
        db_close()
        print(row)
    db_close()

def get_stations(row):
    start_station_name = row[4]
    end_station_name = row[6]
    try:
        start_lat = float(row[8])
        start_long = float(row[9])
    except:
        return ()

    try:
        end_lat = float(row[10])
        end_long = float(row[11])
    except:
        return ()

    return (start_station_name,start_lat, start_long),(end_station_name,end_lat, end_long)

def get_stations_str(row):
    try:
        start_station_id = float(row[5])
        end_station_id = float(row[7])
    except:
        # if row != '':
        #     print(row)
        return ()

    start_station_name = row[4]
    end_station_name = row[6]

    try:
        start_lat = float(row[8])
        start_long = float(row[9])
    except:
        return ()

    try:
        end_lat = float(row[10])
        end_long = float(row[11])
    except:
        return ()

    return (start_station_id,start_station_name,start_lat, start_long),\
    (end_station_id,end_station_name,end_lat, end_long)

def add_stations(stations):
    c = db_connect()
    try:
        for station in stations:
            if station[0] != '':
                c.execute('INSERT INTO stations VALUES (?,?,?)',station)
    except:
    
        db_close()
        print(station)
        raise
        # pass
        # return
    db_close()



db_table_inits()
# print(get_trip_duration('2022-09-10','00:00:00', '2022-09-10', '12:34:56'))

def csv_to_db():
    stations = set()
    station_names = set()

    for filename in FILENAMES:
        filename_with_folder = 'data/' + filename
        with open(filename_with_folder) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            trimmed_data = set()
            info_row = next(csv_reader)
            for row in csv_reader:
                # new_row = faster_get_trip_data(row)
                # if new_row[4] != '' and new_row[0] < 60*60*5 and new_row[0] != -1:            # if end station exists
                #     trimmed_data.add(new_row)

                for station in get_stations(row):
                    if station[0] not in station_names:
                        stations.add(station)
                        station_names.add(station[0])
            print(f'got data for {filename[:6]}')
            print(f'{len(stations) = }')
            # add_new_trip(trimmed_data)
    add_stations(stations)

if __name__ == '__main__':
    csv_to_db()
    # with open('data/202201-citibike-tripdata.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     # trimmed_data = set()
    #     stations = set()
    #     # info_row = next(csv_reader)
    #     line = 0
    #     info_row = next(csv_reader)
    #     for row in csv_reader:
    #         for station in get_stations(row):
    #             stations.add(station)
    #         # if line < 10:
    #             # print(get_stations(row))
    #         line += 1
    # print(f'{len(stations) = }')
    # add_stations(stations)



# with open('202210-citibike-tripdata.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     # print(csv_reader[0])
#     # trimmed_data = []
#     trimmed_data = set()

#     info_row = next(csv_reader)
#     for row in csv_reader:
#         # add_trip_row(row)
#         new_row = faster_get_trip_data(row)
#         if new_row[4] != '' and new_row[0] < 60*60*5 and new_row[0] != -1:            # if end station exists
#             trimmed_data.add(new_row)
#         # add_new_trip(row)
#     add_new_trip(trimmed_data)
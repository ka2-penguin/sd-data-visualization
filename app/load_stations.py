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

    c.execute("CREATE TABLE IF NOT EXISTS stations (station_id text, station_name text, \
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
    return round(loc_value,3)

    # thousanth = int(loc_value * 10000 % 10)
    # # print(thousanth)
    # if thousanth % 2 == 0:
    #     abs_ans = int(loc_value * 10000) / 10000
    #     if negative:
    #         return -1 * abs_ans
    #     return abs_ans

    # abs_ans = round(loc_value + 0.00005,3)
    # # print(abs_ans)
    # if negative:
    #     return -1 * abs_ans
    # return abs_ans


    # thousanth = int(loc_value * 1000 % 10)
    # # print(thousanth)
    # if thousanth % 2 == 0:
    #     abs_ans = int(loc_value * 1000) / 1000
    #     if negative:
    #         return -1 * abs_ans
    #     return abs_ans

    # abs_ans = round(loc_value + 0.0005,3)
    # # print(abs_ans)
    # if negative:
    #     return -1 * abs_ans
    # return abs_ans

def get_stations(row):
    start_station_name = row[4]
    end_station_name = row[6]
    try:
        start_lat = float(row[8])
        start_long = float(row[9])
    except:
        # raise
        return ()

    try:
        end_lat = float(row[10])
        end_long = float(row[11])
    except:
        return ()

    # start_lat = round_coord(float(row[8]))
    # start_long = round_coord(float(row[9]))
    # end_lat = round_coord(float(row[10]))
    # end_long = round_coord(float(row[11]))

    # return (start_lat, start_long, end_lat, end_long), start_name, end_name
    return (start_station_name,start_lat, start_long),(end_station_name,end_lat, end_long)

def add_stations_from_list(stations):
    c = db_connect()
    try:
        # index = 0
        for station in stations:
            # lat,longitude = station[0]
            # name = station[1]
            # if station[0] != '':
            c.execute('INSERT INTO stations VALUES (?,?,?,?)',station)
            # index += 1
    except:
        db_close()
        print(station)
        raise
    db_close()

db_table_inits()
# print(get_trip_duration('2022-09-10','00:00:00', '2022-09-10', '12:34:56'))

'''
ride_id,rideable_type,started_at,ended_at,start_station_name,start_station_id,\
end_station_name,end_station_id,start_lat,start_lng,end_lat,end_lng,member_casual
'''

def load_stations_db():
    # stations = set()
    # stations = dict()
    station_ids = set()
    id_to_name = dict()     # {id: [name1, name2, ...], }
    id_to_coord = dict()    # {id: latest_coord, }
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

                ids = (row[5],row[7])
                # start_station_id = row[5]
                # end_station_id = row[7]
                # station_ids.add(start_station_id)
                # station_ids.add(end_station_id)

                for i in range(len(trip_stations)):
                    station = trip_stations[i]
                    coord = (station[1],station[2])
                    name = station[0]
                    id = ids[i]
                    id_to_coord[id] = coord

                    station_ids.add(id)
                    # if 'SYS' not in id:
                    #     break
                    # print(coord)
                    # coords += coord
                    if name == '':# or name[0].isalpha():
                        continue
                    try:
                        # names = stations[coord]
                        # shortest_name = get_shortest_name((stations[coord], name))
                        id_to_name[id].add(name)
                    except KeyError:
                        id_to_name[id] = {name,}
                        # stations[coord] = {name,}
                        # stations[coord] = name

            print(f'got data for {filename[:6]}')
            # print(f'{len(stations) = }')
            print(f'{len(station_ids) = }')
            print(f'{len(id_to_name) = }')

    # print(f'{station_ids = }')
    # print(f'{len(stations) = }')
    # print(f'{len(station_ids) = }')
    print(f'{len(id_to_name) = }')

    # custom_id = 1
    # coord_to_name = dict()
    stations_data = []
    for id,names in id_to_name.items():
        name = get_shortest_name(names)
        lat,lng = id_to_coord[id]

        station_info = (id, name, lat, lng)
        stations_data.append(station_info)
        # coord_to_name[id_to_coord[id]] = name
    print(stations_data[10])
    add_stations_from_list(stations_data)

    # add_stations_from_dict(coord_to_name)
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

            



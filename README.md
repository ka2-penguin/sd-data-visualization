# sd-data-visualization by PTSD

## See our app live here: https://white-space.live

## Description
This app lets the user search for Citibike trips in 2022 and displays them on a map.
The user can click one of the dots on the map to get the station's id.


## How to run on your local machine
1. Clone this repo
1. Get the requirements

### How to get the data and load it on the database
After running `load_stations.py`
and `load_trips.py` the app doesn't need the `.zip` or `.csv`
 files so feel free to delete them.

1. `cd` into the repo
1. Run `source get_raw_data.sh`
1. Then `cd app/`
1. Run `python3 load_stations.py`
1. Run `python3 load_trips.py`

### How to run the app
1. `cd` into `app/`
1. Run `python3 __init__.py`
1. Go to http://127.0.0.1:8000/ in your favorite browser.

## Data
### Description
This data is originally a csv with data on every Citi Bike trip in 2022
 over a minute.
 It has info on:

    Ride ID
    Rideable type
    Started at
    Ended at
    Start station name
    Start station ID
    End station name
    End station ID
    Start latitude
    Start longitude
    End latitude
    End Longitude
    Member or casual ride


 More info [here](https://citibikenyc.com/system-data) 
    
 The database only has a table `trips` with info on the start date, time, custom station IDs for the start and end stations and a `stations` table with info on the corresponding name and 

### Source: https://s3.amazonaws.com/tripdata/index.html

## APIs
* [Google Maps API](https://github.com/stuy-softdev/notes-and-code/blob/main/api_kb/411_on_Google_Maps_Platform.md)

## Roles
Droplet - Joseph  
Flask - Maya, Daniel  
SQLite3 loading data - Maya  
Reading data - Daniel,Maya  
FEF (Bootstrap) - Joseph  
CSS - Joseph  
HTML - Joseph  
Station markers - Maya  
APIs (Google Map API) - Daniel  
JS for chart - Joseph  

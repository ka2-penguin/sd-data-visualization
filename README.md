# sd-data-visualization by PTSD

## See our app live here: https://white-space.live

## How to run on your local machine
1. Clone this repo
1. Get the requirements

### How to get the data and load it on the database
Note: `data.db` will be over 2 GB and the `.zip` and `.csv`
files will be around 14 GB. After running `load_stations.py`
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
1. Go to http://127.0.0.1:5000/ in your favorite browser.

## Roles
Droplet - Maya  
Flask - Maya  
SQLite3, reading and loading data - Maya  
FEF (Bootstrap) - Daniel  
CSS - Daniel  
HTML - Daniel  
Map - Daniel/Joseph  
APIs (OpenStreetMap API) - Joseph  
JS (with d3.js) - Joseph  

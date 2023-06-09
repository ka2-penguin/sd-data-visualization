from flask import Flask, render_template, session, request, redirect, jsonify, url_for
import json
import read_data
# import load_stations
from load_key import load_key

app = Flask(__name__)
search_results = []

api_key = load_key()
# print(f'{api_key = }')

@app.route('/', methods=["GET","POST"])
def root(results=[], text="hello there"):
    global search_results 
    filters = ""
    print("before post method")
    if request.method == "POST":
        print("got post method")
        filters = request.get_json()
        search_results = read_data.get_trips(filters)
        return redirect('/trip-search-results')
    print(text)
    return render_template("index.html",results=results,text=text,key=api_key)

@app.route('/trip-search-results', methods=["GET","POST"])
def got_form():
    display_search_results = prettier_results(search_results)
    csv_coords_list = read_data.get_csv_coords_list(search_results)
    return render_template("results.html", results=display_search_results, option_values=csv_coords_list, key=api_key)

    
def prettier_results(data):
    new_data = []
    for row in data:
        date = f'{row[1]}-{row[2]}'
        time = f'{row[3]}:{row[4]}'
        if row[5] == 1:
            user_type = 'member'
        else:
            user_type = 'casual'
        time_string = ''
        if row[0] >= 3600:
            time_string += str(row[0] // 3600) + ' hr '
        if row[0] >= 60:
            time_string += str((row[0] % 3600) // 60) + ' min '
        time_string += str(row[0]%60) + ' sec ' 
        new_data.append(f'{user_type}, rode on {date} {time} for {time_string} from station {row[6]} to station {row[7]}')
    return new_data

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    # TEMPLATES_AUTO_RELOAD = True
    # app.config["TEMPLATES_AUTO_RELOAD"] = True

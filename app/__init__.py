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
        filters = request.get_json()
        search_results = read_data.get_trips(filters)
        return redirect('/trip-search-results')
    print(text)
    return render_template("index.html",results=results,text=text,key=api_key)

@app.route('/trip-search-results', methods=["GET","POST"])
def got_form():
    display_search_results = prettier_results(search_results)
    csv_coords_list = read_data.get_csv_coords_list(search_results)
    return render_template("results.html", results=display_search_results,option_values=csv_coords_list,key=api_key)

    # return render_template("index2.html", results=search_results,text=sample_text)

@app.route("/query.json", methods=["GET", "POST"])
def query(): 
    if request.method == "POST":
        with open("query.json", 'w') as f:
            data = request.get_data(as_text=True)
            f.write(str(data))
            f.close()
            print("writen data:")
            print(data)

    with open("query.json", 'r') as f:
        data = json.load(f)
        f.close()
        print("read data:")
        print(data)
        return jsonify(data)
    
def prettier_results(data):
    new_data = []
    for row in data:
        date = f'{row[1]}-{row[2]}'
        time = f'{row[3]}:{row[4]}'
        if row[5] == 1:
            user_type = 'member'
        else:
            user_type = 'casual'
        new_data.append(f'{row[0]} {date} {time} {user_type} {row[6]} {row[7]}')
    return new_data

if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
    # TEMPLATES_AUTO_RELOAD = True
    # app.config["TEMPLATES_AUTO_RELOAD"] = True

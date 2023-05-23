from flask import Flask, render_template, session, request, redirect, jsonify, url_for
import json
import read_data
# import load_stations

app = Flask(__name__)
search_results = []
sample_text = "not changed"

@app.route('/', methods=["GET","POST"])
def root(results=[], text="hello there"):
    global search_results 
    global sample_text
    filters = ""
    print("before post method")
    if request.method == "POST":
        print("got the post method")
        filters = request.get_json()
        print(type(filters))
        print(filters)
        search_results = read_data.get_trips(filters)

        sample_text = "post request"
        return redirect('/trip-search-results')
    print(text)
    return render_template("index.html",results=results,text=text)

@app.route('/trip-search-results', methods=["GET","POST"])
def got_form():
    print("in got_form")
    print(f'{search_results[0] = }')
    print(f'{sample_text = }')
    display_search_results = prettier_results(search_results)
    csv_coords_list = read_data.get_csv_coords_list(search_results)
    return render_template("results.html", results=display_search_results,option_values=csv_coords_list)

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

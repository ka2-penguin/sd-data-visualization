from flask import Flask, render_template, session, request, redirect, jsonify, url_for
import json
import read_data
# import load_stations

app = Flask(__name__)
search_results = []
sample_text = "not changed"

@app.route('/', methods=["GET","POST"])
def root(results=[],text="hello there"):
    global search_results 
    global sample_text
    filters = ""
    # results = []
    # text="hello there"
    print("before post method")
    if request.method == "POST":
        print("got the post method")
        filters = request.get_json()
        print(type(filters))
        print(filters)
        search_results = read_data.get_trips(filters)
        sample_text = "post request"
        # print(results)
        # print('going to render_template')
        # return got_form(results,text)
        # return redirect(url_for("got_form"))
        return redirect('/trip-search-results')

    #     return render_template("index.html", results=results,text=text)
    print(text)
    return render_template("index.html",results=results,text=text)

@app.route('/trip-search-results', methods=["GET","POST"])
def got_form():
    # filters = ""
    # results = []
    # text="hello there"
    # print("before post method")

    print("in got_form")
    # filters = request.get_json()
    # print(type(filters))
    # print(filters)
    # results = read_data.get_trips(filters)
    # text = "post request"
    # print(results)
    # print('going to render_template')

    # return root(results,text)
    print(f'{search_results[0] = }')
    print(f'{sample_text = }')


    return render_template("index2.html", results=search_results,text=sample_text)

@app.route("/query.json", methods=["GET", "POST"])
def query():
    #collect all data necessary to display map
    # info = request.form["query"].split(",")
    # data = {
    #     "trip_duration": info[0],
    #     "start_date": info[1],
    #     "start_time": info[2],
    #     "is_member": info[3],
    #     "start_station_id": info[4],
    #     "end_station_id": info[5],
    # }
    
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

if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
    # TEMPLATES_AUTO_RELOAD = True
    # app.config["TEMPLATES_AUTO_RELOAD"] = True

from flask import Flask, render_template, session, request, redirect, jsonify
import json
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')

@app.route('/query.json', methods=['GET', 'POST'])
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
    
    if request.method == 'POST':
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

if __name__ == '__main__':
    app.debug = True
    app.run(port=8000)
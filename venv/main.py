from flask import *
from data_tester import *
import json


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main_route():
    if (request.method == "GET"):
        return "HEY!"
    if (request.method == "POST"):
        print("POST REQUEST STARTED")
        data = request.json
        if not data['age']:
            data['age'] = 21
        if not data['height']:
            data['height'] = 170
        if not data['weight']:
            data['weight'] = 60
        if not data['gender']:
            data['gender'] = 'Male'
        result = {
                'Age' : data['age'],
                'Height' : data['height'],
                'Weight' : data['weight'],
                'Gender' : data['gender'],
        }
        data = [[d['t'] * 1000 + i, d['x'], d['y'], d['z']] for i, d in enumerate(data['results'])]
        verdict = predict_falling(result, data)
        if type(verdict) is not str:
            verdict = verdict[0]
        res = jsonify({"fallen":str(verdict)})
        print(res)
        return res

app.run(host= '0.0.0.0', port="5000")

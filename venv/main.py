from flask import *
from data_tester import *
import json


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main_route():
    print("I HAVE RECEIVED A ROUTE REQUEST")
    if (request.method == "GET"):
        return "HEY!"
    if (request.method == "POST"):
        print('OK!!!')
        data = request.json
        result = {
                'Age' : data['age'],
                'Height' : data['height'],
                'Weight' : data['weight'],
                'Gender' : data['gender'],
        }
        data = [[d['t'], d['x'], d['y'], d['z']] for d in data['results']]
        verdict = predict_falling(result, data)
        return jsonify({'fallen':verdict})

print('STARTING!')
app.run(host= '0.0.0.0', port="5000")

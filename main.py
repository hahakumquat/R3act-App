from flask import *
from data_tester import *
import json


app = Flask(__name__)

@app.route('/get', methods=['POST', 'GET'])
def main_route():
    if (request.method == "POST"):
        data = request.json
        result = {
                'Age' : data['age'],
                'Height' : data['height'],
                'Weight' : data['weight'],
                'Gender' : data['gender'],
        }
        data = [[d['t'], d['x'], d['y'], d['z']] for d in data['results']]
        verdict = predict_falling(result, data, True)
        return jsonify({'fallen':verdict})

from flask import *
from extensions import mysql

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['POST', 'GET'])
def main_route():
	if (request.method == "POST"):
		content = request.get_json()
		# {
		# 	"results":
		# 	[
		# 	{
		# 		"t": time, 
		# 		"x": x, 
		# 		"y": y, 
		# 		"z":z,
		# 	},
		# 	]
		# }
		data = content["results"]
		x = 0
		y = 0
		z = 0
		for dataPoint in data:
			x = dataPoint["x"]
			y = dataPoint["y"]
			t = dataPoint["t"]

		fallen = False
		if (y > 5):
			fallen = True

		return jsonify(fallen=fallen)
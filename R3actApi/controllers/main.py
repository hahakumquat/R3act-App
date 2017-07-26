from flask import *
from extensions import mysql
import data_tester

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['POST', 'GET'])
def main_route():
	if (request.method == "POST"):
		content = request.get_json()
		# {
		# 	"results":
		# 	[[t,x,y,z],[t,x,y,z]]
		# }
		data = content["results"]
		# x = 0
		# y = 0
		# z = 0
		verdict = predict_falling(dataPoint)
		# for dataPoint in data:
		# 	t = dataPoint[0]
		# 	x = dataPoint[1]
		# 	y = dataPoint[2]
		# 	z = dataPoint[3]
			# print dataPoint
			#predict_falling(dataPoint)

		return jsonify(fallen=verdict)
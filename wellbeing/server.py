from mds import k_mds

from flask import Flask, Response
from flask_cors import CORS, cross_origin

import random
import json
import csv

import numpy as np


app = Flask(__name__)
CORS(app)

distances = np.loadtxt('distances')
details = []

dimensions = ['education','jobs','income','safety','health','environment','civic engagement','accessiblity to services','housing','community','life satisfaction']

with open('wellbeingdata.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for i, row in enumerate(reader):
		row['id'] = i
		for d in dimensions:
			if row[d] != '..':
				row[d] = float(row[d].replace(',','.'))
			else:
				row[d] = 0
		details.append(row)

@app.route('/<int:focus_id>/<int:k>')
def do_mds(focus_id, k):
    ids, coordinates = k_mds(distances, focus_id, k)
    result_details = [details[id] for id in ids]
    result = {'details': result_details, 'order': ids.tolist(), 'coordinates': coordinates.tolist() }
    return Response(json.dumps(result),  mimetype='application/json')

if __name__ == "__main__":
    app.run()

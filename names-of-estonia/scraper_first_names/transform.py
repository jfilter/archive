import json

import csv
with open('results.csv', 'w') as csvfile:
	write = csv.writer(csvfile, delimiter=',')
	write.writerow(['name', 'n'])

	with open('results.json') as json_data:
		d = json.load(json_data)

		dd = {}

		for key in d.keys():

			if int(d[key]) > 5:

				t = key.title();
				if not t in dd:
					dd[t] = d[key]

		for key in dd.keys():
				write.writerow([key, dd[key]])
import csv
import numpy as np

dimensions = ['Education','Jobs','Income','Safety','Health','Environment','Civic engagement','Accessiblity to services','Housing','Community','Life satisfaction']

data = []

with open('wellbeingdata.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		for d in dimensions:
			if row[d] != '..':
				row[d] = float(row[d].replace(',','.'))
			else:
				row[d] = 0
		data.append(row)

n = len(data)
distances = np.zeros((n, n))

print(distances)

for i, element_1 in enumerate(data):
	for ii, element_2 in enumerate(data):
		d = sum( [ (element_1[dimension] - element_2[dimension]) ** 2 for dimension in dimensions ]) ** 1/2.0
		distances[ii][i] = d

			

# for x in zip(*distances):
# 	print(x)


# for i in range(n):
# 	for ii in range(n):
# 		if i == ii:
# 			print(i, ii, distances[i][ii])

np.savetxt('distances', distances)

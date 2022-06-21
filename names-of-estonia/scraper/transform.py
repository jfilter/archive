import csv
import json

data = []
names = set()

with open('results.csv') as file:
    reader = csv.reader(file)
    i = 0
    for row in reader:
        if row[0].replace('ı', 'i') not in names:
            names.add(row[0].replace('ı', 'i'))
            count = 0
            if(row[1] != ""):
                if(row[1] == "4"):
                    row[1] = 'under 5'
                else:
                    count += int(row[1])
                    # row[1] = int(row[1])
            else:
                row[1] = "0"
            if(row[2] != ""):
                if(row[2] == "4"):
                    row[2] = 'under 5'
                else:
                    count += int(row[2])
                    # row[2] = int(row[2])
            else:
                row[2] = "0"
            # if count > 0:
            row.append(str(count))
            data.append(row)


data = sorted(data, key=lambda x: int(x[3]), reverse=True)

i = 0
while i < len(data):
    rank = i + 1
    if i > 0 and data[i][3] == data[i - 1][3]:
        rank = data[i - 1][4]
    data[i].append(rank)
    i += 1


with open("../html/app/assets/data.json", "w") as outfile:
    json.dump(data, outfile)

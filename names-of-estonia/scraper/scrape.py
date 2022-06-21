import requests
import csv
from lxml import html

BASE_URL = "http://www.stat.ee/public/apps/nimed/%s"
data = []


def proccesName(name):
    url = BASE_URL % name
    r = requests.get(url)
    if r.status_code != 200:
        print('error with %s' % name)
    else:
        success, women, men = parseText(r.text)
        if success:
            data.append({'name': name.title(), 'women': women, 'men': men})
            # print(data)


def parseText(text):
    tree = html.fromstring(text)
    elements = tree.xpath('.//div[contains(@class, "item")]/meta/@content')

    # print(elements)

    if len(elements) == 0:
        return False, None, None

    t = elements[0]
    women_number = None
    men_number = None

    women = t.find('naisel')
    if women != -1:
        women_end = women - 1
        women_start = t.rfind(' ', 0, women_end) + 1
        women_string = t[women_start:women_end]
        if women_string == 'viiel':
            women_number = 4
        else:
            women_number = int(women_string)

    men = t.find('mehel')
    if men != -1:
        men_end = men - 1
        men_start = t.rfind(' ', 0, men_end) + 1
        men_string = t[men_start:men_end]
        if men_string == 'viiel':
            men_number = 4
        else:
            men_number = int(men_string)

    return True, women_number, men_number

with open('uniquefirstnames.csv') as file:
    reader = csv.reader(file)
    i = 0
    for row in reader:
        print(i)
        i += 1
        proccesName(row[0])

with open('results.csv', 'w') as csvfile:
    fieldnames = ['name', 'women', 'men']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

import requests

# {
#   __schema {
#     types {
#       name
#     }
#   }
# }
QUERY_SCHEMA = "https://api.datengui.de/?query=%7B%0A%20%20__schema%20%7B%0A%20%20%20%20types%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D"

# {
#   regions {
#     id
#     name
#   }
# }
QUERY_REGIONS = "https://api.datengui.de/?query=%7B%0A%20%20regions%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%7D%0A%7D"

QUERY_BASE_SINGLE_REGION = "https://api.datengui.de/?query={region(id:\"%s\"){id name %s}}"
QUERY_BASE_REGIONS = "https://api.datengui.de/?query={regions(%s){id name %s}}"


QUERY_AVAILABLE_YEARS = """https://api.datengui.de/?query={
  __type(name: "%s")
    {
    fields {
      name
    }
  }
}"""


def fetch_all_timebased_data_set_names():
    """returns only the data sets that are time-based (have years)"""
    r = requests.get(QUERY_SCHEMA)
    data = r.json()

    all_types = data['data']['__schema']['types']

    # only select time-based data
    candidates = [x['name']
                  for x in all_types if x['name'].endswith('__years')]

    return candidates


def fetch_all_regions():
    r = requests.get(QUERY_REGIONS)
    data = r.json()

    return data['data']['regions']


def fetch_avaiable_years(string):
    """return the years for which data exists"""
    r = requests.get(QUERY_AVAILABLE_YEARS % string)
    data = r.json()

    return [x['name'] for x in data['data']['__type']['fields']]

def build_query_object(string):
    string_as_list = string.split('__')

    string_as_list = string_as_list[1:]  # remove 'region'
    first = string_as_list[-2] + '__' + string_as_list[-1]  # remo

    first += '{' + ' '.join(fetch_avaiable_years(string)) + '}'

    string_as_list.pop()  # remove last one
    string_as_list.pop()  # remove last one

    if len(string_as_list) == 0:
        return first

    res = first
    for x in reversed(string_as_list):
        res = x + '{' + res + '}'

    return res


def fetch_data_single_region(id, data_set_string):
    object_string = build_query_object(data_set_string)

    url = QUERY_BASE_SINGLE_REGION % (id, object_string)

    r = requests.get(url)
    data = r.json()

    return data

def fetch_data_regions(regions_filter, data_set_string):
    object_string = build_query_object(data_set_string)

    url = QUERY_BASE_REGIONS % (regions_filter, object_string)

    r = requests.get(url)
    data = r.json()

    return data    
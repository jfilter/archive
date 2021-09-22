import random

from .fetch import fetch_all_timebased_data_set_names, fetch_data_regions

random.seed()

def two_random_data(region_filter):
    all_data = fetch_all_timebased_data_set_names()

    data = fetch_data_regions(region_filter, random.sample(all_data, 1)[0])

    return random.sample(data['data']['regions'], 2)
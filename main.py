from help.api import MapBoxService
from help.data import EventData
from help.tool import Timex

import pandas as pd

## Loading in the API so we can do requests later
with open(file='ors_token.txt', mode='r') as file:
    keys = file.readlines()
mbs_api = MapBoxService(api_key=keys[1])

## Load the API and run it
w = Timex(mbs_api=mbs_api)
w.run()

'''
raw_data = pd.read_csv('case_data.csv')
print(raw_data)

event_data = EventData(data=raw_data, mbs_api=mbs_api)
event_data.data.to_csv('case_event_data.csv')

event_data.get_possible_combinations()

routing_data = event_data.get_possible_routes(include_historical_traffic=True)
routing_data.to_csv('case_routing_data.csv')

ranking_data = event_data.get_ranking()
ranking_data.to_csv('case_ranking_data.csv')
'''

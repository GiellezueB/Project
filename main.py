from help.api import MapBoxService
from help.tool import Timex

import pandas as pd

## Loading in the API so we can do requests later
with open(file='ors_token.txt', mode='r') as file:
    keys = file.readlines()
mbs_api = MapBoxService(api_key=keys[1])

## Load the API and run it
w = Timex(mbs_api=mbs_api)
w.run()
import itertools
import numpy as np
import pandas as pd
from scipy.stats import skewnorm
import matplotlib.pyplot as plt

class EventData():
    def __init__(self, data: pd.DataFrame, mbs_api, inlcude_uncertainty=False, include_traffic_history=True) -> None:
        self.data = data
        self.columns = self.data.columns
        
        self.include_uncertainty = inlcude_uncertainty
        self.include_traffic_history = include_traffic_history

        self.mbs_api = mbs_api

        self.routing_data = None
        self.possible_combinations_idx = None
        self.possible_combations = None

        self.process_data()

    def process_data(self) -> None:
        # Convert timestamp to Pandas timestamp for easier computations
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])

        # Get geodata first so we can drop events without a valid output
        self.data['location_coords'] = self.data['location'].apply(lambda x: self.mbs_api.get_geocode(text=x))
        
        # Sort data by timestamp to have character indices in alphabetical and chronological order
        self.data = self.data.sort_values('timestamp')

        # Change index to characters
        self.data.index = [chr(ord('a') + i) for i in range(len(self.data))]

        # Change column order
        self.data = self.data[['method', 'timestamp', 'location', 'location_coords', 'transportmode', 'confirmed']]
        
        # Drop NA
        self.data = self.data.dropna(subset=['timestamp', 'location'])

    def get_possible_routes(self, age, include_historical_traffic: bool) -> pd.DataFrame:       
        # Shortcut to get a two-column dataframe, with all combinations of size two of all the events
        pairs = list(itertools.combinations(self.data.index, 2))
        possible_routes = pd.DataFrame(zip(*pairs)).T
        possible_routes = possible_routes.rename(columns= {0: 'start_event', 1: 'end_event'})

        # After getting all the possible routes, we merge it with the original data to get all corresponding coordinates
        possible_routes = pd.merge(possible_routes, self.data.add_prefix('start_'), how='left', left_on='start_event', right_index=True)
        possible_routes = pd.merge(possible_routes, self.data.add_prefix('end_'), how='left', left_on='end_event', right_index=True)

        # Based on the sightings we can get the difference between the start and end timestamp to get a suspected 'speed'
        possible_routes['duration'] = (possible_routes['end_timestamp'] - possible_routes['start_timestamp']).dt.total_seconds()

        # This is where we get the data from the MapBox API. We have to provide a starting coordinate, end coordinate, mode of transportation and the timestamp (in the case of driving mode)
        possible_routes['directions'] = possible_routes.apply(lambda x: self.mbs_api.get_directions(start=x['start_location_coords'], 
                                                                                                    end=x['end_location_coords'],
                                                                                                    mode=x['end_transportmode'],
                                                                                                    include_historical_traffic=include_historical_traffic,
                                                                                                    timestamp=x['start_timestamp']), axis=1)
        possible_routes.dropna(subset='directions')
        
        # This is where we grab the distance between point A and point B, as given by Mapbox.
        possible_routes['distance_api'] = possible_routes['directions'].apply(lambda x: x['routes'][0]['distance'])
        possible_routes['duration_api'] = possible_routes['directions'].apply(lambda x: x['routes'][0]['duration'])

        # From the distance computed by the APi and the difference between the start and end timestamp we can get an average speed
        possible_routes['speed'] = possible_routes['distance_api'] / possible_routes['duration']
        possible_routes['speed_api'] = possible_routes['distance_api'] / possible_routes['duration_api']
        
        ## Assigning probabilities
        possible_routes['probability'] = possible_routes.apply(lambda x: self.get_probability(speed = x['speed'],
                                                                                              age = age,
                                                                                              speed_api = x['speed_api'],
                                                                                              mode = x['end_transportmode']), axis=1)

        # We can remove some columns that we do not care about anymore
        self.routing_data = possible_routes[['start_event', 'start_timestamp', 'start_location', 
                                             'end_event', 'end_timestamp', 'end_location', 'end_transportmode', 
                                             'duration', 'speed', 
                                             'distance_api', 'duration_api', 'speed_api',
                                             'probability']]
        return self.routing_data
    
    def get_possible_combinations(self, include = [], min_length = 2) -> list[list[str]]:
        # Start with empty list
        c = [[]]
        
        # If we include the 'confirmed' locations, we add those together with any other included points, 
        # if not, we do only the included points (can be empty)
        include.extend(list(self.data[self.data['confirmed'] == 'Yes'].index))

        for idx in self.data.index:
            # Nifty little code to get all possible combinations in order
            c = c + [r+[idx] for r in c]

        if len(include) > 0:
            # If we have any positions that have to be present in any combination, we check for those here.
            c = [x for x in c if set(include).issubset(x)]
        
        # We only keep the combinations that have the minimum required length, standard 
        self.possible_combinations_idx = [x for x in c if len(x) >= min_length]
        return self.possible_combinations_idx
    
    def get_ranking(self) -> pd.DataFrame:
        def transform_to_timeline(data: pd.DataFrame) -> pd.DataFrame:
            data_shifted = data.shift(-1).add_prefix('end_')
            temp = pd.concat([data.add_prefix('start_'), data_shifted], axis=1)    
            temp = temp.rename(columns={'timestamp': 'start_timestamp', 'location': 'start_location'})
            temp = temp.dropna(subset=['end_timestamp', 'end_location']) 
            temp = temp[['start_timestamp', 'start_location', 'end_timestamp', 'end_location']]
            return temp
            
        prim_key = ['start_timestamp', 'start_location', 'end_timestamp', 'end_location']
        df_all_combinations = list()

        for combination in self.possible_combinations_idx:
            # Filter data to hash
            data_combination = self.data.loc[combination]
            route_name = "".join(combination)
            
            # Transform data to timeline structure
            data_timeline = transform_to_timeline(data_combination)
            
            # Get the duration and distance from pre-computed times
            data_timeline = data_timeline.set_index(prim_key).join(self.routing_data.set_index(prim_key), how='left').reset_index()
            
            # Take the average probabilities
            prob = np.mean(data_timeline['probability'])
            
            df_all_combinations.append((route_name, len(combination), prob))
            
        self.ranking = pd.DataFrame(df_all_combinations, columns=['combination', 'combination_len', 'probability']).sort_values(['probability', 'combination_len'], ascending=False)
        return self.ranking
    
    def get_probability(self, speed: float, age: int, speed_api: float, mode: str) -> float:
        if speed == 0:
            return 1
        elif mode == 'On foot':
            if age < 30:
                mu = 1.34
                std = 0.12
            elif 30 < age < 49:
                mu = 1.26
                std = 0.12
            elif 50 < age < 59:
                mu = 1.23
                std = 0.11
            else:
                mu = 1.21
                std = 0.11     
        elif mode == 'By bike':
            mu = 4.37
            std = 2.06
        elif mode == 'By car':
            mu = speed_api
            std = 0.7 * mu
        else:
            return 0.5

        dist = skewnorm(a=-1, loc=mu, scale=std)
        max_val = max(dist.pdf(np.linspace(mu-std, mu+std, 100)))
        return dist.pdf(speed) / max_val

if __name__ == '__main__':
    pass
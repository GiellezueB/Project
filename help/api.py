import requests
import time
import folium
import openrouteservice
from openrouteservice import convert
import numpy as np

class MapBoxService():
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'}

    def get_geocode(self, text):
        url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json?access_token={}'.format(
            text,
            self.api_key
        )
        req = requests.get(url=url, headers=self.headers)
        
        if (req.status_code == 200):
            req_data = req.json()
            coords = req_data['features'][0]['geometry']['coordinates']
            return coords

        print('Directions response status : ', req.status_code, req.reason, text)
        
    def get_directions(self, start, end, mode, include_historical_traffic,timestamp = None):
        try:
            if mode == 'On foot':
                url = 'https://api.mapbox.com/directions/v5/mapbox/walking/{},{};{},{}?access_token={}'.format(
                    start[0], start[1],
                    end[0], end[1],
                    self.api_key)
            elif mode == 'By bike':
                url = 'https://api.mapbox.com/directions/v5/mapbox/cycling/{},{};{},{}?access_token={}'.format(
                    start[0], start[1],
                    end[0], end[1],
                    self.api_key)
            elif mode == 'By car':
                timestamp_iso = timestamp.strftime('%Y-%m-%dT%H:%M')
                if include_historical_traffic:
                    url = 'https://api.mapbox.com/directions/v5/mapbox/driving-traffic/{},{};{},{}?access_token={}&depart_at={}'.format(
                        start[0], start[1],
                        end[0], end[1],
                        self.api_key,
                        timestamp_iso)
                else:
                    url = 'https://api.mapbox.com/directions/v5/mapbox/driving-traffic/{},{};{},{}?access_token={}&depart_at={}'.format(
                        start[0], start[1],
                        end[0], end[1],
                        self.api_key,
                        timestamp_iso)

            req = requests.get(url=url, headers=self.headers)
        except UnboundLocalError:
            print(start, end, mode, timestamp)
            return None
            
        if (req.status_code == 200):
            req_data = req.json()

            return req_data
                
    def plot_directions(self, coords, timestamps, locations, events, filename):
        client = openrouteservice.Client(key='5b3ce3597851110001cf6248e71bc6969df240ac8acdc15daf25a457')
        res = client.directions(coords)
        geometry = client.directions(coords)['routes'][0]['geometry']
        decoded = convert.decode_polyline(geometry)

        distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
        duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
        center = [np.mean([x[1] for x in coords]), np.mean([x[0] for x in coords])]
        
        m = folium.Map(location=center, zoom_start=10, control_scale=True,tiles="cartodbpositron")
        folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(m)

        for idx, coord in enumerate(coords):
            location_txt = "<h4> <b>Location :&nbsp" + "<strong>"+ locations[idx] +" Km </strong>" +"</h4></b>"
            timestamp_txt = "<h4> <b>Timestamp :&nbsp" + "<strong>"+ str(timestamps[idx]) +" Mins. </strong>" +"</h4></b>"
            event_txt = "<h4> <b>event :&nbsp" + "<strong>"+ str(events[idx]) +"</strong>" +"</h4></b>"
            
            popup = folium.Popup(
                location_txt + timestamp_txt + event_txt,
                max_width=300)
            
            folium.Marker(
                location=coord[::-1],
                icon=folium.Icon(color="green"),
                popup=popup
            ).add_to(m)
        
        m.save(filename)
        
if __name__ == "__main__":
    pass
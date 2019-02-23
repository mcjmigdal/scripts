import csv
from collections import Counter
from sys import argv
from geopy.geocoders import Nominatim
import folium
import pandas as pd

geolocator = Nominatim(user_agent="make_fancy_map")

plik = argv[1]
idx_panstwa = int(argv[2])
with open(plik) as handle:
    reader = csv.reader(handle, delimiter='\t', quoting=csv.QUOTE_NONE)
    panstwa = [row for row in reader]
    panstwa = panstwa[1:]
panstwa = [p[idx_panstwa] for p in panstwa]
panstwa = [p for p in panstwa if len(p) > 0]
print panstwa
panstwa = Counter(panstwa)
panstwa_lokalizacje = [geolocator.geocode(p) for p in panstwa.keys()]
panstwa_latitude = [p.latitude for p in panstwa_lokalizacje]
panstwa_longitude = [p.longitude for p in panstwa_lokalizacje]
panstwa_name = panstwa.keys()
panstwa_value = [min(30,p*2) for p in panstwa.values()] # scale values
print panstwa_value

data = pd.DataFrame({
    'lat': panstwa_longitude,
    'lon': panstwa_latitude,
    'name': panstwa_name,
    'value': panstwa_value
})

m = folium.Map(location=[20,0], tiles="Mapbox Bright", zoom_start=2)

for i in range(0,len(data)):
   folium.Circle(
      location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
      popup=data.iloc[i]['name'],
      radius=data.iloc[i]['value']*10000,
      color='crimson',
      fill=True,
      fill_color='crimson'
   ).add_to(m)

# Save it as html
m.save('mymap.html')


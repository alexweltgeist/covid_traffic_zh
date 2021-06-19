# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 09:19:29 2021

@author: alex
"""
# !pip install gmaps
# !pip install plotly==4.14.3

import os
import pandas as pd
import numpy as np

import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.io import orca

pio.renderers.default='browser'    # pio.renderers?  choose: 'browser' or 'svg'
# svg fucked up: orca missing - needs to be reistalled propoerly (some path is wrong)
print(plotly.__version__)

path_to_file = os.getcwd()

df = px.data.election()
geojson = px.data.election_geojson()

fig = px.choropleth_mapbox(df, geojson=geojson, color="Bergeron",
                           locations="district", featureidkey="properties.district",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron", zoom=9)


fig.show()

fig.(path_to_file + '/test.html')

'''
# if data is stored in a csv the path needs to be added in the config file:
    
C:\users\alex\anaconda3\lib\site-packages\gmaps\datasets\datasets.py

"PROJECT_NAME": {
        "url": "YOUR_PUBLIC_URL_OF_.CSV_FILE",
        "description": "ANY_DESCRIPTION_YOU_WANT",
        "source": "YOUR_WEBSITE",
        "headers": ["latitude", "longitude"],
        "types": [float, float]
    },
'''



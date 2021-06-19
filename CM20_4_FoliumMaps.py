# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 16:28:51 2021

@author: alex
"""
# !pip install pyplot from matplotlib
# !pip install folium
# !pip install geopy 

import pandas as pd
import numpy as np
import folium
from folium import plugins
from folium.plugins import HeatMap


# Daten laden und aufbereiten via FIle CM20_1 und CM20_3

# Karte initialisieren
mymap = folium.Map(
    location=[moto_aggr0720.loc['Z001','latitude'], 
              moto_aggr0720.loc['Z001','longitude']],
    zoom_start=12)


# Alle Messstationen von Fuss, Velo und Moto werden auf der Folium Map ergänzt, resp. angezeigt
# Rot für AUto, Blau für Velofahrer und Grün für Fussgänger

i = 0

for i in range(0, len(moto_aggr0720)):
    folium.Circle(
        radius=60,
        location=[moto_aggr0720.latitude[i], moto_aggr0720.longitude[i]],
        popup='Messstation Auto',
        color='crimson',
        fill=True,
    ).add_to(mymap)

    
for i in range(0, len(velo_aggr0720)):
    folium.Circle(
        radius=60,
        location=[velo_aggr0720.latitude[i], velo_aggr0720.longitude[i]],
        popup='Messstation Velo',
        color='blue',
        fill=True,
    ).add_to(mymap)
    
for i in range(0, len(fuss_aggr0720)):
    folium.Circle(
        radius=60,
        location=[fuss_aggr0720.latitude[i], fuss_aggr0720.longitude[i]],
        popup='Messstation Füssgaenger',
        color='green',
        fill=True,
    ).add_to(mymap)
    
del i 

mymap.save(path_to_file + '/mymap_ZH_stations.html')


# Karte Initialisierung und Messstationen anhand des heatmap anzeigen
mymap2 = folium.Map(
    location=[moto_aggr0720.loc['Z001','latitude'], 
              moto_aggr0720.loc['Z001','longitude']],
    zoom_start=13)

HeatMap(moto_aggr0720.iloc[:,[0,1,3]]).add_to(mymap2)
mymap2.save(path_to_file + '/moto0720_ZH.html')


mymap3 = folium.Map(
    location=[moto_aggr0719.loc['Z001','latitude'], 
              moto_aggr0719.loc['Z001','longitude']],
    zoom_start=13)

HeatMap(moto_aggr0719.iloc[:,[0,1,3]]).add_to(mymap3)
mymap3.save(path_to_file + '/moto0719_ZH.html')


# Veloerkehr vergleich 20 / 19
mymap4 = folium.Map(
    location=[velo_aggr0720.loc['60','latitude'], 
              velo_aggr0720.loc['60','longitude']],
    zoom_start=13)

HeatMap(velo_aggr0720.iloc[:,[0,1,3]]).add_to(mymap4)
mymap4.save(path_to_file + '/velo0720_ZH.html')


mymap5 = folium.Map(
    location=[velo_aggr0719.loc['60','latitude'], 
              velo_aggr0719.loc['60','longitude']],
    zoom_start=13)

HeatMap(velo_aggr0719.iloc[:,[0,1,3]]).add_to(mymap5)
mymap5.save(path_to_file + '/velo0719_ZH.html')

 
# Füssgänger vergleich 20 / 19
mymap4 = folium.Map(
    location=[fuss_aggr0720.loc['39','latitude'], 
              fuss_aggr0720.loc['39','longitude']],
    zoom_start=13)

HeatMap(fuss_aggr0720.iloc[:,[0,1,3]]).add_to(mymap4)
mymap4.save(path_to_file + '/fuss0720_ZH.html')


mymap5 = folium.Map(
    location=[fuss_aggr0719.loc['39','latitude'], 
              fuss_aggr0719.loc['39','longitude']],
    zoom_start=13)

HeatMap(fuss_aggr0719.iloc[:,[0,1,3]]).add_to(mymap5)
mymap5.save(path_to_file + '/fuss0719_ZH.html')

 

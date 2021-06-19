# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 15:49:12 2021

@author: alex
"""

import pandas as pd
import matplotlib.pyplot as plt               # Grafik library
plt.style.use('seaborn')                      # Style-Sheet für Grafiken 
import datetime
from datetime import date


# Daten in Pandas einlesen wenn nicht in Workspace
path_to_file = "C:/Users/alex/Documents/Data_Science_local/CAS_Information_Engineering/B_Scripting/00_Assignment/CovidMobilityZH"
velo_beide = pd.read_csv(path_to_file + '/velo_beide.csv', sep=",", header=0, index_col=False)
fuss_beide = pd.read_csv(path_to_file + '/fuss_beide.csv', sep=",", header=0, index_col=False)
moto_beide = pd.read_csv(path_to_file + '/moto_beide.csv', sep=",", header=0, index_col=False)


# Die Koordinaten in den Files basieren auf dem schweiz. Landesvermessungssystem LV95. Für die Anzeige 
# auf der Karte (z.B. via Folium), brauchen wir den internationalen Standard WGS84. 
#  - Schritt 1: Umrechnung der Koordinaten von LV95 auf LV03 (Code von Christian Cuppone)
#  - Schritt 2: Umrecnnung der Koordinaten von LV03 in WSG84 (Code von Valentin Minder, siehe:
#    https://github.com/ValentinMinder/Swisstopo-WGS84-LV03/commit/bb1622b6aa5f0bd0cfb005da529b63f8787f0da4#diff-08199f9d1863d76fc9c44e5babc483ea50265399ed9ad17af810878caa735d7e )

# Funktionen initialisieren
def LV95_LV03(nord95, ost95):
    '''Umrechnen der CH Koordinaten ins neuere CH Format'''
    nord03 = nord95 - 1000000
    ost03 = ost95 - 2000000
    return (nord03, ost03)

def CH_WGS84_lat(ost03, nord03):
    '''Umrechnen der CH Koordinaten in internationale Latitude'''
    ost03_aux = (ost03 - 600000) / 1000000                  # Zwischenwert für neues Format
    nord03_aux = (nord03 - 200000) / 1000000
    lat = (16.9023892 + (3.238272 * nord03_aux)) + \
            - (0.270978 * pow(ost03_aux, 2)) + \
            - (0.002528 * pow(nord03_aux, 2)) + \
            - (0.0447 * pow(ost03_aux, 2) * nord03_aux) + \
            - (0.0140 * pow(nord03_aux, 3))
    lat = (lat * 100) / 36                                  # Stellen anpassen und von Sekunde zu Grad
    return lat

def CH_WGS84_lng(ost03, nord03):
    '''Umrechnen der CH Koordinaten in internationale Longitude'''
    ost03_aux = (ost03 - 600000) / 1000000
    nord03_aux = (nord03 - 200000) / 1000000
    lng = (2.6779094 + (4.728982 * ost03_aux) + \
            + (0.791484 * ost03_aux * nord03_aux) + \
            + (0.1306 * ost03_aux * pow(nord03_aux, 2))) + \
            - (0.0436 * pow(ost03_aux, 3))
    lng = (lng * 100) / 36
    return lng

# Kolonnen für LV03 und WGS84 im Dataframe einfügen
moto_beide['koord_nord03'] = LV95_LV03(moto_beide['koordinate_nord'], moto_beide['koordinate_ost'])[0]    # Schritt 1
moto_beide['koord_ost03'] = LV95_LV03(moto_beide['koordinate_nord'], moto_beide['koordinate_ost'])[1]     # Schritt 1
moto_beide['latitude'] = CH_WGS84_lat(moto_beide['koord_ost03'], moto_beide['koord_nord03'])              # Schritt 2
moto_beide['longitude'] = CH_WGS84_lng(moto_beide['koord_ost03'], moto_beide['koord_nord03'])             # Schritt 2

velo_beide['koord_nord03'] = LV95_LV03(velo_beide['koordinate_nord'], velo_beide['koordinate_ost'])[0]
velo_beide['koord_ost03'] = LV95_LV03(velo_beide['koordinate_nord'], velo_beide['koordinate_ost'])[1]
velo_beide['latitude'] = CH_WGS84_lat(velo_beide['koord_ost03'], velo_beide['koord_nord03'])
velo_beide['longitude'] = CH_WGS84_lng(velo_beide['koord_ost03'], velo_beide['koord_nord03'])

fuss_beide['koord_nord03'] = LV95_LV03(fuss_beide['koordinate_nord'], fuss_beide['koordinate_ost'])[0]
fuss_beide['koord_ost03'] = LV95_LV03(fuss_beide['koordinate_nord'], fuss_beide['koordinate_ost'])[1]
fuss_beide['latitude'] = CH_WGS84_lat(fuss_beide['koord_ost03'], fuss_beide['koord_nord03'])
fuss_beide['longitude'] = CH_WGS84_lng(fuss_beide['koord_ost03'], fuss_beide['koord_nord03'])

# Check result
moto_beide.info()
velo_beide.info()


# Daten im Juni 20 aggregieren pro Messstation (Anzahl Fahrzeuge pro Station)
moto_aggr0720 = moto_beide.loc[(moto_beide['jahr'] == 2020) & (moto_beide['monat'] == 7)].groupby('station')
moto_aggr0720 = moto_aggr0720.agg({'latitude': np.max, 'longitude': np.max, 'anzahl': np.sum})
moto_aggr0720['gewicht'] = moto_aggr0720.anzahl / moto_aggr0720.anzahl.mean()

velo_aggr0720 = velo_beide.loc[(velo_beide['jahr'] == 2020) & (velo_beide['monat'] == 7)].groupby('station')
velo_aggr0720 = velo_aggr0720.agg({'latitude': np.max, 'longitude': np.max, 'anzahl': np.sum})
velo_aggr0720['gewicht'] = velo_aggr0720.anzahl / velo_aggr0720.anzahl.mean()

fuss_aggr0720 = fuss_beide.loc[(fuss_beide['jahr'] == 2020) & (fuss_beide['monat'] == 7)].groupby('station')
fuss_aggr0720 = fuss_aggr0720.agg({'latitude': np.max, 'longitude': np.max, 'anzahl': np.sum})
fuss_aggr0720['gewicht'] = fuss_aggr0720.anzahl / fuss_aggr0720.anzahl.mean()

# Daten im Juni 19 aggregieren pro Messstation (Anzahl Fahrzeuge pro Station)
moto_aggr0719 = moto_beide.loc[(moto_beide['jahr'] == 2019) & (moto_beide['monat'] == 7)].groupby('station')
moto_aggr0719 = moto_aggr0719.agg({'latitude': np.max, 'longitude': np.max, 'anzahl': np.sum})
moto_aggr0719['gewicht'] = moto_aggr0719.anzahl / moto_aggr0719.anzahl.mean()

velo_aggr0719 = velo_beide.loc[(velo_beide['jahr'] == 2019) & (velo_beide['monat'] == 7)].groupby('station')
velo_aggr0719 = velo_aggr0719.agg({'latitude': np.max, 'longitude': np.max, 'anzahl': np.sum})
velo_aggr0719['gewicht'] = velo_aggr0719.anzahl / velo_aggr0719.anzahl.mean()

fuss_aggr0719 = fuss_beide.loc[(fuss_beide['jahr'] == 2019) & (fuss_beide['monat'] == 7)].groupby('station')
fuss_aggr0719 = fuss_aggr0719.agg({'latitude': np.max, 'longitude': np.max, 'anzahl': np.sum})
fuss_aggr0719['gewicht'] = fuss_aggr0719.anzahl / fuss_aggr0719.anzahl.mean()


# Filtern auf Lockdown periode
start = date.fromisoformat('2019-03-15')
stop = date.fromisoformat('2019-04-19')



moto_lock19 = moto_beide.loc[(date.fromisoformat(str(moto_beide['datum'])) >= start) & (date.fromisoformat(str(moto_beide['datum'])) >= start)]


# Index-type wird bei velo und fuss automatisch auf type = Int64Index gesetzt. Das gibt Probleme bei nachfolgenden
# for-Schlaufen. Daher Uebersteuerung / Konvertierung des Index-Type via user defined function. 
def conv_index(list):
    newlist = []
    for element in list:
        element = str(element)
        newlist.append(element)
    return (newlist)

velo_aggr0720.index = conv_index(list(velo_aggr0720.index))
fuss_aggr0720.index = conv_index(list(fuss_aggr0720.index))
velo_aggr0719.index = conv_index(list(velo_aggr0719.index))
fuss_aggr0719.index = conv_index(list(fuss_aggr0719.index))


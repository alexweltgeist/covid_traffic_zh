# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 10:33:31 2021

@author: alex
"""

import pandas as pd
import matplotlib.pyplot as plt               # Grafik library
plt.style.use('seaborn')                      # Style-Sheet für Grafiken 


# Daten in Pandas einlesen wenn nicht in Workspace
path_to_file = "C:/Users/alex/Documents/Data_Science_local/CAS_Information_Engineering/B_Scripting/00_Assignment/CovidMobilityZH"
velo_beide = pd.read_csv(path_to_file + '/velo_beide.csv', sep=",", header=0, index_col=False)
fuss_beide = pd.read_csv(path_to_file + '/fuss_beide.csv', sep=",", header=0, index_col=False)
moto_beide = pd.read_csv(path_to_file + '/moto_beide.csv', sep=",", header=0, index_col=False)


# Auswertungen auf den vorbereiteten Daten ausführen 

# Erstellen von aggregierten Tabellen für die Grafiken
def year_comp_table(tabelle):
    ''' Anzahl Bewegungen pro Monat und Jahr im Vergleicv
        zwischen 2019 und 2020'''
    temp_19 = tabelle[tabelle.jahr.eq(2019)]
    ds_19 = temp_19.groupby(['monat'])['anzahl'].sum().rename('2019')
    temp_20 = tabelle[tabelle.jahr.eq(2020)]
    ds_20 = temp_20.groupby(['monat'])['anzahl'].sum().rename('2020')
    df_month_year = pd.concat([ds_19, ds_20], axis=1) 
    return df_month_year

def daily_freq_table(tabelle):
    '''Anzahl Bewegungen pro Tag und Stunde im Vergleich 
       zwischen 2019 und 2020'''
    temp_19 = tabelle[tabelle.jahr.eq(2019)]
    ds_19 = temp_19.groupby(['stunde'])['anzahl'].sum().rename('2019')      # tagesverlauf 19
    temp_20 = tabelle[tabelle.jahr.eq(2020)]
    ds_20 = temp_20.groupby(['stunde'])['anzahl'].sum().rename('2020')     # tagesverlauf 20
    df_daily_freq = pd.concat([ds_19, ds_20], axis=1) 
    return df_daily_freq

def monat_comp_table(tabelle, monat):
    ''' Anzahl Bewegungen pro Tag innerhalb eines Monats im Vergleich
        zwischen 2019 und 2020. Monat muss als Integer angegeben werden'''
    temp_monat = tabelle[tabelle.monat.eq(monat)]
    temp_monat19 = temp_monat[temp_monat.jahr.eq(2019)]
    ds_19 = temp_monat19.groupby(['tag'])['anzahl'].sum().rename(str(monat) + '_2019')
    temp_monat20 = temp_monat[temp_monat.jahr.eq(2020)]
    ds_20 = temp_monat20.groupby(['tag'])['anzahl'].sum().rename(str(monat) + '_2020')
    df_monat_tage = pd.concat([ds_19, ds_20], axis=1) 
    return df_monat_tage

# Funktionen zum Plotten
def plot_jahresvergleich(tabelle, name):
    '''Erstelle Graphik für Jahresvergleich'''
    graph = year_comp_table(tabelle).plot(kind = 'bar'
                                          , title = 'Jahresvergleich ' + name
                                          , color = ['lightblue', 'darkblue'])
    return graph

def plot_tagesverlauf(tabelle, name):
    '''Erstelle Graphik für Tagesverlauf'''
    graph = daily_freq_table(tabelle).plot(kind = 'line'
                                          , title = 'Tagesverlauf ' + name
                                          , color = ['lightblue', 'darkblue'])
    return graph

def boxplot_monatsvergleich(tabelle, monat, name):
    '''Graphik um die Verteilung innerhalb eines Monats zwischen
       2019 und 2020 zu vergleichen'''
    graph = monat_comp_table(tabelle, monat).plot(kind = 'box'
                                          , title = 'Monatsverlauf ' + name + ', im Monat ' + str(monat))
    return graph


# main: Funktionen anwenden auf die Verkehrsmittel

plot_jahresvergleich(moto_beide, 'Motorfahrzeuge')
plot_jahresvergleich(velo_beide, 'Velo')
plot_jahresvergleich(fuss_beide, 'Fussgänger')

plot_tagesverlauf(moto_beide, 'Motorfahrzeuge')
plot_tagesverlauf(velo_beide, 'Velo')
plot_tagesverlauf(fuss_beide, 'Fussgänger')

boxplot_monatsvergleich(moto_beide, 7, 'Motorfahrzeuge')
boxplot_monatsvergleich(velo_beide, 7, 'Velo')
boxplot_monatsvergleich(fuss_beide, 7, 'Fussgänger')

year_comp_table(moto_beide)
year_comp_table(velo_beide)
year_comp_table(fuss_beide)

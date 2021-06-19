# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 17:43:03 2020
Mobility and Covid19
@author: alex
version: v03, 15.11.2020
"""

# pls install if not done so previously
# !pip install seaborn==0.11


### Import Libraries / Style / Show Versions ###
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt               # Grafik library
plt.style.use('seaborn')                      # Style-Sheet für Grafiken 
!python --version
print(pd.__version__)
print(sns.__version__)

### not yet used ###
# import sqlalchemy
# import urllib.request
# import csv
# import mysql.connector
# from mysql.connector import Error
# import pymysql
# from folium import plugins
# from folium.plugins import MarkerCluster
# from folium.plugins import FastMarkerCluster

###
### Daten vom Web in Pandas Laden  ###
###

# Webpages fuer Datensatz Motorisierter Individualverkehr
url1 = "https://data.stadt-zuerich.ch/dataset/6212fd20-e816-4828-a67f-90f057f25ddb/resource/44607195-a2ad-4f9b-b6f1-d26c003d85a2/download/sid_dav_verkehrszaehlung_miv_od2031_2020.csv"
url2 = "https://data.stadt-zuerich.ch/dataset/6212fd20-e816-4828-a67f-90f057f25ddb/resource/fa64fa70-6328-4d47-bcf0-1eff694d7c22/download/sid_dav_verkehrszaehlung_miv_od2031_2019.csv"

# Webpages fuer Datensatz Fussgänger und Velo
url3 = "https://data.stadt-zuerich.ch/dataset/83ca481f-275c-417b-9598-3902c481e400/resource/b9308f85-9066-4f5b-8eab-344c790a6982/download/2020_verkehrszaehlungen_werte_fussgaenger_velo.csv"
url4 = "https://data.stadt-zuerich.ch/dataset/83ca481f-275c-417b-9598-3902c481e400/resource/33b3e7d3-f662-43e8-b018-e4b1a254f1f4/download/2019_verkehrszaehlungen_werte_fussgaenger_velo.csv"

# Referenztabelle mit Standortnamen für Velozähler muss bestellt werden unter: https://www.stadt-zuerich.ch/geodaten/download/Standorte_der_automatischen_Fuss__und_Velozaehlungen
# working_directory = os.getcwd() 
path_to_file = 'C:/Users/alex/Documents/Data_Science_local/CAS_Information_Engineering/B_Scripting/00_Assignment/CovidMobilityZH'

# Daten in Panda laden (dauert pro File zw. 1 bis 2 Minuten)
miv_2020 = pd.read_csv(url1, sep=",", header=0, index_col=0)
miv_2019 = pd.read_csv(url2, sep=",", header=0, index_col=0)
fv_2020 = pd.read_csv(url3, sep=",", header=0, index_col=0)
fv_2019 = pd.read_csv(url4, sep=",", header=0, index_col=0)

del url1, url2, url3, url4

# Daten sichten 
fv_2020.info()
fv_2020.head()
fv_2019.DATUM.describe()
fv_2020.VELO_IN.plot()

miv_2020.shape
miv_2020.info()
miv_2020.nunique()
miv_2020.head()
miv_2020.AnzFahrzeuge.describe()
miv_2020.AnzFahrzeuge.sum()
miv_2019.AnzFahrzeuge.sum()
miv_2019.AnzFahrzeuge.plot()


###
### Funktionen für die Datenaufbereitung
###

# Liste mit Zielnamen der Kolonnen
column_names = [ 'station', 'koordinate_nord', 'koordinate_ost', 'datum', 'jahr',
               'monat', 'tag', 'stunde', 'anzahl' ]

def combine_files(raw_data1, raw_data2):
    ''' Listen für 2019 und 2020 zusammenhängen '''
    raw_beide = pd.concat([raw_data1, raw_data2], axis=0)
    return(raw_beide)

def extract_fulldate(table):
    '''Liste erstellen aller Datum-Einträge'''    
    date_list = list(fv_beide.DATUM)
    return(date_list)

def extract_year(date_list):
    '''Jahr als String extrahieren'''
    fv_jahr = []
    for date in date_list:
        date_str = str(date)[0:4]
        fv_jahr.append(date_str)
    return(fv_jahr)

def extract_month(date_list):
    '''Monat als String extrahieren'''
    fv_monat = []
    for date in date_list:
        date_str = str(date)[5:7]
        fv_monat.append(date_str)
    return(fv_monat)

def extract_day(date_list):
    '''Tag als String extrahieren'''
    fv_tag = []
    for date in date_list:
        date_str = str(date)[8:10]
        fv_tag.append(date_str)
    return(fv_tag)

def extract_hour(date_list):
    '''Stunde als String extrahieren'''
    fv_stunde = []
    for date in date_list:
       date_str = str(date)[11:13]
       fv_stunde.append(date_str)
    return(fv_stunde)

def rename_columns(table):
    '''Kolonnen einheitlich benennen'''
    table.columns = column_names
    return table

def clean_index(table):
    '''Numerischen Index setzen'''
    table = table.reset_index(drop=True)
    return table

def remove_anzahl_null(table):
    '''Alle  Tupel mit NULL-Werten entfernen'''
    not_null = table.anzahl.notnull()
    table = table[not_null]
    return(table)

def format_korr(liste):
    ''' Konvertiere Werte einer Kolonne in Integers'''
    int_list = list()
    element = ''
    for line in liste:
        element = line.strip()
        element = int(element)
        int_list.append(element)
    return int_list

def reformat_date_fields(table):
    ''' Speicherung via to_csv und read_csv passt Dtypes automatisch an.
        Daher müssen die Felder jahr, monat, tag und stunde zwingend 
        als Integers gesetzt werden. '''
    clean_colums = ['jahr', 'monat', 'tag', 'stunde']
    for element in clean_colums:
        table[element] = format_korr(table[element])
    return(table)

def cleanup_table(table):
    '''Wendet die verschiedenen eigenen Funktionen an um die 
       Ausgangstabelle zu 'putzen'.'''
    table = rename_columns(table)
    table = remove_anzahl_null(table)
    table = clean_index(table)
    table = reformat_date_fields(table)
    return(table)


###
### Daten für Velo aufbereiten  
###

fv_beide = combine_files(fv_2019, fv_2020)
fv_datum = extract_fulldate(fv_beide)

# Kolonnen zurechtschneiden und anfügen
velo_temp = fv_beide.loc[:, ['FK_STANDORT', 'NORD', 'OST', 'VELO_IN', 'VELO_OUT', 'DATUM']]
velo_beide = velo_temp.assign(  fv_jahr = extract_year(fv_datum)
                              , fv_monat = extract_month(fv_datum)
                              , fv_tag = extract_day(fv_datum)
                              , fv_stunde = extract_hour(fv_datum)
                              , anzahl = velo_temp.VELO_IN + velo_temp.VELO_OUT)
velo_beide.drop(['VELO_IN', 'VELO_OUT'], axis=1, inplace=True)
velo_beide = cleanup_table(velo_beide)
velo_beide.info()

###
### Daten für Fussgänger aufbereiten   
###

# Kolonnen zurechtschneiden und anfügen
fuss_temp = fv_beide.loc[:, ['FK_STANDORT', 'NORD', 'OST', 'FUSS_IN', 'FUSS_OUT', 'DATUM']]
fuss_beide = fuss_temp.assign(  fv_jahr = extract_year(fv_datum)
                              , fv_monat = extract_month(fv_datum)
                              , fv_tag = extract_day(fv_datum)
                              , fv_stunde = extract_hour(fv_datum)
                              , anzahl = fuss_temp.FUSS_IN + fuss_temp.FUSS_OUT)
fuss_beide.drop(['FUSS_IN', 'FUSS_OUT'], axis=1, inplace=True)
fuss_beide = cleanup_table(fuss_beide)
fuss_beide.info()

del fv_beide
del fv_datum
del velo_temp
del fuss_temp

###
### Daten für Motorfahrzeuge aufbereiten  
###

# Listen für 2019 und 2020 zusammenhängen 
miv_beide = combine_files(miv_2019, miv_2020)
miv_datum = list(miv_beide.MessungDatZeit)

# Kolonnen zurechtschneiden und anfügen
moto_temp = miv_beide.loc[:, ['ZSID', 'NKoord', 'EKoord', 'AnzFahrzeuge', 'MessungDatZeit']]
moto_beide = moto_temp.assign(  m_jahr = extract_year(miv_datum) 
                              , m_monat = extract_month(miv_datum)
                              , m_tag = extract_day(miv_datum)
                              , m_stunde = extract_hour(miv_datum)
                              , anzahl = moto_temp.AnzFahrzeuge)
moto_beide.drop(['AnzFahrzeuge'], axis=1, inplace=True)
moto_beide = cleanup_table(moto_beide)
moto_beide.info()

del miv_beide
del miv_datum
del moto_temp
del moto_temp
del column_names

del fv_2019, fv_2020
del miv_2019, miv_2020

###
### Daten persistent speichern
###

# Daten aus Pandas in ein CSV file schreiben
velo_beide.to_csv(path_to_file + '/velo_beide.csv', sep=",", index=False)     # ohne index Kolonne                        
fuss_beide.to_csv(path_to_file + '/fuss_beide.csv', sep=",", index=False)  
moto_beide.to_csv(path_to_file + '/moto_beide.csv', sep=",", index=False)  

# und bei Bedarf wieder in Pandas einlesen
# path_to_file = "C:/Users/alex/Documents/Data_Science_local/CAS_Information_Engineering/B_Scripting/00_Assignment/CovidMobilityZH"
# velo_beide = pd.read_csv(path_to_file + '/velo_beide.csv', sep=",", header=0, index_col=0)
# fuss_beide = pd.read_csv(path_to_file + '/fuss_beide.csv', sep=",", header=0, index_col=0)
# moto_beide = pd.read_csv(path_to_file + '/moto_beide.csv', sep=",", header=0, index_col=0)


'''
###############################################
####                                       ####
#### bis oben geht der brauchbare code     ####
#### ab hier ist alles experimentell       ####
####                                       ####
###############################################


### Pandas df in DB schreiben mit sqlalchemy ###
### Index erstellen!! sonst lädt es nicht in db ###

# Create db engine (connection)
db_engine = sqlalchemy.create_engine("mysql+pymysql://root:rootroot@localhost/assignement_db")

# Show all tables in db by using engine and SQL code
with db_engine.connect() as connection:
    result = connection.execute("SHOW TABLES")
    for row in result:
        print(row)

# drop table if needed
with db_engine.connect() as connection:
    connection.execute("DROP TABLE fv_2019")

# Create a table in the db from a Pandas Dataframe
velo_beide.to_sql("velo_beide", db_engine)
fuss_beide.to_sql("fuss_beide", db_engine)
moto_beide.to_sql("moto_beide", db_engine)



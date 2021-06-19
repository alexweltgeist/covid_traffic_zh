# Verkehrsdaten-Analyse in Zürich während Covid Lockdown in 2020

Das Projekt analysiert die Veränderung der Verkehrsvolumen in der Stadt Zürich vor und während dem Lockdown im 2020. Dazu werden die Verkehrsdaten der Stadt Zürich verwendet. Die Übersicht des Projektes ist im File **Covid19ZH_preso.pdf** dargestellt, die ausführliche Beschreibung findet sind im Bericht **Gruppe6_Covid_Mobilitaet_20201130_v05.pdf**.

Das Projekt wurde zunächst lokal mit Python erstellt. Siehe dazu den Code mit Status "Lokale Version".

In einem zweiten Teil wurden Bestandteile auf Databricks Community Edition mit Spark nachimplementiert um die Performanz zu testen (Spark Version).

* Das File **Big_Data_Proj_Community_Final.ipynb** enthält den Code den wir für die meisten Messungen gebraucht haben
* **KoordinatenUmrechnen.ipynb** enthält den code für die Messung der UDF
* **Big_Data_Proj_Koalas.ipynb** enthält den code für die Samples in Koalas


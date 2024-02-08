import pandas as pd

#Lo que vamos hacer es extraer las tablas del grupo A al grupo H de la liga de campeones de la UEFA 2023-24
all_tables=pd.read_html('https://es.wikipedia.org/wiki/Liga_de_Campeones_de_la_UEFA_2023-24')

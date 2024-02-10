import requests
from bs4 import BeautifulSoup
import pandas as pd

# Obtener el contenido HTML de la página de Wikipedia
url = 'https://es.wikipedia.org/wiki/Liga_de_Campeones_de_la_UEFA_2023-24'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar la tabla que contiene la información de los grupos de la A a la H
tables = soup.find('div', class_='excerpt')

#vemos la información de la tabla
print(tables)

#la visualizamos en un dataframe
df = pd.read_html(str(tables))
print(df)

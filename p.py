import csv
import requests
from bs4 import BeautifulSoup

# URLs de diferentes temporadas de UEFA Champions League
urls = [
    "https://es.wikipedia.org/wiki/Liga_de_Campeones_de_la_UEFA_2023-24#Octavos_de_final",
    "https://es.wikipedia.org/wiki/Liga_de_Campeones_de_la_UEFA_2021-22#Octavos_de_final",
    "https://es.wikipedia.org/wiki/Liga_de_Campeones_de_la_UEFA_2020-21#Octavos_de_final",
    "https://es.wikipedia.org/wiki/Liga_de_Campeones_de_la_UEFA_2019-20#Octavos_de_final",
    "https://es.wikipedia.org/wiki/Liga_de_Campeones_de_la_UEFA_2018-19#Octavos_de_final",
    "https://es.wikipedia.org/wiki/Liga_de_Campeones_de_la_UEFA_2017-18#Octavos_de_final"
]

# Creamos una ñista para almacenar los datos de todas las temporadas
datos_totales = []

# Iteramos sobre los URLs
for url in urls:

    # Realizamos una solicitud GET a la URL
    r = requests.get(url)
    # Extraemos el HTML de la respuesta
    html = r.text

    # Creamos un objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Buscamos la sección de texto que contiene la información de los octavos
    octavos_html = soup.find('span', id='Octavos_de_final').find_next('table', class_='wikitable')

    # Obtenemos las filas de la tabla
    filas = octavos_html.find_all('tr')

    # Iteramos sobre las filas y obtenemos los datos de cada celda
    for fila in filas:
        # Obtenemos las celdas de la fila
        celdas = fila.find_all(['th', 'td'])
        # Extraemos el texto de cada celda y lo agregamos a la lista de datos
        datos_fila = [celda.get_text(strip=True) for celda in celdas]
        # Agregamos la temporada como la primera columna en cada fila, extrayéndola de la URL directamente
        temporada = url.split('_')[-3]
        datos_fila.insert(0, temporada.split('#')[0])
        # Agregamos la fila a la lista de datos totales
        datos_totales.append(datos_fila)

# Cambiamos el encabezado de la primera columna
datos_totales[0][0] = 'Temporada'

# pasamos datos a un archivo CSV
with open('octavos_champions.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(datos_totales)

# Imprimimos los datos
            
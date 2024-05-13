
import csv
import requests
from bs4 import BeautifulSoup

# Lista de años para las temporadas de la UEFA Champions League
years = [
   "2022-2023", "2021-2022", "2020-2021", "2019-2020", "2018-2019", "2017-2018",
    "2016-2017", "2015-2016", "2014-2015", "2013-2014", "2012-2013", "2011-2012",
    "2010-2011", "2009-2010", "2008-2009", "2007-2008", "2006-2007", "2005-2006",
    "2004-2005", "2003-2004"
]
# Creamos una lista para almacenar los datos de todas las temporadas
datos_totales = []

# Iteramos sobre los URLs

for year in years:

    url=f'https://fbref.com/en/comps/8/{year}/schedule/{year}-Champions-League-Scores-and-Fixtures'


    # Realizamos una solicitud GET a la URL
    r = requests.get(url)
    # Extraemos el HTML de la respuesta
    html = r.text

    # Creamos un objeto BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Buscamos la sección de texto que contiene la información de las fases eliminatorias
    html = soup.find('span', attrs={'data-label': 'Scores & Fixtures'}).find_next('table', id=lambda x: x and '_8_3' in x)
     
    # Obtenemos las filas de la tabla
    filas = html.find_all('tr')

    # Iteramos sobre las filas y obtenemos los datos de cada celda
    for fila in filas:
        # Obtenemos las celdas de la fila
        celdas = fila.find_all(['th', 'td'])
        # Eliminamos las celdas que contienen 'xg' en el atributo 'data-stat' ya que no están en todas las temporadas
        celdas = [celda for celda in celdas if 'xg' not in celda.get('data-stat')]
        # Extraemos el texto de cada celda y lo agregamos a la lista de datos
        datos_fila = [celda.get_text(strip=True) for celda in celdas]
        # Si la fila contiene datos, agregamos temporada y fila a la lista de datos totales
        if datos_fila:
            # Extraemos la termporada del URL directamente
            temporada = url.split('/')[-3]
            # Si la lista de datos totales está vacía, agregamos el encabezado de la tabla
            if len(datos_totales) == 0:
                # Agregamos la temporada al encabezado
                datos_fila.insert(0, 'Season')
            else:
                if datos_fila == datos_totales[0][1:]:
                    # Si la fila ya está en la lista de datos totales, pasa a la siguiente fila
                    continue
                else:
                    # Si la fila no coincide con la primera fila de datos totales, agregamos la temporada a la fila
                    datos_fila.insert(0, temporada)
            # Agregamos la fila a la lista de datos totales 
            # Solo añadimos los primeros 16 elementos de la lista, ya que el resto no nos interesa
            datos_totales.append(datos_fila)

# Escribimos los datos en un archivo CSV
ruta_csv = '../data/partidos.csv'
with open(ruta_csv, 'w', newline='', encoding='utf-8') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    for fila in datos_totales:
        escritor_csv.writerow(fila)

# Imprimimos un mensaje de éxito
print(f"El archivo CSV '{ruta_csv.split('/')[-1]}' ha sido creado exitosamente.")
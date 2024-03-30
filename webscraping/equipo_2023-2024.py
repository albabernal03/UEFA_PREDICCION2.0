
from bs4 import BeautifulSoup
import requests
import csv
# Creamos una lista para almacenar los datos de todas las temporadas
datos_totales = []

years=['2023-2024']

def get_data(year):
    try:
        url = f'https://fbref.com/en/comps/8/{year}/schedule/{year}-Champions-League-Scores-and-Fixtures'
        response = requests.get(url)
        response.raise_for_status()  # lanza una excepción si hay un error en la solicitud

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('span', attrs={'data-label': 'Scores & Fixtures'}).find_next('table', id=lambda x: x and '_8_3' in x)

        # Obtenemos las filas de la tabla
        rows = table.find_all('tr')

        # Iteramos sobre las filas y obtenemos los datos de cada celda
        for row in rows:
            # Obtenemos las celdas de la fila
            cells = row.find_all(['th', 'td'])
            # Eliminamos las celdas que contienen 'xg' en el atributo 'data-stat' ya que no están en todas las temporadas
            cells = [cell for cell in cells if 'xg' not in cell.get('data-stat')]
            # Extraemos el texto de cada celda y lo agregamos a la lista de datos
            row_data = [cell.get_text(strip=True) for cell in cells]
            # Agregamos la temporada como la primera columna en cada fila
            row_data.insert(0, year)
            # Agregamos la fila a la lista de datos totales
            datos_totales.append(row_data)

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos para el año {year}: {e}")

# Iteramos sobre los años y obtenemos los datos para cada año
for year in years:
    get_data(year)

# Cambiamos el encabezado de la primera columna
datos_totales[0][0] = 'Season'
# Escribimos los datos en un archivo CSV
csv_file = 'data/equipo_2023-2024.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for row in datos_totales:
        writer.writerow(row)

# Imprimimos un mensaje de éxito
print(f"El archivo CSV '{csv_file}' ha sido creado exitosamente.") #Esto lo puse para saber si se ejecutó correctamente

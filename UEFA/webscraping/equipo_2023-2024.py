import csv
import requests
from bs4 import BeautifulSoup

# Lista de años para las temporadas de la UEFA Champions League
years = ["2023-2024"]

# Creamos una lista para almacenar los datos de todas las temporadas
datos_totales = []

# Iteramos sobre los años y construimos las URLs dinámicamente
for year in years:
    try:
        url = f'https://fbref.com/en/comps/8/{year}/{year}-Champions-League-Stats'
        response = requests.get(url)
        response.raise_for_status()  # lanza una excepción si hay un error en la solicitud

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('span', attrs={'data-label': 'League Table'}).find_next('table', id=lambda x: x and 'overall' in x)

        # Obtenemos las filas de la tabla
        rows = table.find_all('tr')

        # Iteramos sobre las filas y obtenemos los datos de cada celda
        for row in rows:
            cells = row.find_all(['th', 'td'])
            # Eliminamos las celdas que contienen 'xg' en el atributo 'data-stat' ya que no están en todas las temporadas
            cells = [cell for cell in cells if 'xg' not in cell.get('data-stat')]
            # Extraemos el texto de cada celda y lo agregamos a la lista de datos
            data_row = [cell.get_text(strip=True) for cell in cells]
            # Si la fila contiene datos, agregamos temporada y fila a la lista de datos totales
            if data_row:
                # Si la lista de datos totales está vacía, agregamos el encabezado de la tabla
                if not datos_totales:
                    # Agregamos la temporada al encabezado
                    data_row.insert(0, 'Season')
                else:
                    # Si la fila no coincide con la primera fila de datos totales, agregamos la temporada a la fila
                    if data_row != datos_totales[0][1:]:
                        data_row.insert(0, year)
                # Agregamos la fila a la lista de datos totales
                datos_totales.append(data_row)
    except Exception as e:
        print(f"Error al procesar la temporada {year}: {e}")

# Escribimos los datos en un archivo CSV
csv_file_path = 'data/equipo_2023-2024.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    for row in datos_totales:
        csv_writer.writerow(row)

# Imprimimos un mensaje de éxito
print(f"El archivo CSV '{csv_file_path}' ha sido creado exitosamente.")

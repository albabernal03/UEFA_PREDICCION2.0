from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL de la página web
url = 'https://es.wikipedia.org/wiki/Anexo:Octavos_de_final_de_la_Liga_de_Campeones_de_la_UEFA_2022-23'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Buscamos la tabla de la página web
tabla = soup.find('table', {'class': 'wikitable'})

# Verificamos si la tabla existe
if tabla:
    data = []
    rows = tabla.find_all('tr')
    for row in rows:
        cols = row.find_all(['th', 'td'])  # Buscar tanto en celdas de encabezado como en celdas de datos
        row_data = [cell.get_text(strip=True) for cell in cols]
        data.append(row_data)

    # Convertir a DataFrame de pandas
    df = pd.DataFrame(data)

    # Guardar en un archivo CSV
    df.to_csv('datos_octavos_champions.csv', index=False)

    print("Datos guardados exitosamente en 'datos_octavos_champions.csv'.")
else:
    print("No se encontró la tabla en la página.")






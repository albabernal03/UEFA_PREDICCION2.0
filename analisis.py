from bs4 import BeautifulSoup
import requests
import pandas as pd

years = ['2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23']

def get_octavos(year):
    try:
        url = f'https://es.wikipedia.org/wiki/Anexo:Octavos_de_final_de_la_Liga_de_Campeones_de_la_UEFA_{year}'
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})

        if table:
            data = []
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                row_data = [cell.get_text(strip=True) for cell in cols]
                data.append(row_data)
            df = pd.DataFrame(data)
            df.to_csv(f'datos_octavos_champions_{year}.csv', index=False)
            print(f"Datos guardados exitosamente en 'datos_octavos_champions_{year}.csv'.")
        else:
            print(f"No se encontró la tabla en la página para el año {year}.")
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud para el año {year}: {e}")

for year in years:
    get_octavos(year)
  






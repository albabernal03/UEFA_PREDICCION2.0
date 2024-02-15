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
            # Add a new column for the season year
            df['Temporada'] = year
            return df
        else:
            print(f"No se encontró la tabla en la página para el año {year}.")
            return None
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud para el año {year}: {e}")
        return None

# Concatenate all the data into a single DataFrame
all_data = pd.DataFrame()
for year in years:
    df = get_octavos(year)
    if df is not None:
        all_data = pd.concat([all_data, df], ignore_index=True)

# Save the concatenated data to a single CSV file
all_data.to_csv('datos_octavos_champions_con_temporada.csv', index=False)
print("Datos concatenados guardados exitosamente en 'datos_octavos_champions_con_temporada.csv'.")
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
            # Add a new column for the season year
            df['Season'] = year
            return df
        else:
            print(f"No se encontró la tabla en la página para el año {year}.")
            return None
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud para el año {year}: {e}")
        return None

# Concatenate all the data into a single DataFrame
all_data = pd.DataFrame()
for year in years:
    df = get_octavos(year)
    if df is not None:
        all_data = pd.concat([all_data, df], ignore_index=True)

# Save the concatenated data to a single CSV file
all_data.to_csv('datos_octavos_champions_con_temporada.csv', index=False)
print("Datos concatenados guardados exitosamente en 'datos_octavos_champions_con_temporada.csv'.")

from bs4 import BeautifulSoup
import requests
import pandas as pd

years = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23']
stages = ['Octavos_de_final', 'Cuartos_de_final', 'Semifinales']

def get_data(year, stage):
    try:
        url = f'https://es.wikipedia.org/wiki/Anexo:{stage}_de_la_Liga_de_Campeones_de_la_UEFA_{year}'
        response = requests.get(url)
        response.raise_for_status()  # lanza una excepción

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})

        if table:
            data = []
            rows = table.find_all('tr')
            for row in rows[1:]:  # Se salta la primera fila que contiene los encabezados
                cols = row.find_all(['th', 'td'])
                row_data = [year, stage] + [cell.get_text(strip=True) for cell in cols]
                data.append(row_data)
            return data
        else:
            print(f"No se encontró la tabla en la página para el año {year} y la fase {stage}.")
            return None
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud para el año {year} y la fase {stage}: {e}")
        return None

all_data = []
for stage in stages:
    for year in years:
        data = get_data(year, stage)
        if data is not None:
            all_data.extend(data)


# Convert the list to a DataFrame
column_names = ['Temporada', 'Fase', 'Equipo 1', 'Agr.', 'Equipo 2', 'Ida', 'Vuelta']
all_data_df = pd.DataFrame(all_data, columns=column_names)

# Save the concatenated data to a single CSV file
all_data_df.to_csv('champions_results.csv', index=False)

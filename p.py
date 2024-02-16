from bs4 import BeautifulSoup
import requests
import pandas as pd

years = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23']
stages = ['Octavos_de_final', 'Cuartos_de_final', 'Semifinales', 'Final']

def get_data(year, stage):
    try:
        if stage != 'Final':
            url = f'https://es.wikipedia.org/wiki/Anexo:{stage}_de_la_Liga_de_Campeones_de_la_UEFA_{year}'
        else:
            url = f'https://es.wikipedia.org/wiki/Final_de_la_Liga_de_Campeones_de_la_UEFA_{year}'

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        if stage != 'Final':
            table = soup.find('table', {'class': 'wikitable'})
        else:
            # Encuentra la tabla que contiene los datos de la final
            table = soup.find('table', {'class': 'collapsible collapsed'})

        if table:
            data = []
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all(['th', 'td'])
                row_data = [year, stage]
                for cell in cols:
                    row_data.append(cell.get_text(strip=True))
                if stage == 'Final':
                    # Si es la fase final, agregamos una columna adicional para el resultado
                    final_result_th = soup.find('th', style="font-size:200%; white-space:nowrap")
                    if final_result_th:
                        final_result = final_result_th.get_text(strip=True)
                        row_data.append(final_result)
                    else:
                        # Si no se encuentra el resultado, añadimos un valor vacío
                        row_data.append('')
                # Asegurémonos de que todas las filas tengan la misma longitud
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

# Definimos las columnas incluyendo la columna adicional para el resultado
column_names = ['Temporada', 'Fase', 'Equipo 1', 'Agr.', 'Equipo 2', 'Ida', 'Vuelta', 'Resultado']

all_data_df = pd.DataFrame(all_data, columns=column_names)

# Guardamos los datos en un archivo CSV
all_data_df.to_csv('prueba.csv', index=False)

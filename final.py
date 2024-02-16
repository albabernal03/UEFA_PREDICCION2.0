from bs4 import BeautifulSoup
import requests

years = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23']

def get_final_data(year):
    url = f'https://es.wikipedia.org/wiki/Final_de_la_Liga_de_Campeones_de_la_UEFA_{year}'

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encuentra la tabla que contiene la información de la final
    table = soup.find('table', {'class': 'collapsible collapsed'})

    if table:
        # Extraer la primera fila de la tabla
        rows = table.find_all('tr')
        first_row = rows[0]

        # Buscar los elementos relevantes en la primera fila
        team_1 = first_row.find('a', title=True).get_text(strip=True)
        team_2 = first_row.find_all('a', title=True)[1].get_text(strip=True)
        result = first_row.find('b').get_text(strip=True)

        return team_1, result, team_2
    else:
        print(f"No se encontró la tabla en la página para el año {year}.")
        return None, None, None

final_data = []

for year in years:
    team_1, result, team_2 = get_final_data(year)
    final_data.append([year, team_1, result, team_2])  

#pasar csv
import csv
with open('final.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Temporada', 'Equipo 1', 'Resultado', 'Equipo 2'])
    writer.writerows(final_data)



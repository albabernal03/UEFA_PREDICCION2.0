
from bs4 import BeautifulSoup
import requests
years=[2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
web='https://espndeportes.espn.com/futbol/posiciones/_/liga/UEFA.CHAMPIONS/ordenar/pointdifferential/dir/desc/temporada/2022'
response=requests.get(web)
print(response.text)
'''soup=BeautifulSoup(content, 'lxml')'''





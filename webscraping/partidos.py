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

# Encabezados de las columnas
encabezados = ['Temporada','Ronda','Wk','Dia','Fecha','Hora','Local','Resultado','Visitante','Público','Evento','Arbitro','Reporte','Notas']

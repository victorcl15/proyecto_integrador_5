import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

class Collector:
    def __init__(self):
        self.url='https://es.finance.yahoo.com/quote/RIOT/history/' 
        if not os.path.exists('./src/recoleccion_de_datos_automaticos/static'):
            os.makedirs('./src/recoleccion_de_datos_automaticos/static', exist_ok=True)

        if not os.path.exists('./src/recoleccion_de_datos_automaticos/static/data'):
            os.makedirs('./src/recoleccion_de_datos_automaticos/static/data', exist_ok=True)


    def collector_data(self):
        try:
            df = pd.DataFrame()
            headers= {
             'User-Agent':'Mozilla/5.0'
            }
            response = requests.get(self.url,headers=headers)
            if response.status_code != 200:
                print(f'error en la linea 20')
                return df
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.select_one('div[data-testid="history-table"] table')
            if table is None: 
                print(f'error en la linea 26')
                return df
            headerss = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows=[]
            for tr in table.tbody.find_all('tr'):
                columns = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(columns) == len(headerss):
                    rows.append(columns)
            df = pd.DataFrame(rows,columns=headerss).rename(columns={
                'Fecha':'fecha',
                'Abrir':'abrir',
                'Máx.':'max',
                'Mín.':'min',
                'CerrarPrecio de cierre ajustado para splits.' : 'cerrar',
                'Cierre ajustadoPrecio de cierre ajustado para splits y distribuciones de dividendos o plusvalías.' : 'cierre_ajustado',
                'Volumen' : 'volumen'
            })
            return df
        except Exception as error:
         print (f"Error de valor: {error}")
        
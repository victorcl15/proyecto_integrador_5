import requests
from bs4 import BeautifulSoup
import pandas as pd
from logger import Logger


class Collector:
    def __init__(self, logger):
        self.url = "https://es.finance.yahoo.com/quote/RIOT/history/?period1=1459468800&period2=1746662400"
        self.logger = logger

    def collect_data(self):
        try:
            self.logger.info("Collector", "collect_data", "Iniciando la recolección de datos...")
            df = pd.DataFrame()
            headers = {
                'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.url, headers=headers)
            if response.status_code != 200:
                self.logger.error("Collector", "collect_data", f"Error en la solicitud: {response.status_code}")
                return df
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')
            if table is None:
                self.logger.error("Collector", "collect_data", "No se encontró la tabla de datos.")
                return df
            columns_headers = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows=[]
            for tr in table.tbody.find_all('tr'):
                columns = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(columns) == len(columns_headers):
                    rows.append(columns)
            df = pd.DataFrame(rows, columns=columns_headers).rename(columns={
                'Fecha':'fecha',
                'Abrir':'abrir',
                'Máx.':'max',
                'Mín.':'min',
                'CerrarPrecio de cierre ajustado para splits.':'cerrar',
                'Cierre ajustadoPrecio de cierre ajustado para splits y distribuciones de dividendos o plusvalías.':'cierre_ajustado',
                'Volumen':'volumen'
            })
            self.logger.info("Collector", "collect_data", "Datos recolectados con éxito. {}".format(df.shape))
            return df
        except Exception as e:
            self.logger.error("Collector", "collect_data", f"Error de conexión: {e}")
            return None
        
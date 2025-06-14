import pandas as pd


class Enricher:
    """
    Enriches the data with additional information.
    """

    def __init__(self, data):
        self.data = data


    def enriquecer(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Añade KPIs básicos al DataFrame:
        - daily_return
        - moving averages (7 y 30 días)
        - rolling volatility (14 días)
        - cumulative return
        - rolling std (30 días)
        """
        df = df.copy()
        
        # 1. Tasa de variación diaria
        df['daily_return'] = df['cierre_ajustado'].pct_change()
        
        # Ahora sí podemos eliminar filas sin retorno (después de crear la columna)
        df = df.dropna(subset=['daily_return']).reset_index(drop=True)
        
        # 2. Medias móviles
        df['ma_7'] = df['cierre_ajustado'].rolling(window=7, min_periods=1).mean()
        df['ma_30'] = df['cierre_ajustado'].rolling(window=30, min_periods=1).mean()
        
        # 3. Volatilidad (std de daily_return)
        df['volatility_14'] = df['daily_return'].rolling(window=14, min_periods=1).std()
        
        # 4. Retorno acumulado
        df['cum_return'] = (1 + df['daily_return']).cumprod() - 1
        
        # 5. Desviación estándar de cierre ajustado
        df['std_30'] = df['cierre_ajustado'].rolling(window=30, min_periods=1).std()
        
        return df

# if __name__ == '__main__':
#     # ejemplo de ejecución
#     from limpieza import cargar_y_limpiar
#     df0 = cargar_y_limpiar('data/riot_data.csv')
#     df_enriquecido = enriquecer(df0)
#     df_enriquecido.to_csv('data/riot_data_enriquecido.csv', index=False)
#     print("Enriquecimiento completado. Guardado en data/riot_data_enriquecido.csv")

from logger import Logger
import pandas as pd
import locale
import re

class Cleaning:
    """
    Class to clean the data.
    """

    def __init__(self, df, logger: Logger):
        """
        Initialize the class with the dataframe to be cleaned.
        """
        self.df = df
        self.logger = logger

    def cargar_y_limpiar(self, ruta_csv: str) -> pd.DataFrame:
        """
        1) Carga riot_data.csv
        2) Parseo de fecha y orden
        3) Conversión de columnas numéricas
        """
        try:
            # 1. Carga el CSV
            df = pd.read_csv(ruta_csv)
            
            self.logger.info("Cleaning", "cargar_y_limpiar", f"CSV cargado: {df.shape}")
            
            # 2. Convertir la columna fecha con el formato correcto
            if 'fecha' in df.columns:
                # Mapeo de nombres de meses en español
                month_map = {
                    'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
                    'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
                    'sept': 'Sep', 'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
                }
                
                # Convertir nombres de meses a inglés para que pd.to_datetime los entienda
                for spanish, english in month_map.items():
                    df['fecha'] = df['fecha'].str.replace(spanish, english, regex=False)
                
                df['fecha'] = pd.to_datetime(df['fecha'], format="%d %b %Y", errors='coerce')
                self.logger.info("Cleaning", "cargar_y_limpiar", f"Fechas convertidas, NaT: {df['fecha'].isna().sum()}")
            
            # 3. Reemplazar comas por puntos en columnas numéricas y convertir
            cols_num = ['abrir', 'max', 'min', 'cerrar', 'cierre_ajustado', 'volumen']
            for c in cols_num:
                if c in df.columns:
                    # Reemplazar comas por puntos para manejar decimales
                    if df[c].dtype == 'object':
                        df[c] = df[c].str.replace(',', '.', regex=False)
                    df[c] = pd.to_numeric(df[c], errors='coerce')
                    self.logger.info("Cleaning", "cargar_y_limpiar", f"Columna {c} convertida, NaN: {df[c].isna().sum()}")
            
            # 4. Verificar valores faltantes antes de filtrar
            self.logger.info("Cleaning", "cargar_y_limpiar", f"Valores NaN en fecha: {df['fecha'].isna().sum()}")
            self.logger.info("Cleaning", "cargar_y_limpiar", f"Valores NaN en cierre_ajustado: {df['cierre_ajustado'].isna().sum()}")
            
            # 5. Eliminar filas con valores faltantes críticos
            df_before = df.shape[0]
            df = df.dropna(subset=['fecha', 'cierre_ajustado'])
            df_after = df.shape[0]
            self.logger.info("Cleaning", "cargar_y_limpiar", f"Filas eliminadas por NaN: {df_before - df_after}")
            
            # 6. Ordenar cronológicamente
            df = df.sort_values('fecha').reset_index(drop=True)
            
            # 7. Verificar que tenemos datos después de limpiar
            if df.empty:
                self.logger.error("Cleaning", "cargar_y_limpiar", "¡DataFrame vacío después de limpiar!")
            else:
                self.logger.info("Cleaning", "cargar_y_limpiar", f"Datos limpios: {df.shape}")
            
            return df
        except Exception as e:
            self.logger.error("Cleaning", "cargar_y_limpiar", f"Error al limpiar datos: {str(e)}")
            import traceback
            self.logger.error("Cleaning", "cargar_y_limpiar", traceback.format_exc())
            # Devolver un DataFrame vacío en caso de error
            return pd.DataFrame()

# Uso de ejemplo:
# from limpieza import cargar_y_limpiar
# df = cargar_y_limpiar('data/riot_data.csv')
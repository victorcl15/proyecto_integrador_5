from logger import Logger
from collector import Collector
import pandas as pd
from auditor import Auditor

def main():
    logger = Logger()
    df = pd.DataFrame()
    logger.info('Main','main','Inicializar clase Logger')
    collector = Collector(logger=logger)

    df = collector.collector_data()
    
    # Definir la ruta del CSV
    csv_path = "./src/recoleccion_de_datos_automaticos/static/data/riot_data.csv"
    
    # Guardar datos en CSV
    df.to_csv(csv_path, index=False)

    # Auditar el proceso de extracción
    auditor = Auditor(logger=logger)
    audit_file = auditor.audit_extraction(df, csv_path)
    
    logger.info('Main','main', f'Proceso completado. Informe de auditoría en: {audit_file}')

if __name__ == "__main__":
    main()
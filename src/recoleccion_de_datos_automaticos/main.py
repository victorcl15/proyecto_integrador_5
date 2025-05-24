from logger import Logger
from collector import Collector
import pandas as pd
from auditor import Auditor
from cleaning import Cleaning
from enricher import Enricher
from modeller import Modeller

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
    
    # Limpiar los datos
    cleaning = Cleaning(df, logger=logger)
    
    df_cleaned = cleaning.cargar_y_limpiar(csv_path)
    
    # Enriquecer los datos
    enricher = Enricher(df_cleaned)
    df_enriched = enricher.enriquecer(df_cleaned)
    # Verificar que tenemos datos antes de continuar
    if df_enriched.empty or len(df_enriched) < 2:
        logger.error('Main', 'main', f'Error: DataFrame vacío o con datos insuficientes. Filas: {len(df_enriched)}')
        print(f"No hay suficientes datos para entrenar el modelo. Filas disponibles: {len(df_enriched)}")
        # Guardar lo que tengamos hasta este punto
        df_enriched.to_csv('./src/recoleccion_de_datos_automaticos/static/data/riot_data_enriched.csv', index=False)
        return  # Terminar ejecución
    
    # Si llegamos aquí, tenemos datos suficientes
    df_enriched.to_csv('./src/recoleccion_de_datos_automaticos/static/data/riot_data_enriched.csv', index=False)
    logger.info('Main','main', f'Datos enriquecidos y guardados en riot_data_enriched.csv. Filas: {len(df_enriched)}')
    
    # Modelling
    modeller = Modeller(df_enriched)
    
    # Verificar una vez más antes de entrenar
    if df_enriched.empty or len(df_enriched) < 2:
        logger.error('Main', 'main', f'Error antes de entrenar: DataFrame vacío o insuficiente. Filas: {len(df_enriched)}')
        return
        
    print(f"Columnas disponibles: {df_enriched.columns.tolist()}")
    print(f"Número de filas: {len(df_enriched)}")
    
    # Entrenar el modelo con los datos enriquecidos
    modeller.entrenar()
    
    # Realizar predicciones
    predicciones = modeller.predecir()
    
    # Combinar predicciones con datos originales
    df_con_predicciones = df_enriched.copy()
    df_con_predicciones['prediccion'] = predicciones
    
    # Guardar resultados con predicciones
    df_con_predicciones.to_csv('./src/recoleccion_de_datos_automaticos/static/data/riot_data_con_predicciones.csv', index=False)
    logger.info('Main','main', 'Modelo entrenado y predicciones guardadas en riot_data_con_predicciones.csv')
    
    

if __name__ == "__main__":
    main()
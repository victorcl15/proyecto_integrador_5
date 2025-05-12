import pandas as pd
import os
import datetime
from pathlib import Path

class Auditor:
    def __init__(self, logger):
        """Inicializa el auditor con el logger para registrar eventos"""
        self.logger = logger
        self.audit_dir = './docs'
        if not os.path.exists(self.audit_dir):
            os.makedirs(self.audit_dir, exist_ok=True)
            
    def audit_extraction(self, extracted_df, csv_path):
        """Audita el proceso de extracción y guardado de datos"""
        # Fecha y hora de la auditoría
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        audit_filename = f"{self.audit_dir}/audit_{now}.md"
        
        # Analizar el DataFrame extraído
        extracted_rows = len(extracted_df)
        extracted_columns = len(extracted_df.columns)
        column_types = extracted_df.dtypes
        null_values = extracted_df.isnull().sum()
        
        # Comprobar si el CSV fue guardado correctamente
        csv_exists = os.path.exists(csv_path)
        csv_df = None
        csv_rows = 0
        
        if csv_exists:
            csv_df = pd.read_csv(csv_path)
            csv_rows = len(csv_df)
            
        # Crear informe de auditoría
        with open(audit_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Informe de Auditoría - {now}\n\n")
            
            f.write("## Resumen de la Extracción\n\n")
            f.write(f"- Filas extraídas: {extracted_rows}\n")
            f.write(f"- Columnas extraídas: {extracted_columns}\n\n")
            
            f.write("## Guardado en CSV\n\n")
            f.write(f"- Archivo CSV: {csv_path}\n")
            f.write(f"- ¿Existe el archivo?: {'Sí' if csv_exists else 'No'}\n")
            f.write(f"- Filas en CSV: {csv_rows}\n\n")
            
            f.write("## Comparativa\n\n")
            if csv_exists:
                f.write(f"- Coincidencia de filas: {'Sí' if extracted_rows == csv_rows else 'No'}\n")
                if extracted_rows != csv_rows:
                    f.write(f"  - Diferencia: {extracted_rows - csv_rows} filas\n")
            else:
                f.write("- No se puede comparar: archivo CSV no encontrado\n\n")
                
            f.write("## Análisis de Columnas\n\n")
            f.write("| Columna | Tipo de Dato | Valores Nulos |\n")
            f.write("| ------- | ------------ | ------------- |\n")
            for col in extracted_df.columns:
                f.write(f"| {col} | {column_types[col]} | {null_values[col]} |\n")
                
            f.write("\n## Distribución de Valores Nulos\n\n")
            total_nulls = null_values.sum()
            f.write(f"- Total de valores nulos: {total_nulls}\n")
            if total_nulls > 0:
                f.write("- Detalle por columna:\n")
                for col in extracted_df.columns:
                    if null_values[col] > 0:
                        null_percent = (null_values[col] / extracted_rows) * 100
                        f.write(f"  - {col}: {null_values[col]} ({null_percent:.2f}%)\n")
        
        self.logger.info("Auditor", "audit_extraction", f"Informe de auditoría generado: {audit_filename}")
        return audit_filename

from collector import Collector
from logger import Logger
import pandas as pd


def main():
    """Función principal para ejecutar el script de recolección de datos."""
    logger = Logger()
    collector = Collector(logger)
    df = pd.DataFrame()
    df = collector.collect_data()
    if df is not None:
        print(df)







if __name__ == "__main__":
    main()
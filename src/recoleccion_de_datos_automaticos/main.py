from collector import Collector
import pandas as pd


def main():
    df = pd.DataFrame()
    collector = Collector()

    df = collector.collector_data()
    df.to_csv("./src/recoleccion_de_datos_automaticos/static/data/riot_data.csv")



if __name__ == "__main__":
    main()
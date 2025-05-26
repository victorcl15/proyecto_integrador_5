import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import os

# Asegurar que existe la carpeta para guardar el modelo
# os.makedirs('./src/recoleccion_de_datos_automaticos/static/models/', exist_ok=True)
MODEL_PATH = './src/recoleccion_de_datos_automaticos/static/models/model.pkl'


class Modeller:
    def __init__(self, data):
        self.data = data
        self.model = None

    def entrenar(self, target_col='cierre_ajustado'):
        """
        - Separa features y target
        - Entrena un RandomForest (ejemplo)
        - Guarda el modelo en MODEL_PATH
        - Imprime MAE y RMSE en test set
        """
        # 1. Preparar X e y
        X = self.data.drop(columns=['fecha', target_col])
        y = self.data[target_col]
        
        # 2. Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )
        
        # 3. Entrenamiento
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        self.model = model
        
        # 4. Predicción y métricas
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        # rmse = mean_squared_error(y_test, preds, squared=False)
        mse = mean_squared_error(y_test, preds)
        rmse = mse ** 0.5  # Raíz cuadrada del MSE
        print(f"MAE: {mae:.4f}   RMSE: {rmse:.4f}")
        
        # 5. Guardar artefacto
        joblib.dump(model, MODEL_PATH)
        print(f"Modelo guardado en {MODEL_PATH}")

    def predecir(self, df=None):
        """
        Carga el modelo guardado y devuelve un pd.Series de predicciones
        para el DataFrame de entrada (mismas columnas de X entrenadas).
        """
        if df is None:
            df = self.data
            
        # Si tenemos un modelo cargado, lo usamos
        if self.model:
            model = self.model
        else:
            # Si no, intentamos cargar el modelo guardado
            model = joblib.load(MODEL_PATH)
            
        X = df.drop(columns=['fecha', 'cierre_ajustado'], errors='ignore')
        preds = model.predict(X)
        return pd.Series(preds, index=df.index, name='predicted_cierre')
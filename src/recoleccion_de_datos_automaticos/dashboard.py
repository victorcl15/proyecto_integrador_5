import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Cargar los datos
df = pd.read_csv("src/recoleccion_de_datos_automaticos/static/data/riot_data_enriched.csv")
df['fecha'] = pd.to_datetime(df['fecha'])

# Mostrar título
st.title("Dashboard de KPIs Financieros - RIOT")

# Filtro por rango de fechas
fecha_inicio = st.date_input("Fecha inicio", df['fecha'].min())
fecha_fin = st.date_input("Fecha fin", df['fecha'].max())

df_filtrado = df[(df['fecha'] >= pd.to_datetime(fecha_inicio)) & (df['fecha'] <= pd.to_datetime(fecha_fin))]

df['ma_30'] = df['cierre_ajustado'].rolling(window=30).mean()


# KPIs
st.subheader("📊 Indicadores clave")

col1, col2, col3 = st.columns(3)

with col1:
    tasa_variacion = df_filtrado['daily_return'].mean()
    st.metric("Tasa de Variación Promedio", f"{tasa_variacion:.2%}")

with col2:
    media_movil = df_filtrado['ma_7'].iloc[-1]
    st.metric("Media Móvil (7 días)", f"{media_movil:.2f}")

with col3:
    volatilidad = df_filtrado['volatility_14'].iloc[-1]
    st.metric("Volatilidad (14 días)", f"{volatilidad:.2f}")

col4, col5 = st.columns(2)

with col4:
    retorno_acumulado = df_filtrado['cum_return'].iloc[-1]
    st.metric("Retorno Acumulado", f"{retorno_acumulado:.2%}")

with col5:
    desviacion_std = df_filtrado['std_30'].iloc[-1]
    st.metric("Desviación Estándar (30 días)", f"{desviacion_std:.2f}")

# Gráfico interactivo
st.subheader("📈 Cierre Ajustado")
fig, ax = plt.subplots()
ax.plot(df_filtrado['fecha'], df_filtrado['cierre_ajustado'], label="Cierre ajustado")
ax.plot(df_filtrado['fecha'], df_filtrado['ma_7'], label="MA 7", linestyle='--')
ax.plot(df_filtrado['fecha'], df_filtrado['ma_30'], label="MA 30", linestyle=':', color='green')
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio")
ax.legend()
st.pyplot(fig)
st.markdown("Se observan fuertes picos de volatilidad en 2018 y especialmente en 2021, seguidos de una caída sostenida del precio. Las medias móviles suavizan las fluctuaciones diarias, permitiendo identificar tendencias: cuando el precio cruza por encima de ellas, sugiere una fase alcista, y cuando cae por debajo, indica posibles correcciones o fases bajistas. En general, el activo pasó de una etapa especulativa a una fase de mayor estabilidad en los últimos años.")


st.subheader("📉 Retorno Diario (%)")
st.line_chart(df_filtrado.set_index("fecha")["daily_return"])
st.markdown("Se observan picos significativos de retorno positivo y negativo especialmente entre 2018 y 2021, lo que evidencia una alta volatilidad durante esos años. A partir de 2022, las fluctuaciones se vuelven menos extremas, lo que sugiere un comportamiento más estable del activo. Este tipo de análisis permite entender el riesgo y la frecuencia de cambios bruscos en el precio.")


st.subheader("📊 Volatilidad 14 días")
st.bar_chart(df_filtrado.set_index("fecha")["volatility_14"])
st.markdown(" Se observan picos significativos de volatilidad entre 2018 y 2021, coincidiendo con periodos de alta inestabilidad del activo. A partir de 2022, la volatilidad disminuye y se mantiene en niveles más bajos y estables, lo que sugiere un comportamiento menos especulativo. Este indicador permite evaluar el riesgo asociado a invertir en el activo, ya que mayores niveles de volatilidad implican mayor incertidumbre en los precios.")

st.subheader("📈 Retorno Acumulado")
st.area_chart(df_filtrado.set_index("fecha")["cum_return"])
st.markdown("Se evidencian fases de fuerte crecimiento, especialmente en 2018 y 2021, seguidas por caídas pronunciadas que reflejan pérdida de ganancias acumuladas. A partir de 2022, el retorno muestra una tendencia más estable, pero sin recuperar los niveles máximos anteriores. Este indicador es útil para visualizar el desempeño histórico total de una inversión y evaluar su comportamiento en distintos ciclos del mercado.")


fig = px.scatter(df_filtrado, x="volatility_14", y="cierre_ajustado", color="fecha", 
                 title="Relación entre Precio y Volatilidad")
st.plotly_chart(fig)
st.markdown(" Se observa que, en general, los precios más altos tienden a estar asociados con niveles de volatilidad moderada, aunque hay excepciones con alta volatilidad en rangos de precios elevados. Esto sugiere que, aunque el aumento en el precio puede coincidir con cierta inestabilidad, no existe una correlación lineal clara entre ambas variables. Este tipo de visualización ayuda a entender cómo varía el riesgo (volatilidad) en diferentes niveles de precio.")

st.subheader("📊 Distribución de Retornos Diarios")
fig, ax = plt.subplots()
ax.hist(df_filtrado["daily_return"], bins=50, color='skyblue', edgecolor='black')
ax.set_xlabel("Retorno Diario")
ax.set_ylabel("Frecuencia")
st.pyplot(fig)
st.markdown("La forma de campana centrada alrededor del 0 indica que la mayoría de los retornos diarios son pequeños y cercanos a cero, con más días ligeramente positivos o negativos. También se observa una ligera asimetría hacia la derecha, lo que sugiere que aunque las pérdidas extremas ocurren, hay días con retornos positivos muy altos. Esta visualización ayuda a evaluar la frecuencia, magnitud y simetría de los rendimientos diarios, lo cual es clave para analizar el riesgo.")


st.subheader("🔥 Mapa de calor de correlaciones")
corr = df_filtrado[["cierre_ajustado", "ma_7", "ma_30", "daily_return", "volatility_14", "cum_return", "std_30"]].corr()
fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)
st.markdown("Se observa una alta correlación entre el precio de cierre ajustado, las medias móviles (MA 7 y MA 30), y el retorno acumulado, lo que indica que estas variables se mueven casi en sincronía. Por el contrario, los retornos diarios presentan muy baja correlación con las demás variables, lo que sugiere que sus fluctuaciones son más independientes. Este análisis es útil para identificar relaciones directas entre indicadores y evitar redundancias al seleccionar variables para modelos predictivos o análisis técnico.")

# Cargar los datos con predicciones
df_pred = pd.read_csv("src/recoleccion_de_datos_automaticos/static/data/riot_data_con_predicciones.csv")
df_pred['fecha'] = pd.to_datetime(df_pred['fecha'])

# Filtrar datos de predicciones por el mismo rango de fechas
df_pred_filtrado = df_pred[(df_pred['fecha'] >= pd.to_datetime(fecha_inicio)) & (df_pred['fecha'] <= pd.to_datetime(fecha_fin))]

st.subheader("🔮 Precio Real vs Predicción del Modelo")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_pred_filtrado['fecha'], df_pred_filtrado['cierre_ajustado'], label="Precio Real", linewidth=2, color='blue')
ax.plot(df_pred_filtrado['fecha'], df_pred_filtrado['prediccion'], label="Predicción", linewidth=2, color='red', linestyle='--')
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio ($)")
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_title("Comparación entre Precio Real y Predicciones del Modelo")
st.pyplot(fig)

st.markdown("El modelo de Random Forest muestra un desempeño notable al seguir de cerca las tendencias principales del precio real de RIOT. Se observa que las predicciones capturan efectivamente los movimientos direccionales y los patrones generales, aunque con cierto desfase en los picos más extremos. La precisión del modelo es especialmente evidente en períodos de menor volatilidad, mientras que en momentos de alta volatilidad las predicciones tienden a ser más conservadoras. Este comportamiento es típico de los modelos de machine learning que priorizan la estabilidad sobre la captura de movimientos extremos.")



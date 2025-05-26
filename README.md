# 📊 Análisis Financiero Riot Platforms, Inc. (RIOT)

[![Dashboard](https://img.shields.io/badge/Ver%20Dashboard-Streamlit-FF4B4B)](https://proyectointegrador5.streamlit.app/)

## Visión General

Este proyecto implementa un sistema automatizado de recolección, procesamiento, análisis y visualización de datos financieros históricos de RIOT. Incluye un pipeline completo que ejecuta extracción de datos desde Yahoo Finance, limpieza, enriquecimiento con KPIs financieros, modelado predictivo y visualización mediante un dashboard interactivo.

## 🔍 Características Principales

- **Extracción Automática**: Obtiene datos históricos de Yahoo Finance
- **Pipeline de Datos**: Limpieza, transformación y enriquecimiento con métricas financieras
- **KPIs Financieros**: Cálculo de retornos diarios, volatilidad, medias móviles y más
- **Modelado Predictivo**: Implementa Random Forest para predecir precios futuros
- **Dashboard Interactivo**: Visualización de métricas clave mediante Streamlit
- **Auditoría y Logging**: Sistema completo de registro y auditoría de procesos

## 🛠️ Tecnologías Utilizadas

- **Python**: Lenguaje principal de desarrollo
- **Pandas/NumPy**: Manipulación y análisis de datos
- **Scikit-learn**: Modelado predictivo
- **Streamlit**: Visualización interactiva
- **Matplotlib/Plotly/Seaborn**: Generación de gráficos
- **BeautifulSoup**: Web scraping
- **GitHub Actions**: Automatización del pipeline

## 🚀 Instalación y Uso

```bash
# Clonar el repositorio
git clone <url-repositorio>

# Instalar dependencias
pip install -e .

# Ejecutar el pipeline completo
python src/recoleccion_de_datos_automaticos/main.py

# Iniciar el dashboard
streamlit run src/recoleccion_de_datos_automaticos/dashboard.py

## 📂 Estructura del Proyecto

- **collector.py**: Extracción de datos desde Yahoo Finance
- **cleaning.py**: Limpieza y preparación de datos
- **enricher.py**: Cálculo de KPIs financieros
- **modeller.py**: Modelado predictivo con RandomForest
- **dashboard.py**: Interfaz interactiva con Streamlit
- **logger.py & auditor.py**: Sistema de logging y auditoría

## 👥 Autores

- Victor Calle
- Shara Mosquera

---

[**Ver Dashboard Interactivo**](https://proyectointegrador5.streamlit.app/) | [GitHub](https://github.com/)
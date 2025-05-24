from setuptools import setup, find_packages

setup(
    name="recoleccion_de_datos_automaticos",
    version="0.0.1",
    author="Victor Calle y Shara Mosquera",
    author_email="",
    description="",
    py_modules=["actividad_1"],
    install_requires=[
        "pandas==2.2.3",
        "openpyxl",
        "requests==2.32.3",
        "beautifulsoup4==4.13.3",
        "scikit-learn>=0.24.0",
        "joblib>=1.1.0" 
    ]
) 
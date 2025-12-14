# ✈️ Dashboard de Análisis de Retrasos de Vuelos 2015

Dashboard interactivo de Streamlit para analizar el dataset de retrasos de vuelos de Kaggle (usdot/flight-delays).

## 🚀 Instalación Rápida con UV

[UV](https://github.com/astral-sh/uv) es un gestor de paquetes Python ultrarrápido. Sigue estos pasos:

### 1. Instalar UV

```bash
# Para Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Para Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Instalar Dependencias

```bash
# Opción 1: Instalación directa con uv (recomendado)
uv pip install streamlit pandas plotly numpy kagglehub

# Opción 2: Con pip tradicional
pip install streamlit pandas plotly numpy kagglehub
```

### 3. Ejecutar el Dashboard

```bash
# Si estás en el directorio del proyecto
cd /ruta/a/Data-analysis-for-the-2015-flight-dealys-and-cancelation

# Ejecutar con Python del venv
../.venv/bin/python -m streamlit run Dani.py

# O si streamlit está en el PATH del sistema
streamlit run Dani.py
```

**Nota**: El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Características

### Visualizaciones Incluidas:

1. **🌍 Mapa Geográfico Interactivo**
   - Visualización de aeropuertos con volumen de vuelos y retrasos
   - Tamaño del punto = número de vuelos
   - Color = retraso promedio

2. **📅 Heatmap Temporal**
   - Análisis de día de la semana vs mes
   - Identifica los peores momentos para volar
   - Patrones de estacionalidad

3. **🏢 Análisis de Rendimiento**
   - Comparación de aerolíneas
   - Tasas de cancelación
   - Retrasos promedio
   - Causas de cancelación

### Filtros Interactivos:

- 📅 Filtro por mes
- ✈️ Filtro por aerolínea
- 🛫 Filtro por aeropuerto de origen
- 📏 Control de tamaño de muestra

## 📁 Estructura del Proyecto

```
.
├── Dani.py              # Aplicación principal de Streamlit
├── pyproject.toml       # Configuración de dependencias (UV)
└── README.md           # Este archivo
```

## 🔧 Requisitos

- Python >= 3.9
- Streamlit >= 1.28.0
- Pandas >= 2.0.0
- Plotly >= 5.17.0
- NumPy >= 1.24.0
- KaggleHub >= 0.1.0

## 📝 Notas Importantes

- **Primera ejecución**: El dataset se descargará automáticamente desde Kaggle (~100MB)
- **Rendimiento**: Por defecto carga 100,000 filas para optimizar velocidad
- **Caché**: Los datos se cachean automáticamente para recargas rápidas

## 🎓 Autor

**Daniel Ariza García**  
Proyecto Universitario - Almacenamiento, Visualización y Procesamiento de Datos

## 📄 Licencia

Este proyecto es para fines educativos.

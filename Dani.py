"""
Dashboard Interactivo de Análisis de Retrasos de Vuelos
========================================================
Autor: Daniel Ariza García
Proyecto: Análisis de datos de vuelos 2015
Dataset: usdot/flight-delays (Kaggle)

Este dashboard analiza la fiabilidad de los vuelos usando visualizaciones interactivas
organizadas en tres dimensiones principales: Geográfica, Temporal y Rendimiento.

INSTALACIÓN Y EJECUCIÓN CON UV:
--------------------------------
1. Instalar uv (si no lo tienes):
   curl -LsSf https://astral.sh/uv/install.sh | sh

2. Instalar dependencias:
   uv pip install streamlit pandas plotly numpy kagglehub
   
   O usando el archivo pyproject.toml:
   uv pip install -e .

3. Ejecutar el dashboard:
   uv run streamlit run Dani.py
   
   O alternativamente:
   streamlit run Dani.py
"""

# ==================== IMPORTACIÓN DE LIBRERÍAS ====================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
import warnings

warnings.filterwarnings('ignore')

# Intentar importar kagglehub (necesario para descargar el dataset)
try:
    import kagglehub
    KAGGLEHUB_AVAILABLE = True
except ImportError:
    KAGGLEHUB_AVAILABLE = False
    st.warning("⚠️ kagglehub no está instalado. Instálalo con: pip install kagglehub")


# ==================== CONFIGURACIÓN DE LA PÁGINA ====================
st.set_page_config(
    page_title="✈️ Análisis de Retrasos de Vuelos 2015",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== FUNCIONES DE CARGA Y PROCESAMIENTO DE DATOS ====================

@st.cache_data(show_spinner=True)
def load_flight_data(sample_size=100000):
    """
    Carga el dataset de vuelos desde Kaggle usando kagglehub.
    
    Args:
        sample_size (int): Número de filas a cargar aleatoriamente para optimizar rendimiento
        
    Returns:
        tuple: (flights_df, airports_df) - DataFrames de vuelos y aeropuertos
    """
    try:
        if not KAGGLEHUB_AVAILABLE:
            st.error("❌ No se puede cargar los datos sin kagglehub instalado.")
            return None, None
        
        # Descargar el dataset usando kagglehub
        with st.spinner('📥 Descargando dataset desde Kaggle...'):
            path = kagglehub.dataset_download("usdot/flight-delays")
        
        st.info(f"📂 Dataset descargado en: {path}")
        
        # Buscar los archivos CSV en el directorio descargado
        path_obj = Path(path)
        flights_file = None
        airports_file = None
        
        # Buscar flights.csv y airports.csv
        for file in path_obj.rglob('*.csv'):
            if 'flights' in file.name.lower():
                flights_file = file
            elif 'airports' in file.name.lower():
                airports_file = file
        
        if flights_file is None:
            st.error("❌ No se encontró el archivo flights.csv")
            return None, None
        
        # Leer el archivo de vuelos
        # Primero obtener el número total de filas
        with st.spinner('📊 Cargando datos de vuelos...'):
            # Leer una muestra pequeña para conocer las columnas
            df_sample = pd.read_csv(flights_file, nrows=1000)
            total_rows = sum(1 for _ in open(flights_file)) - 1  # -1 por el header
            
            # Si el archivo es grande y se especifica un sample_size finito, cargar solo una muestra
            if total_rows > sample_size and sample_size != float('inf'):
                # Crear índices aleatorios para samplear
                skip_idx = np.random.choice(range(1, total_rows + 1), 
                                           size=total_rows - sample_size, 
                                           replace=False)
                flights_df = pd.read_csv(flights_file, skiprows=skip_idx)
                st.success(f"✅ Cargada muestra aleatoria de {len(flights_df):,} filas de {total_rows:,} totales")
            else:
                # Cargar todos los datos
                flights_df = pd.read_csv(flights_file)
                st.success(f"✅ Cargadas todas las {len(flights_df):,} filas del dataset completo 🎉")
        
        # Leer el archivo de aeropuertos si existe
        airports_df = None
        if airports_file:
            with st.spinner('🛫 Cargando datos de aeropuertos...'):
                airports_df = pd.read_csv(airports_file)
                st.success(f"✅ Cargados {len(airports_df):,} aeropuertos")
        else:
            st.warning("⚠️ No se encontró airports.csv. El mapa no estará disponible.")
        
        return flights_df, airports_df
    
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return None, None


def clean_and_engineer_data(flights_df, airports_df):
    """
    Limpia los datos y realiza ingeniería de características.
    Hace merge con airports para obtener coordenadas geográficas.
    
    Args:
        flights_df (pd.DataFrame): DataFrame de vuelos
        airports_df (pd.DataFrame): DataFrame de aeropuertos
        
    Returns:
        pd.DataFrame: DataFrame procesado y limpio
    """
    try:
        # Crear una copia para no modificar el original
        df = flights_df.copy()
        
        # ========== LIMPIEZA DE DATOS ==========
        
        # Rellenar valores nulos en columnas de retrasos con 0
        delay_columns = [col for col in df.columns if 'DELAY' in col.upper()]
        for col in delay_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Rellenar CANCELLED con 0 (no cancelado)
        if 'CANCELLED' in df.columns:
            df['CANCELLED'] = df['CANCELLED'].fillna(0)
        
        # ========== INGENIERÍA DE CARACTERÍSTICAS ==========
        
        # Crear columnas de fecha más útiles
        if 'MONTH' in df.columns:
            df['MONTH_NAME'] = df['MONTH'].map({
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            })
        
        if 'DAY_OF_WEEK' in df.columns:
            df['DAY_NAME'] = df['DAY_OF_WEEK'].map({
                1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves',
                5: 'Viernes', 6: 'Sábado', 7: 'Domingo'
            })
        
        # Calcular retraso total (suma de todos los tipos de retraso)
        if 'ARRIVAL_DELAY' in df.columns:
            df['TOTAL_DELAY'] = df['ARRIVAL_DELAY']
        elif all(col in df.columns for col in ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 
                                                 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 
                                                 'WEATHER_DELAY']):
            df['TOTAL_DELAY'] = (df['AIR_SYSTEM_DELAY'] + df['SECURITY_DELAY'] + 
                                df['AIRLINE_DELAY'] + df['LATE_AIRCRAFT_DELAY'] + 
                                df['WEATHER_DELAY'])
        
        # ========== MERGE CON AEROPUERTOS ==========
        
        # Si existe el DataFrame de aeropuertos, hacer merge para obtener coordenadas
        if airports_df is not None and 'ORIGIN_AIRPORT' in df.columns:
            # Preparar DataFrame de aeropuertos
            airports_clean = airports_df.copy()
            
            # Renombrar columnas para el merge (ajustar según la estructura real)
            if 'IATA_CODE' in airports_clean.columns:
                airports_clean = airports_clean.rename(columns={'IATA_CODE': 'AIRPORT_CODE'})
            elif 'AIRPORT' in airports_clean.columns:
                airports_clean = airports_clean.rename(columns={'AIRPORT': 'AIRPORT_CODE'})
            
            # Seleccionar solo las columnas necesarias
            coord_cols = ['AIRPORT_CODE']
            if 'LATITUDE' in airports_clean.columns:
                coord_cols.append('LATITUDE')
            if 'LONGITUDE' in airports_clean.columns:
                coord_cols.append('LONGITUDE')
            if 'CITY' in airports_clean.columns:
                coord_cols.append('CITY')
            if 'STATE' in airports_clean.columns:
                coord_cols.append('STATE')
            
            airports_subset = airports_clean[coord_cols].drop_duplicates()
            
            # Hacer merge con aeropuerto de origen
            df = df.merge(
                airports_subset,
                left_on='ORIGIN_AIRPORT',
                right_on='AIRPORT_CODE',
                how='left',
                suffixes=('', '_ORIGIN')
            )
            
            # Renombrar columnas de coordenadas
            if 'LATITUDE' in df.columns:
                df = df.rename(columns={
                    'LATITUDE': 'ORIGIN_LAT',
                    'LONGITUDE': 'ORIGIN_LON'
                })
            
            # Eliminar columna temporal
            if 'AIRPORT_CODE' in df.columns:
                df = df.drop(columns=['AIRPORT_CODE'])
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error en la limpieza de datos: {str(e)}")
        return flights_df


def apply_filters(df, filters):
    """
    Aplica los filtros seleccionados por el usuario al DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame a filtrar
        filters (dict): Diccionario con los filtros a aplicar
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    filtered_df = df.copy()
    
    # Filtro por Mes
    if filters['months'] and len(filters['months']) > 0:
        if 'MONTH' in filtered_df.columns:
            month_nums = [i+1 for i, m in enumerate(['Enero', 'Febrero', 'Marzo', 'Abril', 
                                                      'Mayo', 'Junio', 'Julio', 'Agosto',
                                                      'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']) 
                         if m in filters['months']]
            filtered_df = filtered_df[filtered_df['MONTH'].isin(month_nums)]
    
    # Filtro por Aerolínea
    if filters['airlines'] and len(filters['airlines']) > 0:
        if 'AIRLINE' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['AIRLINE'].isin(filters['airlines'])]
    
    # Filtro por Aeropuerto de Origen
    if filters['origins'] and len(filters['origins']) > 0:
        if 'ORIGIN_AIRPORT' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['ORIGIN_AIRPORT'].isin(filters['origins'])]
    
    return filtered_df


# ==================== FUNCIONES DE VISUALIZACIÓN ====================

def create_airport_map(df):
    """
    Crea un mapa interactivo mostrando aeropuertos con:
    - Tamaño del punto = volumen de vuelos
    - Color = retraso promedio
    
    Args:
        df (pd.DataFrame): DataFrame con datos de vuelos y coordenadas
        
    Returns:
        plotly.graph_objects.Figure: Figura del mapa
    """
    try:
        # Verificar que existan las columnas necesarias
        if not all(col in df.columns for col in ['ORIGIN_LAT', 'ORIGIN_LON', 'ORIGIN_AIRPORT']):
            st.warning("⚠️ No hay datos de coordenadas disponibles para el mapa.")
            return None
        
        # Agrupar por aeropuerto de origen
        airport_stats = df.groupby('ORIGIN_AIRPORT').agg({
            'ORIGIN_LAT': 'first',
            'ORIGIN_LON': 'first',
            'FLIGHT_NUMBER': 'count',  # Volumen de vuelos
            'TOTAL_DELAY': 'mean',  # Retraso promedio
            'CANCELLED': 'sum'  # Total de cancelaciones
        }).reset_index()
        
        airport_stats.columns = ['AIRPORT', 'LAT', 'LON', 'VOLUME', 'AVG_DELAY', 'CANCELLATIONS']
        
        # Eliminar filas con coordenadas nulas
        airport_stats = airport_stats.dropna(subset=['LAT', 'LON'])
        
        if len(airport_stats) == 0:
            st.warning("⚠️ No hay datos válidos para mostrar en el mapa.")
            return None
        
        # Normalizar el tamaño de los puntos
        airport_stats['SIZE'] = airport_stats['VOLUME'] / airport_stats['VOLUME'].max() * 50 + 10
        
        # Crear el mapa con Plotly
        fig = px.scatter_mapbox(
            airport_stats,
            lat='LAT',
            lon='LON',
            size='SIZE',
            color='AVG_DELAY',
            hover_name='AIRPORT',
            hover_data={
                'LAT': False,
                'LON': False,
                'SIZE': False,
                'VOLUME': ':,',
                'AVG_DELAY': ':.1f',
                'CANCELLATIONS': ':,'
            },
            color_continuous_scale='RdYlGn_r',  # Rojo = más retraso, Verde = menos retraso
            size_max=50,
            zoom=3,
            title='Mapa de Aeropuertos: Volumen y Retrasos',
            labels={
                'AVG_DELAY': 'Retraso Promedio (min)',
                'VOLUME': 'Número de Vuelos',
                'CANCELLATIONS': 'Cancelaciones'
            }
        )
        
        # Configurar el estilo del mapa
        fig.update_layout(
            mapbox_style='carto-positron',
            height=600,
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )
        
        return fig
    
    except Exception as e:
        st.error(f"❌ Error al crear el mapa: {str(e)}")
        return None


def create_temporal_heatmap(df):
    """
    Crea un heatmap que cruza Día de la Semana vs Mes
    para identificar patrones temporales de retrasos.
    
    Args:
        df (pd.DataFrame): DataFrame con datos de vuelos
        
    Returns:
        plotly.graph_objects.Figure: Figura del heatmap
    """
    try:
        # Verificar columnas necesarias
        if not all(col in df.columns for col in ['DAY_OF_WEEK', 'MONTH', 'TOTAL_DELAY']):
            st.warning("⚠️ No hay datos suficientes para el análisis temporal.")
            return None
        
        # Crear tabla pivote: Día de Semana (filas) vs Mes (columnas)
        heatmap_data = df.pivot_table(
            values='TOTAL_DELAY',
            index='DAY_OF_WEEK',
            columns='MONTH',
            aggfunc='mean'
        )
        
        # Mapear nombres de días y meses
        day_names = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                      'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        heatmap_data.index = [day_names[i-1] if i <= len(day_names) else f'Día {i}' 
                             for i in heatmap_data.index]
        heatmap_data.columns = [month_names[i-1] if i <= len(month_names) else f'Mes {i}' 
                               for i in heatmap_data.columns]
        
        # Crear el heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn_r',
            text=np.round(heatmap_data.values, 1),
            texttemplate='%{text} min',
            textfont={"size": 10},
            colorbar=dict(title="Retraso<br>Promedio<br>(min)")
        ))
        
        fig.update_layout(
            title='Heatmap: Retrasos por Día de la Semana y Mes',
            xaxis_title='Mes',
            yaxis_title='Día de la Semana',
            height=500,
            xaxis={'side': 'bottom'},
            yaxis={'autorange': 'reversed'}
        )
        
        return fig
    
    except Exception as e:
        st.error(f"❌ Error al crear el heatmap temporal: {str(e)}")
        return None


def create_airline_performance_chart(df):
    """
    Crea gráficos de barras comparando el rendimiento de aerolíneas:
    - % de cancelaciones
    - Retraso promedio
    
    Args:
        df (pd.DataFrame): DataFrame con datos de vuelos
        
    Returns:
        tuple: (fig_cancellations, fig_delays) - Figuras de Plotly
    """
    try:
        # Verificar columnas necesarias
        if 'AIRLINE' not in df.columns:
            st.warning("⚠️ No hay datos de aerolíneas disponibles.")
            return None, None
        
        # Calcular métricas por aerolínea
        airline_stats = df.groupby('AIRLINE').agg({
            'FLIGHT_NUMBER': 'count',
            'CANCELLED': 'sum',
            'TOTAL_DELAY': 'mean'
        }).reset_index()
        
        airline_stats.columns = ['AIRLINE', 'TOTAL_FLIGHTS', 'CANCELLATIONS', 'AVG_DELAY']
        
        # Calcular porcentaje de cancelaciones
        airline_stats['CANCELLATION_RATE'] = (
            airline_stats['CANCELLATIONS'] / airline_stats['TOTAL_FLIGHTS'] * 100
        )
        
        # Ordenar por tasa de cancelación
        airline_stats = airline_stats.sort_values('CANCELLATION_RATE', ascending=True)
        
        # Gráfico 1: % de Cancelaciones
        fig_cancel = px.bar(
            airline_stats,
            x='CANCELLATION_RATE',
            y='AIRLINE',
            orientation='h',
            title='Tasa de Cancelación por Aerolínea',
            labels={
                'CANCELLATION_RATE': 'Porcentaje de Cancelaciones (%)',
                'AIRLINE': 'Aerolínea'
            },
            color='CANCELLATION_RATE',
            color_continuous_scale='Reds',
            text='CANCELLATION_RATE'
        )
        
        fig_cancel.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_cancel.update_layout(height=400, showlegend=False)
        
        # Ordenar por retraso promedio para el segundo gráfico
        airline_stats = airline_stats.sort_values('AVG_DELAY', ascending=True)
        
        # Gráfico 2: Retraso Promedio
        fig_delay = px.bar(
            airline_stats,
            x='AVG_DELAY',
            y='AIRLINE',
            orientation='h',
            title='Retraso Promedio por Aerolínea',
            labels={
                'AVG_DELAY': 'Retraso Promedio (minutos)',
                'AIRLINE': 'Aerolínea'
            },
            color='AVG_DELAY',
            color_continuous_scale='YlOrRd',
            text='AVG_DELAY'
        )
        
        fig_delay.update_traces(texttemplate='%{text:.1f} min', textposition='outside')
        fig_delay.update_layout(height=400, showlegend=False)
        
        return fig_cancel, fig_delay
    
    except Exception as e:
        st.error(f"❌ Error al crear gráficos de aerolíneas: {str(e)}")
        return None, None


def create_cancellation_reason_chart(df):
    """
    Crea un gráfico de pie/donut mostrando las causas de cancelación.
    
    Args:
        df (pd.DataFrame): DataFrame con datos de vuelos
        
    Returns:
        plotly.graph_objects.Figure: Figura del gráfico
    """
    try:
        # Verificar si existe la columna CANCELLATION_REASON
        if 'CANCELLATION_REASON' not in df.columns:
            st.warning("⚠️ No hay datos de causas de cancelación disponibles.")
            return None
        
        # Filtrar solo vuelos cancelados
        cancelled_flights = df[df['CANCELLED'] == 1].copy()
        
        if len(cancelled_flights) == 0:
            st.info("ℹ️ No hay vuelos cancelados en el período seleccionado.")
            return None
        
        # Contar cancelaciones por razón
        cancellation_counts = cancelled_flights['CANCELLATION_REASON'].value_counts()
        
        # Mapear códigos a nombres descriptivos (ajustar según el dataset)
        reason_map = {
            'A': 'Aerolínea/Carrier',
            'B': 'Clima/Weather',
            'C': 'Sistema Aéreo Nacional/NAS',
            'D': 'Seguridad/Security'
        }
        
        cancellation_counts.index = cancellation_counts.index.map(
            lambda x: reason_map.get(x, f'Desconocido ({x})')
        )
        
        # Crear gráfico de dona (donut chart)
        fig = go.Figure(data=[go.Pie(
            labels=cancellation_counts.index,
            values=cancellation_counts.values,
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        
        fig.update_layout(
            title='Distribución de Causas de Cancelación',
            height=400,
            annotations=[dict(text='Causas', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig
    
    except Exception as e:
        st.error(f"❌ Error al crear gráfico de causas de cancelación: {str(e)}")
        return None


# ==================== APLICACIÓN PRINCIPAL ====================

def main():
    """
    Función principal que ejecuta la aplicación de Streamlit.
    """
    
    # ========== HEADER Y INTRODUCCIÓN ==========
    st.title("✈️ Dashboard de Análisis de Retrasos de Vuelos 2015")
    st.markdown("""
    ### 📊 Una Historia sobre la Fiabilidad de los Vuelos
    
    Bienvenido a este análisis interactivo del dataset de retrasos de vuelos de 2015.
    A través de visualizaciones dinámicas, exploraremos **tres dimensiones clave**:
    
    1. **🌍 Contexto Geográfico**: ¿Dónde ocurren los problemas?
    2. **📅 Análisis Temporal**: ¿Cuándo es el peor momento para volar?
    3. **🏢 Rendimiento**: ¿Quién es responsable de los retrasos?
    
    ---
    """)
    
    # ========== BARRA LATERAL: CONFIGURACIÓN Y FILTROS ==========
    st.sidebar.header("⚙️ Configuración")
    
    # Opción para cargar todos los datos
    load_all_data = st.sidebar.checkbox(
        "📊 Cargar TODOS los datos",
        value=False,
        help="⚠️ Cargará el dataset completo (~5.8M vuelos). Puede tardar varios minutos."
    )
    
    if load_all_data:
        st.sidebar.warning("⚠️ Cargando dataset completo. Esto puede tardar 2-5 minutos y usar ~2GB de RAM.")
        sample_size = float('inf')  # Infinito = cargar todo
    else:
        # Control de tamaño de muestra
        sample_size = st.sidebar.slider(
            "Tamaño de muestra (filas)",
            min_value=10000,
            max_value=500000,
            value=100000,
            step=10000,
            help="Número de filas a cargar. Menos filas = más rápido"
        )
    
    # Botón para cargar datos
    if st.sidebar.button("🔄 Cargar/Recargar Datos"):
        st.cache_data.clear()
    
    # ========== CARGA DE DATOS ==========
    with st.spinner('🚀 Cargando y procesando datos...'):
        flights_raw, airports_raw = load_flight_data(sample_size)
    
    # Verificar que los datos se cargaron correctamente
    if flights_raw is None:
        st.error("❌ No se pudieron cargar los datos. Por favor, verifica la instalación de kagglehub.")
        st.stop()
    
    # Limpiar y procesar datos
    with st.spinner('🧹 Limpiando y preparando datos...'):
        df = clean_and_engineer_data(flights_raw, airports_raw)
    
    # ========== FILTROS INTERACTIVOS ==========
    st.sidebar.header("🔍 Filtros")
    
    # Crear diccionario de filtros
    filters = {
        'months': [],
        'airlines': [],
        'origins': []
    }
    
    # Filtro por Mes
    if 'MONTH_NAME' in df.columns:
        all_months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        available_months = [m for m in all_months if m in df['MONTH_NAME'].unique()]
        
        filters['months'] = st.sidebar.multiselect(
            "📅 Seleccionar Meses",
            options=available_months,
            default=[],
            help="Filtra por meses específicos. Vacío = todos los meses"
        )
    
    # Filtro por Aerolínea
    if 'AIRLINE' in df.columns:
        airlines = sorted(df['AIRLINE'].dropna().unique())
        filters['airlines'] = st.sidebar.multiselect(
            "✈️ Seleccionar Aerolíneas",
            options=airlines,
            default=[],
            help="Filtra por aerolíneas específicas. Vacío = todas las aerolíneas"
        )
    
    # Filtro por Aeropuerto de Origen
    if 'ORIGIN_AIRPORT' in df.columns:
        # Mostrar solo los 50 aeropuertos más frecuentes para no saturar
        top_airports = df['ORIGIN_AIRPORT'].value_counts().head(50).index.tolist()
        # Convertir a strings y ordenar
        top_airports_str = [str(x) for x in top_airports]
        filters['origins'] = st.sidebar.multiselect(
            "🛫 Aeropuerto de Origen",
            options=sorted(top_airports_str),
            default=[],
            help="Filtra por aeropuertos de origen. Vacío = todos"
        )
    
    # Aplicar filtros
    df_filtered = apply_filters(df, filters)
    
    # Mostrar métricas generales
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Estadísticas Generales")
    st.sidebar.metric("Total de Vuelos", f"{len(df_filtered):,}")
    
    if 'CANCELLED' in df_filtered.columns:
        total_cancelled = df_filtered['CANCELLED'].sum()
        cancel_rate = (total_cancelled / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        st.sidebar.metric("Vuelos Cancelados", f"{int(total_cancelled):,}", f"{cancel_rate:.2f}%")
    
    if 'TOTAL_DELAY' in df_filtered.columns:
        avg_delay = df_filtered['TOTAL_DELAY'].mean()
        st.sidebar.metric("Retraso Promedio", f"{avg_delay:.1f} min")
    
    # ========== SECCIÓN A: CONTEXTO GEOGRÁFICO ==========
    st.header("🌍 A. Contexto Geográfico: Conectividad y Problemas")
    
    st.markdown("""
    Este mapa interactivo muestra todos los aeropuertos de origen en el dataset.
    - **Tamaño del punto**: Representa el volumen de vuelos desde ese aeropuerto
    - **Color**: Indica el retraso promedio (🔴 Rojo = más retrasos, 🟢 Verde = menos retrasos)
    
    Pasa el cursor sobre los puntos para ver detalles específicos.
    """)
    
    # Crear y mostrar el mapa
    map_fig = create_airport_map(df_filtered)
    if map_fig:
        st.plotly_chart(map_fig, use_container_width=True)
        
        # Análisis geoespacial profesional
        with st.expander("🌍 Análisis Geoespacial: El Corredor Noreste"):
            st.markdown("""
            El mapa revela una **alta densidad de tráfico y retrasos** en la Costa Este, específicamente 
            en el corredor **Nueva York - Washington - Boston**. 
            
            La congestión en estos 'hubs' principales genera un **efecto dominó** que afecta a los vuelos 
            en todo el país. Los aeropuertos más grandes (puntos de mayor tamaño) muestran patrones mixtos:
            
            - ✅ **Ventaja**: Mayor infraestructura y recursos de gestión
            - ⚠️ **Desventaja**: Alta congestión y dependencia meteorológica
            
            Los aeropuertos costeros y en regiones con clima variable (noreste en invierno, sur en verano 
            por tormentas) tienden a mostrar mayores retrasos promedio (tonos rojizos).
            """)
    
    # ========== SECCIÓN B: ANÁLISIS TEMPORAL ==========
    st.header("📅 B. Análisis Temporal: ¿Cuándo Volar?")
    
    st.markdown("""
    Este **heatmap** cruza el día de la semana con el mes del año, permitiendo identificar:
    - 🔥 **Puntos calientes**: Combinaciones de día/mes con mayores retrasos
    - ❄️ **Puntos fríos**: Mejores momentos para volar
    - 🎄 **Estacionalidad**: Patrones relacionados con vacaciones y temporadas altas
    """)
    
    # Crear y mostrar el heatmap
    heatmap_fig = create_temporal_heatmap(df_filtered)
    if heatmap_fig:
        st.plotly_chart(heatmap_fig, use_container_width=True)
        
        # Análisis de patrones estacionales 2015
        st.markdown("### 📅 Patrones Estacionales Detectados")
        st.markdown("""
        **1. El efecto 'Snowmageddon' (Febrero):** Las zonas rojas intensas en febrero coinciden con 
        las tormentas de nieve históricas que paralizaron la Costa Este en 2015. Este fenómeno extremo 
        causó cancelaciones masivas y retrasos en cadena que afectaron a todo el sistema aéreo nacional.
        
        **2. El caos de Verano (Junio-Julio):** Se observa una saturación generalizada debido al alto 
        volumen de turismo vacacional y las tormentas eléctricas convectivas típicas de la tarde. La combinación 
        de mayor demanda y clima inestable crea el escenario perfecto para retrasos acumulativos.
        
        **3. El 'Valle' de Otoño (Septiembre):** Es el **mejor mes para volar** (zonas verdes). El tráfico 
        baja significativamente tras el inicio escolar y el clima es más estable en la mayor parte del país. 
        Los martes y miércoles de septiembre representan la ventana óptima para viajes sin contratiempos.
        
        💡 **Recomendación Elite**: Evita volar viernes de junio-julio y cualquier día de febrero. 
        Prioriza martes/miércoles de septiembre-octubre para máxima puntualidad.
        """)
    
    # ========== SECCIÓN C: RENDIMIENTO DE AEROLÍNEAS ==========
    st.header("🏢 C. Rendimiento: ¿Quién es Responsable?")
    
    st.markdown("""
    En esta sección analizamos el desempeño de las diferentes aerolíneas y las causas
    principales de los problemas operacionales.
    """)
    
    # Insight sobre modelos de negocio
    st.info("""
    ✈️ **Diferencias por Modelo de Negocio**
    
    Los datos muestran dos comportamientos claros según el tipo de aerolínea:
    
    - **Tasa de Cancelación (MQ, EV):** Las aerolíneas regionales como Envoy (MQ) y ExpressJet (EV) 
      tienen las tasas más altas. A menudo actúan como 'fusibles', siendo canceladas primero para 
      proteger los vuelos principales de las grandes compañías (código compartido).
    
    - **Retrasos (NK, F9):** Las aerolíneas Low Cost como Spirit (NK) y Frontier (F9) lideran en 
      minutos de retraso. Sus ajustadas rotaciones de aviones (15-30 min entre vuelos) hacen que un 
      pequeño retraso matutino se acumule exponencialmente durante el día.
    
    - **La excepción (HA):** Hawaiian Airlines tiene un rendimiento casi perfecto al operar en un 
      clima ideal y aislado del tráfico continental. Opera en rutas transpacíficas sin la congestión 
      típica de los hubs continentales.
    """)
    
    # Crear dos columnas para los gráficos de aerolíneas
    col1, col2 = st.columns(2)
    
    fig_cancel, fig_delay = create_airline_performance_chart(df_filtered)
    
    with col1:
        st.subheader("Cancelaciones por Aerolínea")
        if fig_cancel:
            st.plotly_chart(fig_cancel, use_container_width=True)
    
    with col2:
        st.subheader("Retrasos por Aerolínea")
        if fig_delay:
            st.plotly_chart(fig_delay, use_container_width=True)
    
    # Análisis de cancelaciones
    st.markdown("---")
    st.subheader("🔍 Causas de Cancelación")
    
    fig_reasons = create_cancellation_reason_chart(df_filtered)
    if fig_reasons:
        st.plotly_chart(fig_reasons, use_container_width=True)
        
        # Insight clave sobre responsabilidad
        st.warning("""
        💡 **Insight Clave:** Contrario a la creencia popular, la aerolínea solo es responsable directa 
        de aproximadamente el **30%** de las cancelaciones. 
        
        El **Clima (Weather)** es el factor dominante (**>50%**), seguido por problemas del Sistema Aéreo 
        Nacional (congestión de tráfico aéreo y capacidad aeroportuaria limitada).
        """)
        
        st.info("""
        **💡 Desglose de Responsabilidad**:
        
        - **🌧️ Clima (Weather)**: ~50-60% - Tormentas, nieve, niebla. Completamente fuera del control de las aerolíneas. 
          Las cancelaciones preventivas por clima son decisiones de seguridad.
        
        - **✈️ Aerolínea (Carrier)**: ~25-35% - Incluye problemas mecánicos, falta de tripulación, 
          overbook, etc. Esta es la única categoría 100% responsabilidad de la aerolínea.
        
        - **🏢 Sistema Aéreo Nacional (NAS)**: ~10-15% - Control de tráfico aéreo saturado, 
          capacidad aeroportuaria excedida, restricciones de slots.
        
        - **🔒 Seguridad (Security)**: <5% - Incidentes de seguridad, amenazas, inspecciones (muy poco frecuente).
        
        **Conclusión**: Las aerolíneas con altas tasas de cancelación por "Carrier" necesitan mejorar 
        su mantenimiento preventivo, planificación de tripulaciones y gestión de flota.
        """)
    
    # ========== PIE DE PÁGINA ==========
    st.markdown("---")
    st.markdown("""
    ### 📚 Conclusiones Generales
    
    Este análisis interactivo revela que la **fiabilidad de los vuelos** depende de múltiples factores:
    
    1. **Ubicación**: Los aeropuertos en regiones con climas extremos enfrentan más desafíos
    2. **Temporalidad**: Evita volar en temporadas altas (verano/invierno) y fines de semana
    3. **Elección de Aerolínea**: Compara tasas de cancelación y retrasos antes de reservar
    
    **🎯 Recomendación Final**: Para maximizar tus probabilidades de un vuelo puntual:
    - Vuela en **martes o miércoles**
    - Elige **primavera u otoño** (Abril-Mayo o Septiembre-Octubre)
    - Selecciona aerolíneas con **bajas tasas de cancelación**
    - Considera aeropuertos **secundarios** en zonas con mejor clima
    
    ---
    
    *Dashboard creado por Daniel Ariza García | Dataset: USDOT Flight Delays 2015 (Kaggle)*
    """)


# ==================== PUNTO DE ENTRADA ====================
if __name__ == "__main__":
    main()

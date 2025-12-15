import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN DE PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Visualización de Datos de Tráfico Aéreo USA",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CONSTANTES Y CONFIGURACIÓN DE COLORES
# =============================================================================
class ColorScheme:
    """Paleta de colores profesional para el dashboard"""
    PRIMARY = "#2C3E50"          # Azul oscuro corporativo
    SECONDARY = "#34495E"        # Gris azulado
    ACCENT = "#3498DB"           # Azul brillante
    SUCCESS = "#27AE60"          # Verde profesional
    WARNING = "#F39C12"          # Naranja
    DANGER = "#E74C3C"           # Rojo
    INFO = "#5DADE2"             # Azul claro
    LIGHT = "#ECF0F1"            # Gris muy claro
    DARK = "#1A252F"             # Azul muy oscuro
    GRADIENT_START = "#2C3E50"
    GRADIENT_END = "#3498DB"
    
    # Escalas de color para gráficos
    SEQUENTIAL = ['#ECF0F1', '#BDC3C7', '#95A5A6', '#7F8C8D', '#34495E', '#2C3E50']
    DIVERGING = ['#27AE60', '#F39C12', '#E74C3C']

# =============================================================================
# ESTILOS CSS PROFESIONALES
# =============================================================================
st.markdown(f"""
<style>
    /* ========== TEMA GENERAL ========== */
    .main {{
        background: linear-gradient(135deg, {ColorScheme.GRADIENT_START} 0%, {ColorScheme.GRADIENT_END} 100%);
        background-attachment: fixed;
    }}
    
    .block-container {{
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 16px;
        margin: 1rem auto;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    }}
    
    /* ========== TIPOGRAFÍA ========== */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
        font-weight: 600;
        color: {ColorScheme.PRIMARY};
        letter-spacing: -0.5px;
    }}
    
    /* ========== SIDEBAR (monocromo: blanco y negro) ========== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #FFFFFF 0%, #F7F7F7 100%);
        border-right: 1px solid #e6eef6;
    }}
    [data-testid="stSidebar"] .css-1d391kg,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox .css-1v3fvcr,
    [data-testid="stSidebar"] .stSelectbox .css-1d391kg {{
        color: #000000 !important;
    }}
    /* Inputs con fondo blanco y texto oscuro para legibilidad */
    [data-testid="stSidebar"] .stSelectbox select,
    [data-testid="stSidebar"] .stDateInput input,
    [data-testid="stSidebar"] .stMultiSelect input {{
        background: #FFFFFF !important;
        color: #000000 !important;
    }}

    /* ========== TARJETAS KPI: aumentar contraste del emoji/icono ========== */
    .kpi-icon {{
        font-size: 48px;
        position: absolute;
        right: 16px;
        top: 50%;
        transform: translateY(-50%);
        opacity: 0.9;
        color: {ColorScheme.ACCENT};
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12));
    }}
    
    /* ========== PESTAÑAS ========== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: {ColorScheme.LIGHT};
        border-radius: 10px;
        padding: 6px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 48px;
        background: transparent;
        border-radius: 8px;
        color: {ColorScheme.SECONDARY};
        font-weight: 600;
        font-size: 14px;
        border: none;
        padding: 0 24px;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {ColorScheme.PRIMARY}, {ColorScheme.ACCENT});
        color: white !important;
        box-shadow: 0 2px 8px rgba(44, 62, 80, 0.25);
    }}
    
    /* ========== SIDEBAR (asegurar etiquetas en negro) ========== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #FFFFFF 0%, #F7F7F7 100%);
    }}
    
    [data-testid="stSidebar"] .css-1d391kg, 
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label {{
        color: #000000 !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {{
        color: #000000 !important;
        font-weight: 600;
    }}
    
    /* ========== MÉTRICAS NATIVAS ========== */
    [data-testid="stMetricValue"] {{
        font-size: 24px;
        font-weight: 700;
        color: {ColorScheme.PRIMARY};
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {ColorScheme.SECONDARY};
        font-size: 13px;
        font-weight: 600;
    }}
    
    /* ========== ALERTAS Y MENSAJES ========== */
    .stAlert {{
        border-radius: 10px;
        border-left: 4px solid {ColorScheme.ACCENT};
        background: rgba(52, 152, 219, 0.05);
    }}
    
    /* ========== BOTONES ========== */
    .stButton > button {{
        background: linear-gradient(135deg, {ColorScheme.PRIMARY}, {ColorScheme.ACCENT});
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(44, 62, 80, 0.2);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(44, 62, 80, 0.3);
    }}
    
    /* ========== DATAFRAMES ========== */
    .dataframe {{
        font-size: 13px;
        border-radius: 8px;
        overflow: hidden;
    }}
    
    /* ========== EXPANDERS ========== */
    .streamlit-expanderHeader {{
        background: {ColorScheme.LIGHT};
        border-radius: 8px;
        font-weight: 600;
        color: {ColorScheme.PRIMARY};
    }}
    
    /* ========== SEPARADORES ========== */
    hr {{
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, {ColorScheme.LIGHT}, transparent);
    }}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# FUNCIONES DE CARGA Y PROCESAMIENTO
# =============================================================================
@st.cache_data(ttl=3600)
def load_and_clean_data():
    """
    Carga y preprocesa los datos de vuelos con manejo robusto de errores.
    Incluye preprocesamiento del notebook: limpieza de códigos de aeropuerto,
    manejo de valores nulos y formateo de tiempos.
    
    Returns:
        tuple: (flights_df, flights_geo_df, airlines_df) o (None, None, None) si hay error
    """
    try:
        # Carga de archivos
        flights = pd.read_csv('flights.csv')
        airlines = pd.read_csv('airlines.csv')
        airports = pd.read_csv('airports.csv')
        
    except FileNotFoundError as e:
        st.error(f"❌ **Error de carga:** No se encontró el archivo `{e.filename}`")
        return None, None, None
    except Exception as e:
        st.error(f"❌ **Error inesperado:** {str(e)}")
        return None, None, None

    # ========== PREPROCESAMIENTO DEL NOTEBOOK ==========
    
    # 1. CREAR COLUMNA DE FECHA
    flights['DATE'] = pd.to_datetime(flights[['YEAR', 'MONTH', 'DAY']])
    flights['DAY_NAME'] = flights['DATE'].dt.day_name()
    flights['MONTH_NAME'] = flights['DATE'].dt.strftime('%B')
    
    # 2. FUNCIÓN PARA CONVERTIR FORMATO HHMM A CADENA HH:MM
    def format_time(x):
        if pd.isnull(x):
            return np.nan
        if x == 2400:  # Manejar caso borde de medianoche
            return '00:00'
        x = int(x)
        return f"{x // 100:02d}:{x % 100:02d}"
    
    # Aplicar a columnas de tiempo clave
    time_cols = ['SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME']
    for col in time_cols:
        if col in flights.columns:
            flights[col + '_FORMATTED'] = flights[col].apply(format_time)
    
    # 3. MANEJO DE VALORES NULOS
    # Rellenar causas de retraso con 0 (asumimos que si es nulo, no hubo ese tipo de retraso)
    delay_cols = ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
    for col in delay_cols:
        if col in flights.columns:
            flights[col] = flights[col].fillna(0)
    
    # 4. LIMPIEZA DE CÓDIGOS DE AEROPUERTO (Eliminar numéricos si no se pueden mapear)
    # Mantenemos solo los que tienen longitud 3 (IATA codes)
    flights = flights[flights['ORIGIN_AIRPORT'].apply(lambda x: len(str(x)) == 3)]
    flights = flights[flights['DESTINATION_AIRPORT'].apply(lambda x: len(str(x)) == 3)]
    
    # ========== PROCESAMIENTO ADICIONAL ==========
    
    # Ordenamiento de días
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    flights['DAY_NAME'] = pd.Categorical(flights['DAY_NAME'], categories=day_order, ordered=True)

    # 5. MERGE CON AEROLÍNEAS
    flights = flights.merge(airlines, left_on='AIRLINE', right_on='IATA_CODE', how='left')
    # Renombrar columna para evitar duplicados
    flights = flights.rename(columns={'AIRLINE_y': 'AIRLINE_NAME', 'AIRLINE_x': 'AIRLINE_CODE'})
    # Eliminar columna duplicada
    if 'IATA_CODE' in flights.columns:
        flights = flights.drop('IATA_CODE', axis=1)

    # Mapeo de causas de cancelación
    cancellation_map = {
        'A': 'Aerolínea/Operativo',
        'B': 'Clima/Meteorología',
        'C': 'Sistema Nacional (NAS)',
        'D': 'Seguridad'
    }
    flights['CANCELLATION_DESC'] = flights['CANCELLATION_REASON'].map(cancellation_map).fillna('No Cancelado')

    # Datos geográficos (ya filtrados por códigos de 3 caracteres)
    flights_geo = flights.copy()
    flights_geo = flights_geo.merge(
        airports, 
        left_on='ORIGIN_AIRPORT', 
        right_on='IATA_CODE', 
        how='inner'
    )
    
    # Categorías de retraso
    flights['DELAY_CATEGORY'] = pd.cut(
        flights['DEPARTURE_DELAY'], 
        bins=[-np.inf, 0, 15, 60, np.inf],
        labels=['Adelantado', 'A Tiempo', 'Retraso Moderado', 'Retraso Severo']
    )
    
    return flights, flights_geo, airlines

def calculate_kpis(df):
    """
    Calcula los KPIs principales del dashboard.
    
    Args:
        df: DataFrame con los datos de vuelos
        
    Returns:
        dict: Diccionario con los KPIs calculados
    """
    total_flights = len(df)
    
    if total_flights == 0:
        return {
            'total_flights': 0,
            'cancelled_count': 0,
            'cancel_rate': 0,
            'avg_dep_delay': 0,
            'on_time_pct': 0
        }
    
    cancelled_count = df['CANCELLED'].sum()
    cancel_rate = (cancelled_count / total_flights) * 100
    avg_dep_delay = df['DEPARTURE_DELAY'].mean()
    on_time_pct = (len(df[df['DEPARTURE_DELAY'] < 15]) / total_flights) * 100
    
    return {
        'total_flights': total_flights,
        'cancelled_count': cancelled_count,
        'cancel_rate': cancel_rate,
        'avg_dep_delay': avg_dep_delay,
        'on_time_pct': on_time_pct
    }

def create_kpi_card(title, value, note, icon):
    """
    Genera HTML para una tarjeta KPI.
    
    Args:
        title: Título del KPI
        value: Valor principal a mostrar
        note: Nota descriptiva
        icon: Emoji/icono a mostrar
        
    Returns:
        str: HTML de la tarjeta
    """
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """

# =============================================================================
# CARGA DE DATOS
# =============================================================================
df, df_geo, airlines_ref = load_and_clean_data()

if df is None:
    st.error("⚠️ **Error Crítico:** No se pudieron cargar los archivos de datos. Verifica que existan en el directorio.")
    st.stop()

# =============================================================================
# SIDEBAR - PANEL DE CONTROL
# =============================================================================
with st.sidebar:
    st.markdown("## Panel de Control")
    st.markdown("---")
    
    # Filtro de fecha
    date_range = st.date_input(
        "📅 Rango de Fechas",
        value=(df['DATE'].min(), df['DATE'].max()),
        min_value=df['DATE'].min(),
        max_value=df['DATE'].max()
    )
    
    # Filtro de aerolíneas
    airlines_list = ['Todas'] + sorted(df['AIRLINE_NAME'].dropna().unique().tolist())
    selected_airline = st.selectbox("✈️ Aerolínea", airlines_list)
    
    # Filtro de estado
    flight_status = st.multiselect(
        "📊 Estado del Vuelo",
        ['Operado', 'Cancelado'],
        default=['Operado', 'Cancelado']
    )
    
    st.markdown("---")
    st.markdown("### 📈 Estadísticas Generales")
    
    # Aplicar filtros
    df_filtered = df.copy()
    
    # Filtro de fecha
    if len(date_range) == 2:
        df_filtered = df_filtered[
            (df_filtered['DATE'] >= pd.to_datetime(date_range[0])) & 
            (df_filtered['DATE'] <= pd.to_datetime(date_range[1]))
        ]
    
    # Filtro de aerolínea
    if selected_airline != 'Todas':
        df_filtered = df_filtered[df_filtered['AIRLINE_NAME'] == selected_airline]
    
    # Filtro de estado
    status_filter = []
    if 'Operado' in flight_status:
        status_filter.append(0)
    if 'Cancelado' in flight_status:
        status_filter.append(1)
    
    if status_filter:
        df_filtered = df_filtered[df_filtered['CANCELLED'].isin(status_filter)]
    
    # Mini métricas en sidebar
    st.metric("Vuelos Filtrados", f"{len(df_filtered):,}")
    st.metric("Aeropuertos Únicos", df_filtered['ORIGIN_AIRPORT'].nunique())
    
    if len(df_filtered) > 0:
        days_range = (df_filtered['DATE'].max() - df_filtered['DATE'].min()).days
        st.metric("Período", f"{days_range} días")

# =============================================================================
# HEADER PRINCIPAL
# =============================================================================
st.markdown(f"""
<div style='text-align: center; padding: 30px 0 20px 0;'>
    <h1 style='font-size: 46px; margin-bottom: 10px; color: {ColorScheme.PRIMARY};'>
        ✈️ Visualización de Datos de Tráfico Aéreo USA
    </h1>
    <p style='font-size: 17px; color: {ColorScheme.SECONDARY}; font-weight: 500;'>
        Análisis Integral del Tráfico Aéreo en Estados Unidos
    </p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# PESTAÑAS PRINCIPALES
# =============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Resumen Ejecutivo", 
    "📅 Análisis Temporal", 
    "🏆 Ranking Aerolíneas", 
    "🗺️ Geografía Operativa",
    "🔍 Análisis Detallado"
])

# =============================================================================
# TAB 1: DASHBOARD EJECUTIVO
# =============================================================================
with tab1:
    st.markdown("### 📈 Indicadores Clave de Rendimiento")
    
    # Calcular KPIs
    kpis = calculate_kpis(df_filtered)
    
    # Mostrar tarjetas KPI
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            create_kpi_card(
                "Operaciones Totales",
                f"{kpis['total_flights']:,}",
                "Vuelos procesados",
                "📊"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_kpi_card(
                "Puntualidad",
                f"{kpis['on_time_pct']:.1f}%",
                "Retraso < 15 minutos",
                "✅"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_kpi_card(
                "Retraso Promedio",
                f"{kpis['avg_dep_delay']:.1f}m",
                "Tiempo de espera",
                "⏱️"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            create_kpi_card(
                "Cancelaciones",
                f"{kpis['cancel_rate']:.2f}%",
                f"{kpis['cancelled_count']:,} vuelos",
                "❌"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos principales
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### 📈 Evolución Temporal del Tráfico")
        daily_flights = df_filtered.groupby('DATE').size().reset_index(name='Vuelos')
        
        fig_trend = px.area(
            daily_flights, 
            x='DATE', 
            y='Vuelos',
            template='plotly_white'
        )
        fig_trend.update_traces(
            line_color=ColorScheme.ACCENT,
            fillcolor=f'rgba(52, 152, 219, 0.2)'
        )
        fig_trend.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="",
            yaxis_title="Número de Vuelos",
            font=dict(family="Inter, sans-serif", size=12, color=ColorScheme.SECONDARY),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(fig_trend, width="stretch")
    
    with col_right:
        st.markdown("#### 🎯 Distribución por Estado de Retraso")
        delay_dist = df_filtered['DELAY_CATEGORY'].value_counts().reset_index()
        delay_dist.columns = ['Categoría', 'Cantidad']
        
        # Mostrar como barras horizontales para mejor comparación (no tarta)
        order = ['Adelantado', 'A Tiempo', 'Retraso Moderado', 'Retraso Severo']
        delay_dist['Categoría'] = pd.Categorical(delay_dist['Categoría'], categories=order, ordered=True)
        delay_dist = delay_dist.sort_values('Categoría')
        
        color_map = {
            'Adelantado': ColorScheme.SUCCESS,
            'A Tiempo': ColorScheme.ACCENT,
            'Retraso Moderado': ColorScheme.WARNING,
            'Retraso Severo': ColorScheme.DANGER
        }
        delay_dist['color'] = delay_dist['Categoría'].map(color_map)
        
        fig_bar_delay = px.bar(
            delay_dist,
            x='Cantidad',
            y='Categoría',
            orientation='h',
            color='Categoría',
            color_discrete_map=color_map,
            text='Cantidad'
        )
        fig_bar_delay.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_bar_delay.update_layout(
            height=300,
            margin=dict(l=0, r=20, t=10, b=0),
            xaxis_title="Número de Vuelos",
            yaxis_title="Estado de Retraso",
            showlegend=False,
            template='plotly_white',
            font=dict(family="Inter, sans-serif", size=12, color=ColorScheme.SECONDARY)
        )
        st.plotly_chart(fig_bar_delay, width="stretch")
    
    # Comparativa Día de la Semana
    st.markdown("#### 📅 Rendimiento por Día de la Semana")
    
    day_stats = df_filtered.groupby('DAY_NAME').agg({
        'FLIGHT_NUMBER': 'count',
        'DEPARTURE_DELAY': 'mean',
        'CANCELLED': 'sum'
    }).reset_index()
    day_stats.columns = ['Día', 'Vuelos', 'Retraso Promedio', 'Cancelados']
    
    fig_days = go.Figure()
    
    fig_days.add_trace(go.Bar(
        x=day_stats['Día'],
        y=day_stats['Vuelos'],
        name='Número de Vuelos',
        marker_color=ColorScheme.ACCENT,
        yaxis='y'
    ))
    
    fig_days.add_trace(go.Scatter(
        x=day_stats['Día'],
        y=day_stats['Retraso Promedio'],
        name='Retraso Promedio (min)',
        line=dict(color=ColorScheme.DANGER, width=3),
        yaxis='y2',
        mode='lines+markers'
    ))
    
    fig_days.update_layout(
        yaxis=dict(
            title=dict(
                text='Número de Vuelos',
                font=dict(color=ColorScheme.ACCENT)
            ),
            tickfont=dict(color=ColorScheme.ACCENT)
        ),
        yaxis2=dict(
            title=dict(
                text='Retraso Promedio (minutos)',
                font=dict(color=ColorScheme.DANGER)
            ),
            tickfont=dict(color=ColorScheme.DANGER),
            overlaying='y',
            side='right'
        ),
        legend=dict(
            x=0.5,
            y=1.15,
            xanchor='center',
            orientation='h',
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        height=400,
        hovermode='x unified',
        template='plotly_white',
        font=dict(family="Inter, sans-serif", size=12, color=ColorScheme.SECONDARY),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig_days, width="stretch")

# =============================================================================
# TAB 2: ANÁLISIS TEMPORAL
# =============================================================================
with tab2:
    st.markdown("### ⏱️ Patrones de Congestión y Eficiencia Temporal")
    
    # Mapa de calor
    heatmap_data = df_filtered.groupby(['MONTH', 'DAY_NAME'])['DEPARTURE_DELAY'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='DAY_NAME', columns='MONTH', values='DEPARTURE_DELAY')
    
    fig_heat = px.imshow(
        heatmap_pivot,
        labels=dict(x="Mes", y="Día de la Semana", color="Retraso (min)"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        color_continuous_scale=[[0, ColorScheme.SUCCESS], [0.5, ColorScheme.WARNING], [1, ColorScheme.DANGER]],
        aspect="auto",
        text_auto=".1f"
    )
    fig_heat.update_layout(
        title={
            'text': '<b>Mapa de Calor: Retrasos Promedio por Mes y Día</b>',
            'font': {'size': 18, 'color': ColorScheme.PRIMARY}
        },
        height=500,
        font=dict(family="Inter, sans-serif", size=12, color=ColorScheme.SECONDARY)
    )
    st.plotly_chart(fig_heat, width="stretch")
    
    # Análisis por hora
    if 'SCHEDULED_DEPARTURE' in df_filtered.columns:
        st.markdown("#### ⏰ Distribución Horaria de Operaciones")
        
        df_filtered['HOUR'] = pd.to_datetime(
            df_filtered['SCHEDULED_DEPARTURE'], 
            format='%H%M', 
            errors='coerce'
        ).dt.hour
        
        hourly = df_filtered.groupby('HOUR').size().reset_index(name='Vuelos')
        
        fig_hour = px.bar(
            hourly, 
            x='HOUR', 
            y='Vuelos',
            color='Vuelos',
            color_continuous_scale=[[0, ColorScheme.SUCCESS], [1, ColorScheme.WARNING]]
        )
        fig_hour.update_layout(
            height=350,
            xaxis_title="Hora del Día (24h)",
            yaxis_title="Número de Vuelos",
            showlegend=False,
            template='plotly_white',
            font=dict(family="Inter, sans-serif", size=12, color=ColorScheme.SECONDARY)
        )
        st.plotly_chart(fig_hour, width="stretch")

# =============================================================================
# TAB 3: RANKING AEROLÍNEAS
# =============================================================================
with tab3:
    st.markdown("### 🏆 Análisis Competitivo de Aerolíneas")
    
    # Métricas por aerolínea
    airline_metrics = df_filtered.groupby('AIRLINE_NAME').agg({
        'FLIGHT_NUMBER': 'count',
        'DEPARTURE_DELAY': 'mean',
        'CANCELLED': ['sum', 'mean']
    }).reset_index()
    
    airline_metrics.columns = ['Aerolínea', 'Total Vuelos', 'Retraso Promedio', 'Cancelados', 'Tasa Cancelación']
    airline_metrics['Tasa Cancelación'] = airline_metrics['Tasa Cancelación'] * 100
    airline_metrics = airline_metrics[airline_metrics['Total Vuelos'] >= 10]  # Filtrar aerolíneas con pocos vuelos
    airline_metrics = airline_metrics.sort_values('Total Vuelos', ascending=False).head(15)
    
    # Gráfico alternativo: barras horizontales por retraso promedio, coloreadas por tasa de cancelación
    st.markdown("#### 📊 Rendimiento por Aerolínea: Retraso vs Tasa de Cancelación")
    perf = airline_metrics.copy()
    perf = perf.sort_values('Retraso Promedio', ascending=True)
    fig_perf = px.bar(
        perf,
        x='Retraso Promedio',
        y='Aerolínea',
        orientation='h',
        color='Tasa Cancelación',
        color_continuous_scale=['#27AE60', '#F39C12', '#E74C3C'],  # verde -> amarillo -> rojo
        hover_data={'Total Vuelos': True, 'Retraso Promedio': ':.1f', 'Tasa Cancelación': ':.2f'},
        labels={'Retraso Promedio': 'Retraso Promedio (min)', 'Tasa Cancelación': 'Tasa de Cancelación (%)'}
    )
    # Asegurar que la aerolínea con menor retraso quede arriba
    fig_perf.update_layout(
        height=520,
        margin=dict(l=0, r=10, t=10, b=10),
        template='plotly_white',
        font=dict(family="Inter, sans-serif", size=12, color=ColorScheme.SECONDARY)
    )
    # Forzar orden para que el menor retraso aparezca arriba
    fig_perf.update_yaxes(categoryorder='array', categoryarray=list(perf['Aerolínea'][::-1]))
    st.plotly_chart(fig_perf, width="stretch")
    
    st.info("💡 **Interpretación:** Las aerolíneas en la esquina inferior izquierda tienen mejor rendimiento (menos retrasos y cancelaciones)")
    
    # Rankings mejorados
    st.markdown("#### 🎯 Rankings de Rendimiento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🥇 Top 5 - Mejor Puntualidad")
        st.markdown("<div style='font-size: 12px; color: #7F8C8D; margin-bottom: 10px;'>Aerolíneas con menor retraso promedio</div>", unsafe_allow_html=True)
        
        top_punctual = airline_metrics.nsmallest(5, 'Retraso Promedio')[['Aerolínea', 'Retraso Promedio', 'Total Vuelos']].reset_index(drop=True)
        top_punctual.index = top_punctual.index + 1
        top_punctual.index.name = 'Posición'
        top_punctual['Retraso Promedio'] = top_punctual['Retraso Promedio'].round(1)
        top_punctual['Total Vuelos'] = top_punctual['Total Vuelos'].astype(int)

        # Mostrar tabla compacta con formato
        st.table(top_punctual.style.format({
            'Retraso Promedio': '{:.1f} min',
            'Total Vuelos': '{:,}'
        }))
        
        # Gráfico horizontal para Top 5 (mejor puntualidad)
        fig_top = px.bar(
            top_punctual.sort_values('Retraso Promedio', ascending=False),
            x='Retraso Promedio',
            y='Aerolínea',
            orientation='h',
            text='Retraso Promedio',
            color='Retraso Promedio',
            color_continuous_scale=[ColorScheme.ACCENT, ColorScheme.DANGER],
            labels={'Retraso Promedio': 'Retraso (min)'
        })
        fig_top.update_traces(texttemplate='%{text:.1f} min', textposition='outside', marker_line_color='rgba(0,0,0,0.06)')
        fig_top.update_layout(height=320, margin=dict(l=0, r=10, t=8, b=8), xaxis_title='Retraso Promedio (min)', yaxis_title='')
        st.plotly_chart(fig_top, width="stretch")
        
    with col2:
        st.markdown("##### 🔴 Top 5 - Mayor Retraso")
        st.markdown("<div style='font-size: 12px; color: #7F8C8D; margin-bottom: 10px;'>Aerolíneas con mayor retraso promedio</div>", unsafe_allow_html=True)

        worst_punctual = airline_metrics.nlargest(5, 'Retraso Promedio')[['Aerolínea', 'Retraso Promedio', 'Total Vuelos']].reset_index(drop=True)
        worst_punctual.index = worst_punctual.index + 1
        worst_punctual.index.name = 'Posición'
        worst_punctual['Retraso Promedio'] = worst_punctual['Retraso Promedio'].round(1)
        worst_punctual['Total Vuelos'] = worst_punctual['Total Vuelos'].astype(int)

        # Mostrar tabla
        st.table(worst_punctual.style.format({
            'Retraso Promedio': '{:.1f} min',
            'Total Vuelos': '{:,}'
        }))

        # Gráfico horizontal para Top 5 peor puntualidad
        fig_worst = px.bar(
            worst_punctual.sort_values('Retraso Promedio', ascending=True),
            x='Retraso Promedio',
            y='Aerolínea',
            orientation='h',
            text='Retraso Promedio',
            color='Retraso Promedio',
            color_continuous_scale=[ColorScheme.ACCENT, ColorScheme.DANGER],
            labels={'Retraso Promedio': 'Retraso (min)'
        })
        fig_worst.update_traces(texttemplate='%{text:.1f} min', textposition='inside', textfont=dict(color='white'), marker_line_color='rgba(0,0,0,0.06)')
        fig_worst.update_layout(height=320, margin=dict(l=0, r=10, t=8, b=8), xaxis_title='Retraso Promedio (min)', yaxis_title='')
        st.plotly_chart(fig_worst, width="stretch")

    # Expander con matriz completa
    with st.expander("Ver Matriz Completa de Rendimiento"):
        st.dataframe(
            airline_metrics.sort_values('Retraso Promedio').style.background_gradient(subset=['Retraso Promedio'], cmap='Blues'),
            width="stretch"
        )

# =============================================================================
# TAB 4: MAPA GEOGRÁFICO
# =============================================================================
with tab4:
    st.markdown("### 🗺️ Red de Operaciones y Hubs Principales")

    if df_geo is not None and not df_geo.empty:
        map_data = df_geo.groupby(['ORIGIN_AIRPORT', 'LATITUDE', 'LONGITUDE', 'AIRPORT', 'CITY']).agg({
            'FLIGHT_NUMBER': 'count',
            'DEPARTURE_DELAY': 'mean'
        }).reset_index()
        map_data.columns = ['Código', 'Latitud', 'Longitud', 'Aeropuerto', 'Ciudad', 'Vuelos', 'Retraso Promedio']

        map_data['Tamaño'] = np.log1p(map_data['Vuelos']) * 8

        # Color: verde (bajo retraso) -> amarillo -> rojo (alto retraso)
        fig_map = px.scatter_mapbox(
            map_data,
            lat="Latitud",
            lon="Longitud",
            hover_name="Aeropuerto",
            hover_data={"Ciudad": True, "Vuelos": ':,', "Retraso Promedio": ':.1f'},
            size="Tamaño",
            color="Retraso Promedio",
            color_continuous_scale=['#27AE60', '#F39C12', '#E74C3C'],
            size_max=40,
            opacity=0.9,
            zoom=3.5,
            mapbox_style="carto-positron"
        )
        fig_map.update_layout(height=650, margin=dict(l=0, r=0, t=0, b=0), coloraxis_colorbar=dict(title="Retraso (min)"))
        st.plotly_chart(fig_map, width="stretch")

        st.markdown("#### 🏢 Top 10 Aeropuertos por Volumen")
        top_airports = map_data.nlargest(10, 'Vuelos')[['Aeropuerto', 'Ciudad', 'Vuelos', 'Retraso Promedio']]
        st.dataframe(top_airports.style.format({'Vuelos': '{:,}', 'Retraso Promedio': '{:.1f}'}), width="stretch")
    else:
        st.warning("⚠️ No hay datos geográficos disponibles para la selección actual")

# =============================================================================
# TAB 5: ANÁLISIS DETALLADO
# =============================================================================
with tab5:
    st.markdown("### 🔍 Exploración Avanzada de Datos")

    analysis_type = st.radio(
        "Selecciona el tipo de análisis:",
        ["Causas de Cancelación", "Distribución de Distancias", "Análisis de Rutas"]
    )

    if analysis_type == "Causas de Cancelación":
        cancelled_df = df_filtered[df_filtered['CANCELLED'] == 1]
        if not cancelled_df.empty:
            causes = cancelled_df['CANCELLATION_DESC'].value_counts().reset_index()
            causes.columns = ['Causa', 'Cantidad']
            causes['Porcentaje'] = (causes['Cantidad'] / causes['Cantidad'].sum() * 100).round(2)

            fig = px.bar(
                causes,
                x='Cantidad',
                y='Causa',
                orientation='h',
                text='Porcentaje',
                color='Cantidad',
                color_continuous_scale=['#27AE60', '#F39C12', '#E74C3C']
                                
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=420, showlegend=False, margin=dict(l=0, r=0, t=10, b=10))
            st.plotly_chart(fig, width="stretch")
        else:
            st.success("✅ No hay cancelaciones en el período seleccionado")

    elif analysis_type == "Distribución de Distancias":
        if 'DISTANCE' in df_filtered.columns:
            fig = px.histogram(
                df_filtered,
                x='DISTANCE',
                nbins=50,
                color_discrete_sequence=[ColorScheme.ACCENT]
            )
            fig.update_layout(height=420, xaxis_title="Distancia (millas)", yaxis_title="Frecuencia", template='plotly_white')
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No hay columna 'DISTANCE' en el dataset.")

    else:  # Análisis de Rutas
        if 'ORIGIN_AIRPORT' in df_filtered.columns and 'DESTINATION_AIRPORT' in df_filtered.columns:
            routes = df_filtered.groupby(['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']).size().reset_index(name='Vuelos')
            routes = routes.nlargest(20, 'Vuelos')
            routes['Ruta'] = routes['ORIGIN_AIRPORT'] + ' → ' + routes['DESTINATION_AIRPORT']

            fig = px.bar(
                routes.sort_values('Vuelos'),
                x='Vuelos',
                y='Ruta',
                orientation='h',
                color='Vuelos',
                color_continuous_scale=["#1D23D2", "#4EADF0", "#24ECC7"]
            )
            fig.update_layout(height=600, showlegend=False, template='plotly_white')
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("No están disponibles las columnas de origen/destino para el análisis de rutas.")

    with st.expander("📋 Ver Datos Crudos (Primeras 100 filas)"):
        st.dataframe(df_filtered.head(100), width="stretch")

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 12px; color: {ColorScheme.SECONDARY};'>
    Visualización de Datos de Tráfico Aéreo USA | Por Javier, Daniel y Carlos {datetime.now().year}
</div>
""", unsafe_allow_html=True)
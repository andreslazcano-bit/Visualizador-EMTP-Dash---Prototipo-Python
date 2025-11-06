"""
============================================================================
LAYOUT DE MAPA DE CHILE - MATRÍCULA Y ESTABLECIMIENTOS
============================================================================
Visualización geográfica de la distribución de matrícula y establecimientos EMTP
Usa choroplethmapbox con GeoJSON de fcortes/Chile-GeoJSON
Soporta visualización a nivel regional y comunal
"""

import json
import urllib.request
from functools import lru_cache
import pandas as pd
import plotly.express as px
from dash import dcc, html
import dash_bootstrap_components as dbc

# URLs de GeoJSON
REGIONAL_GEOJSON_URL = "https://raw.githubusercontent.com/fcortes/Chile-GeoJSON/master/Regional.geojson"
COMUNAL_GEOJSON_URL = "https://raw.githubusercontent.com/fcortes/Chile-GeoJSON/master/comunas.geojson"
DATA_PATH = "data/processed/matricula_comunal_simulada.csv"

# Escalas de colores personalizadas del proyecto
# Basadas en la paleta institucional del CSS
# Escala para Matrícula: de claro a oscuro con más contraste
COLOR_SCALE_MATRICULA = [
    [0.0, '#E8EEF2'],   # Muy claro (gris azulado)
    [0.25, '#5A6E79'],  # secondary-color (gris azulado)
    [0.5, '#34536A'],   # primary-color (azul oscuro)
    [0.75, '#2A4255'],  # tertiary-color (azul muy oscuro)
    [1.0, '#1e293b']    # Negro azulado (valores máximos)
]

# Escala para Establecimientos: de claro a cálido con más contraste
COLOR_SCALE_ESTABLECIMIENTOS = [
    [0.0, '#FFFFFF'],   # Blanco puro (sin establecimientos)
    [0.2, '#F4F6F7'],   # neutral-color (gris muy claro)
    [0.4, '#C2A869'],   # accent-yellow (dorado)
    [0.7, '#B35A5A'],   # accent-color (rojo institucional)
    [1.0, '#8B3A3A']    # Rojo oscuro (muchos establecimientos)
]

@lru_cache(maxsize=2)
def get_chile_geojson():
    """
    Carga el GeoJSON de Chile por regiones desde GitHub.
    """
    with urllib.request.urlopen(REGIONAL_GEOJSON_URL) as response:
        return json.loads(response.read().decode('utf-8'))

@lru_cache(maxsize=2)
def get_comunas_geojson():
    """
    Carga el GeoJSON de comunas desde GitHub.
    """
    with urllib.request.urlopen(COMUNAL_GEOJSON_URL) as response:
        return json.loads(response.read().decode('utf-8'))

def create_chile_map():
    """
    Crea el mapa de Chile por regiones con matrícula.
    """
    # Cargar GeoJSON
    geojson = get_chile_geojson()
    
    # Cargar datos de matrícula
    df = pd.read_csv(DATA_PATH)
    
    # Extraer código de región correctamente del cod_comuna
    # Si el código es >= 10000, la región son los primeros 2 dígitos
    # Si es < 10000, la región es el primer dígito
    def get_region_code(cod_comuna):
        cod_str = str(cod_comuna)
        if len(cod_str) == 5:  # códigos como 15201
            return int(cod_str[:2])
        else:  # códigos como 2302
            return int(cod_str[0])
    
    df['codregion'] = df['cod_comuna'].apply(get_region_code)
    
    # Agrupar por región
    df_regiones = df.groupby('codregion').agg({
        'matricula_total': 'sum',
        'region': 'first'
    }).reset_index()
    
    # Crear mapa
    fig = px.choropleth_mapbox(
        df_regiones,
        geojson=geojson,
        locations='codregion',
        featureidkey="properties.codregion",
        color='matricula_total',
        color_continuous_scale=COLOR_SCALE_MATRICULA,
        range_color=[df_regiones['matricula_total'].min(), df_regiones['matricula_total'].max()],
        hover_name='region',
        hover_data={
            'codregion': False,
            'matricula_total': ':,'
        },
        labels={'matricula_total': 'Matrícula Total'},
        zoom=3.2,
        center={"lat": -35, "lon": -71},
        mapbox_style='open-street-map',
        opacity=0.7
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600
    )
    
    return fig

def create_chile_comunas_map():
    """
    Crea el mapa de Chile por comunas con matrícula.
    """
    # Cargar GeoJSON
    geojson = get_comunas_geojson()
    
    # Cargar datos de matrícula
    df_raw = pd.read_csv(DATA_PATH)
    
    # Agrupar por comuna
    df = df_raw.groupby(['cod_comuna', 'comuna', 'region']).agg({
        'matricula_total': 'sum'
    }).reset_index()
    
    # Asegurar que cod_comuna es int (para hacer match con el GeoJSON)
    df['cod_comuna'] = df['cod_comuna'].astype(int)
    
    # Crear figura de choropleth
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='cod_comuna',
        featureidkey="properties.cod_comuna",
        color='matricula_total',
        color_continuous_scale=COLOR_SCALE_MATRICULA,
        range_color=[df['matricula_total'].min(), df['matricula_total'].max()],
        hover_name='comuna',
        hover_data={
            'cod_comuna': False,
            'region': True,
            'matricula_total': ':,',
        },
        labels={
            'matricula_total': 'Matrícula Total',
            'region': 'Región'
        },
        zoom=3.5,
        center={"lat": -35, "lon": -71},
        mapbox_style='open-street-map',
        opacity=0.7
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600
    )
    
    return fig

def create_establecimientos_map():
    """
    Crea el mapa de establecimientos EMTP (choropleth por comuna).
    """
    # Cargar GeoJSON
    geojson = get_chile_geojson()
    
    # Cargar datos
    df = pd.read_csv(DATA_PATH)
    
    # Extraer código de región
    def get_region_code(cod_comuna):
        cod_str = str(cod_comuna)
        if len(cod_str) == 5:
            return int(cod_str[:2])
        else:
            return int(cod_str[0])
    
    df['codregion'] = df['cod_comuna'].apply(get_region_code)
    
    # Agrupar por región y estimar establecimientos
    df_regiones = df.groupby('codregion').agg({
        'region': 'first',
        'matricula_total': 'sum'
    }).reset_index()
    
    # Estimar número de establecimientos (aproximadamente 1 por cada 100 estudiantes)
    df_regiones['establecimientos'] = (df_regiones['matricula_total'] / 100).apply(lambda x: max(1, int(x)))
    
    # Crear mapa choropleth
    fig = px.choropleth_mapbox(
        df_regiones,
        geojson=geojson,
        locations='codregion',
        featureidkey="properties.codregion",
        color='establecimientos',
        color_continuous_scale=COLOR_SCALE_ESTABLECIMIENTOS,
        range_color=[df_regiones['establecimientos'].min(), df_regiones['establecimientos'].max()],
        hover_name='region',
        hover_data={
            'codregion': False,
            'establecimientos': True,
            'matricula_total': ':,'
        },
        labels={
            'establecimientos': 'N° Establecimientos',
            'matricula_total': 'Matrícula Total'
        },
        zoom=3.2,
        center={"lat": -35, "lon": -71},
        mapbox_style='open-street-map',
        opacity=0.7
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600
    )
    
    return fig

def create_establecimientos_comunas_map():
    """
    Crea el mapa de establecimientos por comuna.
    """
    # Cargar GeoJSON
    geojson = get_comunas_geojson()
    
    # Cargar datos
    df_raw = pd.read_csv(DATA_PATH)
    
    # Agrupar por comuna
    df = df_raw.groupby(['cod_comuna', 'comuna', 'region']).agg({
        'matricula_total': 'sum'
    }).reset_index()
    
    # Asegurar que cod_comuna es int
    df['cod_comuna'] = df['cod_comuna'].astype(int)
    
    # Estimar establecimientos
    df['establecimientos'] = (df['matricula_total'] / 100).apply(lambda x: max(1, int(x)))
    
    # Crear mapa choropleth
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='cod_comuna',
        featureidkey="properties.cod_comuna",
        color='establecimientos',
        color_continuous_scale=COLOR_SCALE_ESTABLECIMIENTOS,
        range_color=[df['establecimientos'].min(), df['establecimientos'].max()],
        hover_name='comuna',
        hover_data={
            'cod_comuna': False,
            'region': True,
            'establecimientos': True,
            'matricula_total': ':,'
        },
        labels={
            'establecimientos': 'N° Establecimientos',
            'matricula_total': 'Matrícula Total',
            'region': 'Región'
        },
        zoom=3.5,
        center={"lat": -35, "lon": -71},
        mapbox_style='open-street-map',
        opacity=0.7
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600
    )
    
    return fig

def create_tabla_resumen_matricula(granularidad='regional'):
    """
    Crea tabla resumen de matrícula por territorio.
    
    Args:
        granularidad: 'regional' o 'comunal'
    """
    df = pd.read_csv(DATA_PATH)
    
    if granularidad == 'regional':
        # Resumen por región
        df_resumen = df.groupby('region').agg({
            'matricula_total': 'sum',
            'comuna': 'nunique'
        }).reset_index()
        df_resumen.columns = ['Región', 'Matrícula Total', 'N° Comunas']
        df_resumen = df_resumen.sort_values('Matrícula Total', ascending=False)
        
    else:  # comunal
        # Resumen por comuna (top 20)
        df_resumen = df.groupby(['region', 'comuna']).agg({
            'matricula_total': 'sum'
        }).reset_index()
        df_resumen.columns = ['Región', 'Comuna', 'Matrícula Total']
        df_resumen = df_resumen.sort_values('Matrícula Total', ascending=False).head(20)
    
    # Formatear números
    for col in df_resumen.columns:
        if 'Total' in col or 'N°' in col:
            df_resumen[col] = df_resumen[col].apply(lambda x: f"{int(x):,}")
    
    # Crear tabla HTML
    tabla = dbc.Table.from_dataframe(
        df_resumen,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        className="mb-0"
    )
    
    return tabla

def create_tabla_resumen_establecimientos(granularidad='regional'):
    """
    Crea tabla resumen de establecimientos por territorio.
    
    Args:
        granularidad: 'regional' o 'comunal'
    """
    df = pd.read_csv(DATA_PATH)
    
    # Estimar establecimientos (1 por cada 100 estudiantes aprox)
    df_est = df.groupby(['region', 'comuna', 'cod_comuna']).agg({
        'matricula_total': 'sum'
    }).reset_index()
    df_est['establecimientos'] = (df_est['matricula_total'] / 100).apply(lambda x: max(1, int(x)))
    
    if granularidad == 'regional':
        # Resumen por región
        df_resumen = df_est.groupby('region').agg({
            'establecimientos': 'sum',
            'matricula_total': 'sum',
            'comuna': 'nunique'
        }).reset_index()
        df_resumen['promedio'] = (df_resumen['matricula_total'] / df_resumen['establecimientos']).astype(int)
        df_resumen = df_resumen.sort_values('establecimientos', ascending=False)
        
        # Formatear
        df_resumen.columns = ['Región', 'N° Establecimientos', 'Matrícula Total', 'N° Comunas', 'Promedio Mat./Estab.']
        for col in ['N° Establecimientos', 'Matrícula Total', 'N° Comunas', 'Promedio Mat./Estab.']:
            df_resumen[col] = df_resumen[col].apply(lambda x: f"{int(x):,}")
        
    else:  # comunal
        # Resumen por comuna (top 20)
        df_resumen = df_est.groupby(['region', 'comuna']).agg({
            'establecimientos': 'sum',
            'matricula_total': 'sum'
        }).reset_index()
        df_resumen = df_resumen.sort_values('establecimientos', ascending=False).head(20)
        
        # Formatear
        df_resumen.columns = ['Región', 'Comuna', 'N° Establecimientos', 'Matrícula Total']
        for col in ['N° Establecimientos', 'Matrícula Total']:
            df_resumen[col] = df_resumen[col].apply(lambda x: f"{int(x):,}")
    
    # Crear tabla HTML
    tabla = dbc.Table.from_dataframe(
        df_resumen,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        className="mb-0"
    )
    
    return tabla

def create_mapas_layout():
    """
    Crea el layout completo de la sección de mapas con subpestañas.
    """
    return dbc.Container([
        # Encabezado
        dbc.Row([
            dbc.Col([
                html.H2([
                    html.I(className="bi bi-geo-alt-fill me-3", style={"color": "var(--primary-color)"}),
                    "Visualización Geográfica"
                ], className="text-primary-custom mb-1"),
                html.P(
                    "Distribución territorial de matrícula y establecimientos EMTP",
                    className="text-gray-dark mb-4"
                )
            ])
        ]),
        
        # KPIs Generales
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3(id='mapa-num-territorios', className="text-primary-custom kpi-value mb-0"),
                        html.P(id='mapa-label-territorios', className="text-gray-dark kpi-label mb-0")
                    ])
                ], className="kpi-card text-center border-accent-custom")
            ], md=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("142,289", className="text-green kpi-value mb-0"),
                        html.P("Total Matrícula", className="text-gray-dark kpi-label mb-0")
                    ])
                ], className="kpi-card text-center border-accent-custom")
            ], md=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("1,234", className="text-orange kpi-value mb-0"),
                        html.P("Establecimientos", className="text-gray-dark kpi-label mb-0")
                    ])
                ], className="kpi-card text-center border-accent-custom")
            ], md=3, className="mb-3"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H3("94.2%", className="text-purple kpi-value mb-0"),
                        html.P("Cobertura", className="text-gray-dark kpi-label mb-0")
                    ])
                ], className="kpi-card text-center border-accent-custom")
            ], md=3, className="mb-3")
        ], className="mb-4"),
        
        # Control de Granularidad
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Label([
                                html.I(className="bi bi-zoom-in me-2"),
                                "Nivel de Granularidad"
                            ], className="fw-bold text-gray-dark mb-2"),
                            dcc.RadioItems(
                                id='mapa-granularidad',
                                options=[
                                    {'label': ' Regional (16 regiones)', 'value': 'regional'},
                                    {'label': ' Comunal (345 comunas)', 'value': 'comunal'}
                                ],
                                value='regional',
                                inline=True,
                                className="custom-radio-items"
                            )
                        ])
                    ])
                ], className="border-accent-custom shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        # Tabs para Matrícula y Establecimientos
        dbc.Tabs([
            # Tab 1: Matrícula
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        # Mapa de Matrícula
                        dbc.Card([
                            dbc.CardHeader([
                                html.I(className="bi bi-map me-2"),
                                "Distribución de Matrícula"
                            ], className="bg-light-custom border-0 fw-bold"),
                            dbc.CardBody([
                                dcc.Loading(
                                    id="loading-mapa-matricula",
                                    type="default",
                                    children=dcc.Graph(
                                        id='mapa-matricula',
                                        figure={},
                                        config={'displayModeBar': False}
                                    )
                                )
                            ], className="p-0")
                        ], className="border-accent-custom shadow-sm mb-4")
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        # Tabla resumen de Matrícula
                        dbc.Card([
                            dbc.CardHeader([
                                html.I(className="bi bi-table me-2"),
                                "Resumen por Territorio"
                            ], className="bg-light-custom border-0 fw-bold"),
                            dbc.CardBody([
                                html.Div(id='tabla-resumen-matricula', className="table-responsive")
                            ])
                        ], className="border-accent-custom shadow-sm")
                    ], width=12)
                ])
            ], label="Matrícula", tab_id="tab-matricula", 
               label_style={"color": "#5A6E79"}, 
               active_label_style={"color": "#34536A", "font-weight": "bold"}),
            
            # Tab 2: Establecimientos
            dbc.Tab([
                dbc.Row([
                    dbc.Col([
                        # Mapa de Establecimientos
                        dbc.Card([
                            dbc.CardHeader([
                                html.I(className="bi bi-building me-2"),
                                "Ubicación de Establecimientos"
                            ], className="bg-light-custom border-0 fw-bold"),
                            dbc.CardBody([
                                dcc.Loading(
                                    id="loading-mapa-establecimientos",
                                    type="default",
                                    children=dcc.Graph(
                                        id='mapa-establecimientos',
                                        figure={},
                                        config={'displayModeBar': False}
                                    )
                                )
                            ], className="p-0")
                        ], className="border-accent-custom shadow-sm mb-4")
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        # Tabla resumen de Establecimientos
                        dbc.Card([
                            dbc.CardHeader([
                                html.I(className="bi bi-table me-2"),
                                "Resumen por Territorio"
                            ], className="bg-light-custom border-0 fw-bold"),
                            dbc.CardBody([
                                html.Div(id='tabla-resumen-establecimientos', className="table-responsive")
                            ])
                        ], className="border-accent-custom shadow-sm")
                    ], width=12)
                ])
            ], label="Establecimientos", tab_id="tab-establecimientos",
               label_style={"color": "#5A6E79"}, 
               active_label_style={"color": "#34536A", "font-weight": "bold"})
        ], id="tabs-mapas", active_tab="tab-matricula", className="mb-3")
    ], fluid=True, className="p-4")

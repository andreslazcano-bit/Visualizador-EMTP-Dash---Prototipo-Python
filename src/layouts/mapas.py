"""
============================================================================
LAYOUT DE MAPA DE CHILE - MATRÍCULA Y ESTABLECIMIENTOS
============================================================================
Visualización geográfica de la distribución de matrícula y establecimientos EMTP
Usa choroplethmapbox con GeoJSON real de Chile
Soporta visualización a nivel regional y comunal
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import urllib.request
import geopandas as gpd
from pathlib import Path


def get_chile_geojson():
    """
    Obtiene el GeoJSON real de las regiones de Chile desde GitHub
    Fuente: https://github.com/fcortes/Chile-GeoJSON
    """
    try:
        # URL del GeoJSON de regiones de Chile
        # Probando diferentes archivos del repositorio
        urls = [
            "https://raw.githubusercontent.com/fcortes/Chile-GeoJSON/master/Regional.geojson",
            "https://raw.githubusercontent.com/fcortes/Chile-GeoJSON/master/regiones_edit.geojson"
        ]
        
        for url in urls:
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    geojson_data = json.loads(response.read().decode('utf-8'))
                    print(f"✓ GeoJSON cargado exitosamente desde: {url}")
                    return geojson_data
            except:
                continue
        
        print("⚠ No se pudo cargar GeoJSON desde ninguna fuente")
        return None
        
    except Exception as e:
        print(f"Error cargando GeoJSON: {e}")
        return None


def get_comunas_geojson():
    """
    Obtiene el GeoJSON de las comunas de Chile desde el shapefile local
    Fuente: Biblioteca del Congreso Nacional de Chile
    """
    try:
        # Ruta al shapefile de comunas
        base_dir = Path(__file__).parent.parent.parent
        shapefile_path = base_dir / "Comunas" / "comunas.shp"
        
        if not shapefile_path.exists():
            print(f"⚠ Shapefile no encontrado en: {shapefile_path}")
            return None
        
        # Leer shapefile con geopandas
        gdf = gpd.read_file(shapefile_path)
        
        # Filtrar "Zona sin demarcar" (codregion = 0)
        gdf = gdf[gdf['codregion'] != 0].copy()
        
        # Convertir a GeoJSON
        geojson_data = json.loads(gdf.to_json())
        
        print(f"✓ GeoJSON comunal cargado: {len(gdf)} comunas")
        return geojson_data
        
    except Exception as e:
        print(f"Error cargando GeoJSON comunal: {e}")
        return None


def create_chile_map():
    """
    Crea mapa coroplético de Chile con distribución de matrícula EMTP por región
    Usa colores degradados tipo Shiny para intensidad
    """
    # Cargar GeoJSON real de Chile
    geojson = get_chile_geojson()
    
    if geojson is None:
        # Si falla la carga, mostrar mensaje de error
        return go.Figure().add_annotation(
            text="Error cargando datos del mapa de Chile",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#B35A5A")
        )
    
    # Datos simulados de matrícula por región (16 regiones)
    # IMPORTANTE: El GeoJSON usa codregion como número, no string
    data = {
        'Region': [
            'Región de Arica y Parinacota', 'Región de Tarapacá', 'Región de Antofagasta', 
            'Región de Atacama', 'Región de Coquimbo', 'Región de Valparaíso', 
            'Región Metropolitana de Santiago', "Región del Libertador General Bernardo O'Higgins",
            'Región del Maule', 'Región de Ñuble', 'Región del Biobío', 'Región de La Araucanía',
            'Región de Los Ríos', 'Región de Los Lagos', 'Región Aysén del General Carlos Ibáñez del Campo', 
            'Región de Magallanes y de la Antártica Chilena'
        ],
        'codregion': [15, 1, 2, 3, 4, 5, 13, 6, 7, 16, 8, 9, 14, 10, 11, 12],  # Números, no strings
        'Matricula': [1850, 3200, 4100, 2800, 5600, 34500, 65300, 12400,
                      18900, 8200, 28700, 15600, 7300, 19800, 1450, 2100],
        'Establecimientos': [14, 28, 32, 22, 56, 248, 385, 94,
                             158, 72, 246, 132, 68, 187, 12, 18]
    }
    df = pd.DataFrame(data)
    df['Promedio'] = (df['Matricula'] / df['Establecimientos']).round(1)
    
    # Crear figura de choropleth
    # El GeoJSON usa properties.codregion (número)
    fig = px.choropleth_mapbox(
        df, 
        geojson=geojson,
        locations='codregion',  # Ahora usa números como el GeoJSON
        featureidkey="properties.codregion",  # El GeoJSON tiene este campo
        color='Matricula',
        color_continuous_scale=[
            [0.0, '#FFF8DC'],    # Beige claro (mínimo)
            [0.2, '#FFEAA7'],    # Amarillo suave
            [0.4, '#DFE6E9'],    # Gris azulado
            [0.6, '#74B9FF'],    # Azul medio
            [0.8, '#5A6E79'],    # Gris azul oscuro Shiny
            [1.0, '#1A2935']     # Azul muy oscuro (máximo)
        ],
        hover_name='Region',
        hover_data={
            'codregion': False,
            'Matricula': ':,',
            'Establecimientos': True,
            'Promedio': ':.1f'
        },
        labels={
            'Matricula': 'Matrícula Total',
            'Establecimientos': 'N° Establecimientos',
            'Promedio': 'Promedio por Establecimiento'
        },
        zoom=3.2,
        center={"lat": -35, "lon": -71},
        mapbox_style='open-street-map',
        opacity=0.7
    )
    
    fig.update_layout(
        title={
            'text': 'Distribución de Matrícula EMTP por Región',
            'font': {'size': 18, 'color': '#34536A', 'family': 'Segoe UI, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        height=700,
        paper_bgcolor='white',
        coloraxis_colorbar=dict(
            title="Matrícula",
            thickness=20,
            len=0.7,
            tickformat=','
        )
    )
    
    return fig


def create_establecimientos_map():
    """
    Crea un mapa choropleth de establecimientos por región
    con regiones coloreadas según la intensidad (más oscuro = más establecimientos)
    """
    # Cargar GeoJSON real de Chile
    geojson = get_chile_geojson()
    
    if geojson is None:
        # Si falla la carga, mostrar mensaje de error
        return go.Figure().add_annotation(
            text="Error cargando datos del mapa de Chile",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#B35A5A")
        )
    
    regiones_data = {
        'codregion': [15, 1, 2, 3, 4, 5, 13, 6, 7, 16, 8, 9, 14, 10, 11, 12],  # Números
        'Región': [
            'Región de Arica y Parinacota', 'Región de Tarapacá', 'Región de Antofagasta', 
            'Región de Atacama', 'Región de Coquimbo', 'Región de Valparaíso', 
            'Región Metropolitana de Santiago', "Región del Libertador General Bernardo O'Higgins",
            'Región del Maule', 'Región de Ñuble', 'Región del Biobío', 'Región de La Araucanía',
            'Región de Los Ríos', 'Región de Los Lagos', 'Región Aysén del General Carlos Ibáñez del Campo', 
            'Región de Magallanes y de la Antártica Chilena'
        ],
        'Establecimientos': [
            18, 32, 58, 28,
            84, 156, 385, 124,
            142, 62, 198, 128,
            52, 112, 14, 19
        ],
        'Matrícula': [
            2450, 4380, 8920, 3150,
            12840, 28450, 65300, 18950,
            22350, 8940, 31200, 19850,
            7450, 18200, 1850, 2520
        ]
    }
    
    df = pd.DataFrame(regiones_data)
    df['Promedio'] = (df['Matrícula'] / df['Establecimientos']).round(0)
    
    # Crear mapa choropleth con Mapbox
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson,
        locations='codregion',  # Ahora usa números
        featureidkey="properties.codregion",  # El GeoJSON tiene este campo
        color='Establecimientos',
        color_continuous_scale=[
            [0.0, '#F5E6FF'],    # Púrpura muy claro (mínimo)
            [0.2, '#E6CCFF'],    # Púrpura claro
            [0.4, '#D4A5E8'],    # Púrpura medio
            [0.6, '#B35A5A'],    # Rojo rosado
            [0.8, '#8B3A3A'],    # Rojo oscuro
            [1.0, '#34536A']     # Azul oscuro (máximo)
        ],
        hover_name='Región',
        hover_data={
            'codregion': False,
            'Establecimientos': ':,.0f',
            'Matrícula': ':,.0f',
            'Promedio': ':,.0f'
        },
        labels={
            'Establecimientos': 'N° Establecimientos',
            'Matrícula': 'Matrícula EMTP',
            'Promedio': 'Promedio por EE'
        },
        mapbox_style='open-street-map',
        zoom=3.2,
        center=dict(lat=-35, lon=-71),
        opacity=0.7
    )
    
    fig.update_layout(
        title=dict(
            text='<b>Distribución de Establecimientos EMTP por Región</b>',
            font=dict(size=20, color='#2C3E50', family='Arial'),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        height=700,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor='white',
        plot_bgcolor='white',
        coloraxis_colorbar=dict(
            title="<b>N° de<br>Establecimientos</b>",
            thickness=20,
            len=0.7,
            x=1.02,
            tickformat=',',
            tickfont=dict(size=11)
        )
    )
    
    return fig


def create_chile_comunas_map():
    """
    Crea mapa coroplético de Chile con distribución de matrícula EMTP por comuna
    Usa datos del shapefile oficial de la Biblioteca del Congreso Nacional
    """
    # Cargar GeoJSON de comunas
    geojson = get_comunas_geojson()
    
    if geojson is None:
        return go.Figure().add_annotation(
            text="Error cargando datos comunales",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#B35A5A")
        )
    
    # Cargar datos comunales desde CSV
    try:
        base_dir = Path(__file__).parent.parent.parent
        data_path = base_dir / "data" / "processed" / "matricula_comunal_simulada.csv"
        
        if not data_path.exists():
            return go.Figure().add_annotation(
                text="Datos comunales no disponibles",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#B35A5A")
            )
        
        # Leer y agregar datos por comuna (suma de todos los años y especialidades)
        df_full = pd.read_csv(data_path)
        df = df_full.groupby(['cod_comuna', 'comuna', 'region']).agg({
            'matricula_total': 'sum'
        }).reset_index()
        df.columns = ['cod_comuna', 'Comuna', 'Region', 'Matricula']
        
        # Crear figura de choropleth
        fig = px.choropleth_mapbox(
            df, 
            geojson=geojson,
            locations='cod_comuna',
            featureidkey="properties.cod_comuna",
            color='Matricula',
            color_continuous_scale=[
                [0.0, '#FFF8DC'],    # Beige claro (mínimo)
                [0.2, '#FFEAA7'],    # Amarillo suave
                [0.4, '#DFE6E9'],    # Gris azulado
                [0.6, '#74B9FF'],    # Azul medio
                [0.8, '#5A6E79'],    # Gris azul oscuro Shiny
                [1.0, '#1A2935']     # Azul muy oscuro (máximo)
            ],
            hover_name='Comuna',
            hover_data={
                'cod_comuna': False,
                'Region': True,
                'Matricula': ':,',
            },
            labels={
                'Matricula': 'Matrícula Total',
                'Region': 'Región'
            },
            zoom=3.2,
            center={"lat": -35, "lon": -71},
            mapbox_style='open-street-map',
            opacity=0.7
        )
        
        fig.update_layout(
            title={
                'text': 'Distribución de Matrícula EMTP por Comuna',
                'font': {'size': 18, 'color': '#34536A', 'family': 'Segoe UI, sans-serif'},
                'x': 0.5,
                'xanchor': 'center'
            },
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            height=700,
            paper_bgcolor='white',
            coloraxis_colorbar=dict(
                title="Matrícula",
                thickness=20,
                len=0.7,
                tickformat=','
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creando mapa comunal: {e}")
        return go.Figure().add_annotation(
            text=f"Error: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#B35A5A")
        )


def create_establecimientos_comunas_map():
    """
    Crea mapa coroplético de establecimientos por comuna
    """
    # Cargar GeoJSON de comunas
    geojson = get_comunas_geojson()
    
    if geojson is None:
        return go.Figure().add_annotation(
            text="Error cargando datos comunales",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#B35A5A")
        )
    
    # Para este mapa, vamos a contar el número de establecimientos únicos por comuna
    # basado en los datos comunales (aproximación)
    try:
        base_dir = Path(__file__).parent.parent.parent
        data_path = base_dir / "data" / "processed" / "matricula_comunal_simulada.csv"
        
        if not data_path.exists():
            return go.Figure().add_annotation(
                text="Datos comunales no disponibles",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="#B35A5A")
            )
        
        # Leer datos comunales
        df_full = pd.read_csv(data_path)
        
        # Estimar número de establecimientos por comuna
        # (contando combinaciones únicas de especialidad y dependencia)
        df = df_full.groupby(['cod_comuna', 'comuna', 'region']).agg({
            'matricula_total': 'sum',
            'especialidad': 'nunique',  # Aproximación: distintas especialidades
            'dependencia': 'nunique'
        }).reset_index()
        
        # Estimación simple: cada combinación especialidad-dependencia podría ser un EE
        df['Establecimientos'] = (df['especialidad'] * df['dependencia'] / 3).round(0).astype(int)
        df['Establecimientos'] = df['Establecimientos'].clip(lower=1)  # Mínimo 1
        
        df_plot = df[['cod_comuna', 'comuna', 'region', 'Establecimientos', 'matricula_total']].copy()
        df_plot.columns = ['cod_comuna', 'Comuna', 'Region', 'Establecimientos', 'Matricula']
        df_plot['Promedio'] = (df_plot['Matricula'] / df_plot['Establecimientos']).round(0)
        
        # Crear mapa choropleth
        fig = px.choropleth_mapbox(
            df_plot,
            geojson=geojson,
            locations='cod_comuna',
            featureidkey="properties.cod_comuna",
            color='Establecimientos',
            color_continuous_scale=[
                [0.0, '#F5E6FF'],    # Púrpura muy claro
                [0.2, '#E6CCFF'],    # Púrpura claro
                [0.4, '#D4A5E8'],    # Púrpura medio
                [0.6, '#B35A5A'],    # Rojo rosado
                [0.8, '#8B3A3A'],    # Rojo oscuro
                [1.0, '#34536A']     # Azul oscuro
            ],
            hover_name='Comuna',
            hover_data={
                'cod_comuna': False,
                'Region': True,
                'Establecimientos': ':,.0f',
                'Matricula': ':,.0f',
                'Promedio': ':,.0f'
            },
            labels={
                'Establecimientos': 'N° Establecimientos (est.)',
                'Matricula': 'Matrícula EMTP',
                'Promedio': 'Promedio por EE',
                'Region': 'Región'
            },
            mapbox_style='open-street-map',
            zoom=3.2,
            center=dict(lat=-35, lon=-71),
            opacity=0.7
        )
        
        fig.update_layout(
            title=dict(
                text='<b>Distribución de Establecimientos EMTP por Comuna (estimado)</b>',
                font=dict(size=18, color='#2C3E50', family='Arial'),
                x=0.5,
                xanchor='center',
                y=0.98,
                yanchor='top'
            ),
            height=700,
            margin=dict(l=0, r=0, t=50, b=0),
            paper_bgcolor='white',
            plot_bgcolor='white',
            coloraxis_colorbar=dict(
                title="<b>N° Est.</b>",
                thickness=20,
                len=0.7,
                x=1.02,
                tickformat=',',
                tickfont=dict(size=11)
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creando mapa comunal de establecimientos: {e}")
        return go.Figure().add_annotation(
            text=f"Error: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#B35A5A")
        )


def create_mapas_layout():
    """Crea el layout completo de la pestaña de Mapas"""
    
    return html.Div([
        dbc.Container([
            # Header
            dbc.Row([
                dbc.Col([
                    html.H2([
                        html.I(className="fas fa-map-marked-alt me-3", style={"color": "#34536A"}),
                        "Visualización Geográfica EMTP"
                    ], className="mb-3", style={"color": "#2C3E50"}),
                    html.P(
                        "Distribución territorial de la matrícula y establecimientos de Educación Media Técnico-Profesional en Chile",
                        className="text-muted mb-2"
                    )
                ], width=8),
                dbc.Col([
                    # Selector de granularidad
                    html.Div([
                        html.Label("Nivel de detalle:", className="text-muted small mb-1"),
                        dcc.RadioItems(
                            id='mapa-granularidad',
                            options=[
                                {'label': ' Regional (16 regiones)', 'value': 'regional'},
                                {'label': ' Comunal (345 comunas)', 'value': 'comunal'}
                            ],
                            value='regional',
                            inline=False,
                            className="",
                            labelStyle={'display': 'block', 'marginBottom': '5px'},
                            inputStyle={"marginRight": "8px"}
                        )
                    ], style={
                        'backgroundColor': '#F8F9FA',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'border': '1px solid #DEE2E6'
                    })
                ], width=4)
            ]),
            
            # KPIs Resumen
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="fas fa-users fa-2x mb-2", style={"color": "#34536A"}),
                                html.H3("287.450", className="mb-0", style={"color": "#2C3E50"}),
                                html.P("Matrícula Nacional", className="text-muted small mb-0")
                            ], className="text-center")
                        ])
                    ], className="shadow-sm border-0 h-100")
                ], md=3, className="mb-3"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="fas fa-school fa-2x mb-2", style={"color": "#B35A5A"}),
                                html.H3("1.842", className="mb-0", style={"color": "#2C3E50"}),
                                html.P("Establecimientos", className="text-muted small mb-0")
                            ], className="text-center")
                        ])
                    ], className="shadow-sm border-0 h-100")
                ], md=3, className="mb-3"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="fas fa-map fa-2x mb-2", style={"color": "#5A6E79"}),
                                html.H3(id='kpi-territorios', children="16", className="mb-0", style={"color": "#2C3E50"}),
                                html.P(id='kpi-territorios-label', children="Regiones", className="text-muted small mb-0")
                            ], className="text-center")
                        ])
                    ], className="shadow-sm border-0 h-100")
                ], md=3, className="mb-3"),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="fas fa-chart-line fa-2x mb-2", style={"color": "#C2A869"}),
                                html.H3("156", className="mb-0", style={"color": "#2C3E50"}),
                                html.P("Est. promedio/región", className="text-muted small mb-0")
                            ], className="text-center")
                        ])
                    ], className="shadow-sm border-0 h-100")
                ], md=3, className="mb-3")
            ]),
            
            # Tabs con Mapas
            dbc.Row([
                dbc.Col([
                    dbc.Tabs([
                        dbc.Tab(
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Loading(
                                        id="loading-mapa-matricula",
                                        type="circle",
                                        children=dcc.Graph(
                                            id='mapa-matricula',
                                            figure=create_chile_map(),
                                            config={'displayModeBar': True, 'displaylogo': False}
                                        )
                                    )
                                ])
                            ], className="border-0 shadow-sm mt-3"),
                            label="Matrícula por Territorio",
                            tab_id="tab-mapa-matricula",
                            label_style={"color": "#34536A"},
                            active_label_style={"color": "#34536A", "fontWeight": "bold"}
                        ),
                        dbc.Tab(
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Loading(
                                        id="loading-mapa-establecimientos",
                                        type="circle",
                                        children=dcc.Graph(
                                            id='mapa-establecimientos',
                                            figure=create_establecimientos_map(),
                                            config={'displayModeBar': True, 'displaylogo': False}
                                        )
                                    )
                                ])
                            ], className="border-0 shadow-sm mt-3"),
                            label="Establecimientos por Territorio",
                            tab_id="tab-mapa-establecimientos",
                            label_style={"color": "#B35A5A"},
                            active_label_style={"color": "#B35A5A", "fontWeight": "bold"}
                        ),
                    ], id="mapas-tabs", active_tab="tab-mapa-matricula")
                ], width=12)
            ], className="mb-4"),
            
            # Tabla de datos por región
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H5([
                                html.I(className="fas fa-table me-2"),
                                "Datos por Territorio"
                            ], className="mb-0")
                        ]),
                        dbc.CardBody([
                            html.Div(id='tabla-regiones', children=[
                                create_regiones_table()
                            ])
                        ])
                    ], className="shadow-sm border-0")
                ], width=12)
            ])
            
        ], fluid=True, className="py-4")
    ], style={"background": "#F4F6F7", "minHeight": "100vh"})


def create_regiones_table():
    """Crea tabla resumen de datos por región"""
    
    regiones_data = {
        'Región': [
            'Arica y Parinacota', 'Tarapacá', 'Antofagasta', 'Atacama',
            'Coquimbo', 'Valparaíso', 'Metropolitana', "O'Higgins",
            'Maule', 'Ñuble', 'Biobío', 'La Araucanía',
            'Los Ríos', 'Los Lagos', 'Aysén', 'Magallanes'
        ],
        'Matrícula': [
            2450, 4380, 8920, 3150,
            12840, 28450, 65300, 18950,
            22350, 8940, 31200, 19850,
            7450, 18200, 1850, 2520
        ],
        'Establecimientos': [
            18, 32, 58, 28,
            84, 156, 385, 124,
            142, 62, 198, 128,
            52, 112, 14, 19
        ]
    }
    
    df = pd.DataFrame(regiones_data)
    df['Promedio Mat./Est.'] = (df['Matrícula'] / df['Establecimientos']).round(0).astype(int)
    
    # Crear tabla HTML
    table_header = [
        html.Thead(html.Tr([
            html.Th("Región", style={"backgroundColor": "#34536A", "color": "white"}),
            html.Th("Matrícula", style={"backgroundColor": "#34536A", "color": "white"}),
            html.Th("Establecimientos", style={"backgroundColor": "#34536A", "color": "white"}),
            html.Th("Promedio Mat./Est.", style={"backgroundColor": "#34536A", "color": "white"})
        ]))
    ]
    
    table_body = [html.Tbody([
        html.Tr([
            html.Td(row['Región']),
            html.Td(f"{row['Matrícula']:,}".replace(",", "."), style={"textAlign": "right"}),
            html.Td(f"{row['Establecimientos']:,}".replace(",", "."), style={"textAlign": "right"}),
            html.Td(f"{row['Promedio Mat./Est.']:,}".replace(",", "."), style={"textAlign": "right"})
        ], style={"borderBottom": "1px solid #ECF0F1"})
        for idx, row in df.iterrows()
    ])]
    
    return dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        className="mb-0"
    )

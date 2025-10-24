"""
============================================================================
LAYOUTS PARA CONTENIDO DE DEMOSTRACIÓN
============================================================================
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def create_demo_kpi_cards(title, metrics):
    """Crea tarjetas KPI de demostración con paleta oficial"""
    cards = []
    colors = ['primary-custom', 'green', 'orange', 'purple']  # Usando colores de la paleta
    
    for i, (label, value) in enumerate(metrics.items()):
        color_class = colors[i % len(colors)]
        card = dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(str(value), className=f"text-{color_class} kpi-value"),
                    html.P(label, className="text-gray-dark kpi-label")
                ])
            ], className="kpi-card text-center border-accent-custom")
        ], md=3, className="mb-3")
        cards.append(card)
    
    return dbc.Row(cards)


def create_demo_chart(chart_type="line", title="Gráfico de Demostración"):
    """Crea un gráfico de demostración con paleta oficial"""
    # Datos simulados
    years = list(range(2019, 2025))
    values = np.random.randint(50, 200, len(years))
    
    # Colores de la paleta oficial
    color_palette = ['#006FB3', '#FE6565', '#2D717C', '#E0701E', '#6633CC', '#FFA11B']
    
    if chart_type == "line":
        fig = px.line(
            x=years, 
            y=values,
            title=title,
            labels={'x': 'Año', 'y': 'Cantidad'},
            color_discrete_sequence=[color_palette[0]]
        )
        fig.update_traces(line=dict(width=3))
    elif chart_type == "bar":
        fig = px.bar(
            x=years, 
            y=values,
            title=title,
            labels={'x': 'Año', 'y': 'Cantidad'},
            color_discrete_sequence=[color_palette[1]]
        )
    else:
        fig = px.pie(
            values=values[:4], 
            names=['Región A', 'Región B', 'Región C', 'Región D'],
            title=title,
            color_discrete_sequence=color_palette[:4]
        )
    
    fig.update_layout(
        template="plotly_white",
        font=dict(size=12, color='#111111'),  # Negro para títulos
        title_font=dict(size=16, color='#111111'),
        height=400,
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF'
    )
    
    return dcc.Graph(figure=fig, className="mb-4")


def create_demo_filters():
    """Crea filtros de demostración con paleta oficial"""
    return dbc.Card([
        dbc.CardHeader(html.H5(html.Span([html.I(className="fas fa-filter me-2"), "Filtros"]), className="mb-0 text-primary-custom")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Región:", className="text-gray-dark"),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Todas las regiones', 'value': 'all'},
                            {'label': 'Metropolitana', 'value': 'rm'},
                            {'label': 'Valparaíso', 'value': 'v'},
                            {'label': 'Biobío', 'value': 'viii'},
                        ],
                        value='all',
                        id='filter-region',
                        style={'borderColor': '#A8B7C7'}
                    )
                ], md=6),
                dbc.Col([
                    html.Label("Año:", className="text-gray-dark"),
                    dcc.Dropdown(
                        options=[
                            {'label': '2024', 'value': 2024},
                            {'label': '2023', 'value': 2023},
                            {'label': '2022', 'value': 2022},
                        ],
                        value=2024,
                        id='filter-year',
                        style={'borderColor': '#A8B7C7'}
                    )
                ], md=6),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    html.Label("Especialidad:", className="text-gray-dark"),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Todas', 'value': 'all'},
                            {'label': 'Administración', 'value': 'admin'},
                            {'label': 'Electricidad', 'value': 'elec'},
                            {'label': 'Mecánica', 'value': 'mec'},
                        ],
                        value='all',
                        id='filter-especialidad',
                        style={'borderColor': '#A8B7C7'}
                    )
                ], md=6),
                dbc.Col([
                    dbc.Button(
                        "Aplicar Filtros", 
                        className="btn-primary-custom mt-4 w-100",
                        id="apply-filters"
                    )
                ], md=6),
            ])
        ])
    ], className="mb-4 filters-sidebar border-accent-custom")


def create_demo_table():
    """Crea una tabla de demostración"""
    # Datos simulados
    data = {
        'Especialidad': ['Administración', 'Electricidad', 'Mecánica', 'Construcción', 'Gastronomía'],
        'Matrícula 2024': [1250, 980, 750, 620, 580],
        'Matrícula 2023': [1180, 950, 720, 600, 550],
        'Variación %': [5.9, 3.2, 4.2, 3.3, 5.5],
        'Tasa Retención %': [92.5, 89.3, 87.8, 85.2, 91.1]
    }
    
    df = pd.DataFrame(data)
    
    return dbc.Table.from_dataframe(
        df, 
        striped=True, 
        bordered=True, 
        hover=True,
        responsive=True,
        className="mb-4"
    )


def create_section_layout(title, kpi_metrics, chart_configs, include_table=True, custom_table_data=None):
    """Crea un layout de sección estándar con paleta oficial"""
    
    # El título ahora puede ser un string o un elemento HTML (Span con ícono)
    layout = [
        html.H2(title, className="mb-4 text-primary-custom", style={'fontWeight': 'bold'}),
        
        # KPIs
        create_demo_kpi_cards(title, kpi_metrics),
        
        html.Hr(style={'borderColor': '#A8B7C7'}),
        
        # Filtros y contenido
        dbc.Row([
            # Sidebar con filtros
            dbc.Col([
                create_demo_filters()
            ], md=3),
            
            # Contenido principal
            dbc.Col([
                # Gráficos
                *[create_demo_chart(**config) for config in chart_configs],
                
                # Tabla si se requiere
                html.H4(html.Span([html.I(className="fas fa-table me-2"), "Datos Detallados"]), className="mt-4 mb-3 text-tertiary-custom") if include_table else "",
                create_demo_table(custom_table_data) if include_table else "",
                
            ], md=9)
        ])
    ]
    
    return html.Div(layout)


def create_matricula_subtab_content(subtab):
    """Crea contenido específico para sub-pestañas de matrícula"""
    contents = {
        "evolucion": {
            "title": html.Span([html.I(className="fas fa-chart-area me-2"), "Evolución Anual de la Matrícula EMTP"]),
            "metrics": {
                "Matrícula 2024": "85,420",
                "Crecimiento 5 años": "+12.8%", 
                "Promedio Anual": "82,150",
                "Proyección 2025": "88,200"
            },
            "charts": [
                {"chart_type": "line", "title": "Evolución Histórica de Matrícula (2015-2024)"},
                {"chart_type": "bar", "title": "Crecimiento Anual por Región"},
            ],
            "table_data": {
                'Año': [2020, 2021, 2022, 2023, 2024],
                'Matrícula Total': [78450, 79820, 81200, 83150, 85420],
                'Hombres': [45230, 46180, 47020, 48100, 49350],
                'Mujeres': [33220, 33640, 34180, 35050, 36070],
                'Variación %': ['-', '+1.7%', '+1.7%', '+2.4%', '+2.7%']
            }
        },
        "demografia": {
            "title": html.Span([html.I(className="fas fa-user-friends me-2"), "Distribución Demográfica de Estudiantes"]),
            "metrics": {
                "% Mujeres": "42.8%",
                "% Hombres": "57.2%", 
                "Edad Promedio": "16.8 años",
                "% Vulnerabilidad": "68.2%"
            },
            "charts": [
                {"chart_type": "pie", "title": "Distribución por Género"},
                {"chart_type": "bar", "title": "Matrícula por Quintil Socioeconómico"},
            ],
            "table_data": {
                'Género': ['Masculino', 'Femenino'],
                'Cantidad': [48830, 36590],
                'Porcentaje': ['57.2%', '42.8%'],
                'Crecimiento 2023': ['+2.1%', '+3.8%'],
                'Especialidades Top': ['Electricidad', 'Administración']
            }
        },
        "retencion": {
            "title": html.Span([html.I(className="fas fa-user-check me-2"), "Análisis de Retención Estudiantil"]),
            "metrics": {
                "Tasa Retención": "89.5%",
                "Deserción Anual": "10.5%", 
                "Retención 3° Medio": "92.1%",
                "Retención 4° Medio": "87.3%"
            },
            "charts": [
                {"chart_type": "line", "title": "Evolución de Tasa de Retención por Nivel"},
                {"chart_type": "bar", "title": "Retención por Especialidad"},
            ],
            "table_data": {
                'Especialidad': ['Administración', 'Electricidad', 'Mecánica', 'Construcción', 'Gastronomía'],
                'Tasa Retención %': [92.5, 89.3, 87.8, 85.2, 91.1],
                'Deserción %': [7.5, 10.7, 12.2, 14.8, 8.9],
                'Principales Causas': ['Económicas', 'Académicas', 'Laborales', 'Familiares', 'Vocacionales']
            }
        },
        "comparacion": {
            "title": html.Span([html.I(className="fas fa-chart-bar me-2"), "Comparación con Sistema Educativo"]),
            "metrics": {
                "% Total Sistema": "38.4%",
                "vs HC Científico": "61.6%", 
                "Preferencia Técnica": "+5.2%",
                "Brecha de Género": "14.4pp"
            },
            "charts": [
                {"chart_type": "pie", "title": "Distribución: EMTP vs Humanista-Científico"},
                {"chart_type": "bar", "title": "Comparación Regional: Preferencia EMTP"},
            ],
            "table_data": {
                'Región': ['Metropolitana', 'Valparaíso', 'Biobío', 'Araucanía', 'Antofagasta'],
                '% EMTP': [35.2, 42.8, 45.1, 48.3, 44.7],
                '% HC': [64.8, 57.2, 54.9, 51.7, 55.3],
                'Tendencia': ['Estable', 'Creciente', 'Creciente', 'Estable', 'Decreciente']
            }
        }
    }
    
    if subtab not in contents:
        subtab = "evolucion"
    
    content = contents[subtab]
    return create_section_layout(
        content["title"],
        content["metrics"], 
        content["charts"],
        include_table=True,
        custom_table_data=content.get("table_data")
    )


def create_demo_table(custom_data=None):
    """Crea una tabla de demostración con datos personalizables"""
    if custom_data:
        df = pd.DataFrame(custom_data)
    else:
        # Datos por defecto
        data = {
            'Especialidad': ['Administración', 'Electricidad', 'Mecánica', 'Construcción', 'Gastronomía'],
            'Matrícula 2024': [1250, 980, 750, 620, 580],
            'Matrícula 2023': [1180, 950, 720, 600, 550],
            'Variación %': [5.9, 3.2, 4.2, 3.3, 5.5],
            'Tasa Retención %': [92.5, 89.3, 87.8, 85.2, 91.1]
        }
        df = pd.DataFrame(data)
    
    return dbc.Table.from_dataframe(
        df, 
        striped=True, 
        bordered=True, 
        hover=True,
        responsive=True,
        className="mb-4"
    )


def create_egresados_subtab_content(subtab):
    """Crea contenido específico para sub-pestañas de egresados"""
    contents = {
        "transicion": {
            "title": html.Span([html.I(className="fas fa-arrow-right me-2"), "Tasa de Transición a Educación Superior"]),
            "metrics": {
                "Tasa Transición": "67.3%",
                "A Universidades": "30.4%", 
                "A Institutos": "36.9%",
                "Inmediata": "45.2%"
            },
            "charts": [
                {"chart_type": "line", "title": "Evolución Tasa de Transición 2015-2024"},
                {"chart_type": "bar", "title": "Transición por Tipo de Institución"},
            ],
            "table_data": {
                'Especialidad': ['Administración', 'Electricidad', 'Mecánica', 'Enfermería', 'Programación'],
                'Tasa Transición %': [72.3, 65.8, 61.2, 78.5, 74.1],
                'Universidades %': [35.2, 28.4, 25.1, 42.3, 38.7],
                'Institutos %': [37.1, 37.4, 36.1, 36.2, 35.4],
                'Área Preferida': ['Negocios', 'Ingeniería', 'Técnica', 'Salud', 'TI']
            }
        },
        "areas": {
            "title": html.Span([html.I(className="fas fa-th me-2"), "Áreas y Carreras de Continuidad"]),
            "metrics": {
                "Áreas Populares": "8",
                "Continuidad Directa": "78.5%", 
                "Cambio de Área": "21.5%",
                "Éxito Académico": "85.2%"
            },
            "charts": [
                {"chart_type": "pie", "title": "Distribución por Área de Estudio"},
                {"chart_type": "bar", "title": "Top 10 Carreras Elegidas"},
            ]
        },
        "geografia": {
            "title": html.Span([html.I(className="fas fa-map-marker-alt me-2"), "Distribución Geográfica de Egresados"]),
            "metrics": {
                "Regiones Activas": "15",
                "Concentración RM": "41.2%", 
                "Movilidad Inter-regional": "23.8%",
                "Estudio en Región": "76.2%"
            },
            "charts": [
                {"chart_type": "bar", "title": "Egresados por Región de Origen vs Estudio"},
                {"chart_type": "line", "title": "Flujo de Movilidad Regional"},
            ]
        },
        "genero": {
            "title": html.Span([html.I(className="fas fa-users me-2"), "Análisis por Género en Transición"]),
            "metrics": {
                "Transición Mujeres": "71.8%",
                "Transición Hombres": "64.1%", 
                "Brecha de Género": "7.7pp",
                "Áreas Predominantes": "4"
            },
            "charts": [
                {"chart_type": "bar", "title": "Tasa de Transición por Género y Especialidad"},
                {"chart_type": "pie", "title": "Distribución por Género en ESUP"},
            ]
        }
    }
    
    if subtab not in contents:
        subtab = "transicion"
    
    content = contents[subtab]
    return create_section_layout(
        content["title"],
        content["metrics"], 
        content["charts"],
        include_table=True,
        custom_table_data=content.get("table_data")
    )


def create_docentes_subtab_content(subtab):
    """Crea contenido específico para sub-pestañas de docentes"""
    contents = {
        "distribucion": {
            "title": html.Span([html.I(className="fas fa-users me-2"), "Distribución Total de Docentes EMTP"]),
            "metrics": {
                "Total Docentes": "12,450",
                "Por Especialidad": "8,920", 
                "Formación General": "3,530",
                "Ratio Est/Doc": "6.9"
            },
            "charts": [
                {"chart_type": "bar", "title": "Docentes por Especialidad"},
                {"chart_type": "pie", "title": "Distribución por Tipo de Formación"},
            ],
            "table_data": {
                'Especialidad': ['Administración', 'Electricidad', 'Mecánica', 'Construcción', 'Gastronomía'],
                'N° Docentes': [1850, 1420, 1230, 980, 780],
                'Ratio Est/Doc': [6.8, 6.9, 6.1, 6.3, 7.4],
                'Experiencia Prom.': [8.5, 9.2, 10.1, 11.3, 7.8],
                '% Con Título Ped.': [78.3, 82.1, 75.4, 71.2, 80.9]
            }
        },
        "demografia": {
            "title": html.Span([html.I(className="fas fa-id-card me-2"), "Perfil Demográfico Docente"]),
            "metrics": {
                "Edad Promedio": "42.3 años",
                "% Mujeres": "35.2%", 
                "% Hombres": "64.8%",
                "% Mayores 50": "28.7%"
            },
            "charts": [
                {"chart_type": "bar", "title": "Distribución Etaria por Rango"},
                {"chart_type": "pie", "title": "Distribución por Género"},
            ]
        },
        "titulacion": {
            "title": html.Span([html.I(className="fas fa-graduation-cap me-2"), "Formación y Titulación Docente"]),
            "metrics": {
                "Título Pedagógico": "78.3%",
                "Título Técnico": "21.7%", 
                "Postgrado": "34.8%",
                "Cert. Especialidad": "89.2%"
            },
            "charts": [
                {"chart_type": "bar", "title": "Nivel de Formación por Especialidad"},
                {"chart_type": "line", "title": "Evolución de Titulación Pedagógica"},
            ]
        },
        "estabilidad": {
            "title": html.Span([html.I(className="fas fa-briefcase me-2"), "Estabilidad Laboral Docente"]),
            "metrics": {
                "Años Promedio": "8.5 años",
                "Rotación Anual": "12.8%", 
                "Contrato Indefinido": "67.4%",
                "Jornada Completa": "42.1%"
            },
            "charts": [
                {"chart_type": "line", "title": "Evolución de la Rotación Docente"},
                {"chart_type": "bar", "title": "Estabilidad por Tipo de Establecimiento"},
            ]
        }
    }
    
    if subtab not in contents:
        subtab = "distribucion"
    
    content = contents[subtab]
    return create_section_layout(
        content["title"],
        content["metrics"], 
        content["charts"],
        include_table=True,
        custom_table_data=content.get("table_data")
    )


def create_titulacion_subtab_content(subtab):
    """Crea contenido específico para sub-pestañas de titulación"""
    contents = {
        "evolucion": {
            "title": html.Span([html.I(className="fas fa-chart-area me-2"), "Evolución de Titulados EMTP"]),
            "metrics": {
                "Titulados 2024": "16,890",
                "Crecimiento Anual": "+4.2%", 
                "Tasa Histórica": "91.2%",
                "Meta Nacional": "95.0%"
            },
            "charts": [
                {"chart_type": "line", "title": "Evolución Histórica de Titulados (2015-2024)"},
                {"chart_type": "bar", "title": "Titulados por Cohorte de Ingreso"},
            ]
        },
        "tasa": {
            "title": html.Span([html.I(className="fas fa-percentage me-2"), "Tasa de Titulación por Especialidad"]),
            "metrics": {
                "Tasa Nacional": "91.2%",
                "Mejor Especialidad": "95.8%", 
                "Brecha Max-Min": "12.3pp",
                "Tendencia": "Creciente"
            },
            "charts": [
                {"chart_type": "bar", "title": "Tasa de Titulación por Especialidad"},
                {"chart_type": "line", "title": "Evolución por Especialidad"},
            ]
        },
        "tiempo": {
            "title": html.Span([html.I(className="fas fa-clock me-2"), "Tiempo de Titulación"]),
            "metrics": {
                "Tiempo Promedio": "18 meses",
                "Titulación Oportuna": "67.8%", 
                "Máximo Observado": "36 meses",
                "Eficiencia": "85.6%"
            },
            "charts": [
                {"chart_type": "bar", "title": "Tiempo de Titulación por Especialidad"},
                {"chart_type": "pie", "title": "Distribución de Tiempos"},
            ]
        },
        "comparativo": {
            "title": html.Span([html.I(className="fas fa-chart-bar me-2"), "Análisis Comparativo Regional"]),
            "metrics": {
                "Regiones Evaluadas": "15",
                "Mejor Región": "96.4%", 
                "Brecha Regional": "8.7pp",
                "Convergencia": "Positiva"
            },
            "charts": [
                {"chart_type": "bar", "title": "Tasa de Titulación por Región"},
                {"chart_type": "line", "title": "Evolución Regional Comparada"},
            ]
        }
    }
    
    if subtab not in contents:
        subtab = "evolucion"
    
    content = contents[subtab]
    return create_section_layout(
        content["title"],
        content["metrics"], 
        content["charts"],
        include_table=True,
        custom_table_data=content.get("table_data")
    )


def create_establecimientos_subtab_content(subtab):
    """Crea contenido específico para sub-pestañas de establecimientos"""
    contents = {
        "geografia": {
            "title": html.Span([html.I(className="fas fa-map-marker-alt me-2"), "Distribución Geográfica de Establecimientos"]),
            "metrics": {
                "Total Establecimientos": "968",
                "Regiones Cubiertas": "15", 
                "Concentración RM": "28.4%",
                "Ruralidad": "15.3%"
            },
            "charts": [
                {"chart_type": "bar", "title": "Establecimientos por Región"},
                {"chart_type": "pie", "title": "Distribución Urbano/Rural"},
            ]
        },
        "especialidades": {
            "title": html.Span([html.I(className="fas fa-th-large me-2"), "Especialidades y Programas"]),
            "metrics": {
                "Especialidades Activas": "47",
                "Programas Totales": "2,840", 
                "Más Popular": "Administración",
                "Cobertura Nacional": "100%"
            },
            "charts": [
                {"chart_type": "bar", "title": "Top 15 Especialidades por Matrícula"},
                {"chart_type": "pie", "title": "Distribución por Sector Productivo"},
            ]
        },
        "dependencia": {
            "title": html.Span([html.I(className="fas fa-building me-2"), "Análisis por Dependencia"]),
            "metrics": {
                "Municipal": "45.3%",
                "Part. Subvencionado": "54.7%", 
                "Matrícula Pública": "48.2%",
                "Matrícula Privada": "51.8%"
            },
            "charts": [
                {"chart_type": "pie", "title": "Distribución por Dependencia"},
                {"chart_type": "bar", "title": "Matrícula por Tipo de Establecimiento"},
            ]
        },
        "evolucion": {
            "title": html.Span([html.I(className="fas fa-chart-area me-2"), "Evolución Temporal del Sistema"]),
            "metrics": {
                "Crecimiento Anual": "+1.8%",
                "Nuevos Programas": "127", 
                "Especializaciones": "+12",
                "Inversión": "$2.4B"
            },
            "charts": [
                {"chart_type": "line", "title": "Evolución N° de Establecimientos"},
                {"chart_type": "bar", "title": "Nuevas Especialidades por Año"},
            ]
        }
    }
    
    if subtab not in contents:
        subtab = "geografia"
    
    content = contents[subtab]
    return create_section_layout(
        content["title"],
        content["metrics"], 
        content["charts"],
        include_table=True,
        custom_table_data=content.get("table_data")
    )


def create_proyectos_subtab_content(subtab):
    """Crea contenido específico para sub-pestañas de proyectos"""
    contents = {
        "recursos": {
            "title": html.Span([html.I(className="fas fa-dollar-sign me-2"), "Asignación de Recursos SEEMTP"]),
            "metrics": {
                "Inversión Total": "$4.2B",
                "Proyectos Activos": "245", 
                "Promedio por Proyecto": "$17.1M",
                "Cofinanciamiento": "35%"
            },
            "charts": [
                {"chart_type": "pie", "title": "Distribución de Recursos por Componente"},
                {"chart_type": "bar", "title": "Inversión por Región"},
            ]
        },
        "ejecucion": {
            "title": html.Span([html.I(className="fas fa-clipboard-list me-2"), "Ejecución Financiera"]),
            "metrics": {
                "% Ejecución": "87.3%",
                "Presupuesto Vigente": "$3.67B", 
                "Devengado": "$3.2B",
                "Por Ejecutar": "$1.0B"
            },
            "charts": [
                {"chart_type": "bar", "title": "Ejecución por Componente"},
                {"chart_type": "line", "title": "Evolución Mensual de Ejecución"},
            ]
        },
        "cobertura": {
            "title": html.Span([html.I(className="fas fa-map-marker-alt me-2"), "Cobertura Nacional"]),
            "metrics": {
                "Establecimientos Beneficiados": "412",
                "Estudiantes Impactados": "89,450", 
                "Cobertura Nacional": "42.6%",
                "Regiones Activas": "15"
            },
            "charts": [
                {"chart_type": "bar", "title": "Establecimientos Beneficiados por Región"},
                {"chart_type": "pie", "title": "Distribución por Tipo de Proyecto"},
            ]
        },
        "evolucion": {
            "title": html.Span([html.I(className="fas fa-chart-area me-2"), "Evolución Anual del Programa"]),
            "metrics": {
                "Años de Ejecución": "8",
                "Crecimiento Anual": "+15.2%", 
                "Meta 2025": "$5.5B",
                "Eficiencia": "92.1%"
            },
            "charts": [
                {"chart_type": "line", "title": "Evolución del Presupuesto Anual"},
                {"chart_type": "bar", "title": "Proyectos Nuevos por Año"},
            ]
        }
    }
    
    if subtab not in contents:
        subtab = "recursos"
    
    content = contents[subtab]
    return create_section_layout(
        content["title"],
        content["metrics"], 
        content["charts"],
        include_table=True,
        custom_table_data=content.get("table_data")
    )
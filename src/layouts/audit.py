"""
============================================================================
LAYOUT DE AUDITORÍA (ADMIN)
============================================================================
Dashboard para visualizar logs de accesos y acciones de usuarios
"""

import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

from src.utils.audit import audit_logger


def create_audit_layout():
    """Crea el layout de auditoría para administradores"""
    
    layout = html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2([
                    html.I(className="fas fa-clipboard-list me-2"),
                    "Auditoría del Sistema"
                ], className="mb-3"),
                html.P(
                    "Registro de accesos, acciones y uso del sistema por los usuarios",
                    className="text-muted"
                )
            ])
        ]),
        
        html.Hr(),
        
        # Filtros
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5([html.I(className="fas fa-filter me-2"), "Filtros"], className="card-title"),
                        dbc.Row([
                            # Rango de fechas
                            dbc.Col([
                                dbc.Label("Período"),
                                dcc.Dropdown(
                                    id='audit-date-range',
                                    options=[
                                        {'label': 'Último día', 'value': 1},
                                        {'label': 'Últimos 7 días', 'value': 7},
                                        {'label': 'Últimos 30 días', 'value': 30},
                                        {'label': 'Últimos 90 días', 'value': 90},
                                        {'label': 'Todo el historial', 'value': 9999}
                                    ],
                                    value=7,
                                    clearable=False
                                )
                            ], md=3),
                            
                            # Usuario
                            dbc.Col([
                                dbc.Label("Usuario"),
                                dcc.Dropdown(
                                    id='audit-user-filter',
                                    placeholder="Todos los usuarios",
                                    clearable=True
                                )
                            ], md=3),
                            
                            # Acción
                            dbc.Col([
                                dbc.Label("Tipo de Acción"),
                                dcc.Dropdown(
                                    id='audit-action-filter',
                                    options=[
                                        {'label': 'Todas', 'value': 'all'},
                                        {'label': 'Login', 'value': 'login'},
                                        {'label': 'Logout', 'value': 'logout'},
                                        {'label': 'Ver Dashboard', 'value': 'view_dashboard'},
                                        {'label': 'Exportar Datos', 'value': 'export_data'},
                                        {'label': 'Gestión de Usuarios', 'value': 'user_'},
                                        {'label': 'Permisos Denegados', 'value': 'permission_denied'}
                                    ],
                                    value='all',
                                    clearable=False
                                )
                            ], md=3),
                            
                            # Estado
                            dbc.Col([
                                dbc.Label("Estado"),
                                dcc.Dropdown(
                                    id='audit-status-filter',
                                    options=[
                                        {'label': 'Todos', 'value': 'all'},
                                        {'label': 'Exitoso', 'value': 'success'},
                                        {'label': 'Error', 'value': 'error'},
                                        {'label': 'Denegado', 'value': 'denied'}
                                    ],
                                    value='all',
                                    clearable=False
                                )
                            ], md=3)
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    [html.I(className="fas fa-sync-alt me-2"), "Actualizar"],
                                    id="btn-refresh-audit",
                                    color="primary",
                                    className="mt-3"
                                )
                            ])
                        ])
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Estadísticas resumidas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📊 Estadísticas del Período", className="card-title"),
                        html.Div(id='audit-stats-cards')
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Acciones por Día"),
                    dbc.CardBody([
                        dcc.Graph(id='audit-timeline-chart')
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("👥 Usuarios Más Activos"),
                    dbc.CardBody([
                        dcc.Graph(id='audit-users-chart')
                    ])
                ])
            ], md=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🎯 Distribución de Acciones"),
                    dbc.CardBody([
                        dcc.Graph(id='audit-actions-chart')
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Dashboards Más Visitados"),
                    dbc.CardBody([
                        dcc.Graph(id='audit-dashboards-chart')
                    ])
                ])
            ], md=6)
        ], className="mb-4"),
        
        # Tabla de logs detallada
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("📋 Registro Detallado de Auditoría", className="mb-0"),
                        dbc.Badge("Últimos 100 registros", color="info", className="ms-2")
                    ]),
                    dbc.CardBody([
                        html.Div(id='audit-logs-table')
                    ])
                ])
            ])
        ])
    ], className="p-4")
    
    return layout


def create_audit_stats_cards(stats: dict) -> dbc.Row:
    """
    Crea tarjetas con estadísticas de auditoría
    
    Args:
        stats: Diccionario con estadísticas
    
    Returns:
        Row con tarjetas de estadísticas
    """
    cards = [
        {
            'title': 'Total Acciones',
            'value': stats.get('total_actions', 0),
            'icon': 'fas fa-clipboard-check',
            'color': 'primary'
        },
        {
            'title': 'Usuarios Activos',
            'value': stats.get('unique_users', 0),
            'icon': 'fas fa-users',
            'color': 'success'
        },
        {
            'title': 'Logins Exitosos',
            'value': stats.get('logins', 0),
            'icon': 'fas fa-sign-in-alt',
            'color': 'info'
        },
        {
            'title': 'Logins Fallidos',
            'value': stats.get('failed_logins', 0),
            'icon': 'fas fa-exclamation-triangle',
            'color': 'warning'
        },
        {
            'title': 'Exportaciones',
            'value': stats.get('exports', 0),
            'icon': 'fas fa-download',
            'color': 'secondary'
        }
    ]
    
    cols = []
    for card in cards:
        cols.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className=f"{card['icon']} fa-2x text-{card['color']} mb-2"),
                            html.H3(card['value'], className="mb-0"),
                            html.P(card['title'], className="text-muted mb-0 small")
                        ], className="text-center")
                    ])
                ])
            ], width=12, md=2, className="mb-3 mb-md-0")
        )
    
    return dbc.Row(cols)


def create_audit_logs_table(logs_df: pd.DataFrame) -> dash_table.DataTable:
    """
    Crea tabla de logs de auditoría
    
    Args:
        logs_df: DataFrame con logs
    
    Returns:
        DataTable de Dash
    """
    if logs_df.empty:
        return html.P("No hay registros de auditoría para el período seleccionado", className="text-muted")
    
    # Formatear timestamp
    logs_df['timestamp_formatted'] = pd.to_datetime(logs_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Extraer detalles relevantes
    def extract_details(row):
        details = row['details']
        if not isinstance(details, dict):
            return ''
        
        if row['action'] == 'view_dashboard':
            return details.get('dashboard', '')
        elif row['action'] == 'export_data':
            return f"{details.get('export_type', '')} - {details.get('dashboard', '')}"
        elif 'user_' in row['action']:
            return f"Usuario: {details.get('target_user', '')}"
        else:
            return ', '.join(f"{k}: {v}" for k, v in details.items() if k and v)
    
    logs_df['details_str'] = logs_df.apply(extract_details, axis=1)
    
    # Mapear iconos de estado
    def status_icon(status):
        if status == 'success':
            return '✅'
        elif status == 'failed' or status == 'error':
            return '❌'
        elif status == 'denied':
            return '🚫'
        else:
            return '⚪'
    
    logs_df['status_icon'] = logs_df['status'].apply(status_icon)
    
    # Seleccionar columnas
    display_df = logs_df[[
        'timestamp_formatted', 'username', 'action', 'status_icon', 'details_str', 'ip_address'
    ]].copy()
    
    display_df.columns = ['Fecha/Hora', 'Usuario', 'Acción', 'Estado', 'Detalles', 'IP']
    
    # Crear tabla
    table = dash_table.DataTable(
        id='audit-logs-datatable',
        columns=[{"name": col, "id": col} for col in display_df.columns],
        data=display_df.head(100).to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '8px',
            'fontSize': '13px',
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_header={
            'backgroundColor': '#34536A',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#f8f9fa'
            },
            {
                'if': {
                    'filter_query': '{Estado} = "❌"',
                },
                'backgroundColor': '#ffe6e6'
            },
            {
                'if': {
                    'filter_query': '{Estado} = "🚫"',
                },
                'backgroundColor': '#fff3cd'
            }
        ],
        page_size=15,
        sort_action='native',
        filter_action='native'
    )
    
    return table


def create_timeline_chart(logs_df: pd.DataFrame) -> go.Figure:
    """Crea gráfico de línea de acciones por día"""
    if logs_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Agrupar por día
    logs_df['date'] = pd.to_datetime(logs_df['timestamp']).dt.date
    daily_counts = logs_df.groupby('date').size().reset_index(name='count')
    
    fig = px.line(
        daily_counts,
        x='date',
        y='count',
        title='',
        labels={'date': 'Fecha', 'count': 'Número de Acciones'},
        markers=True
    )
    
    fig.update_traces(line_color='#34536A', marker_size=8)
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
    
    return fig


def create_users_chart(stats: dict) -> go.Figure:
    """Crea gráfico de barras de usuarios más activos"""
    top_users = stats.get('top_users', {})
    
    if not top_users:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df = pd.DataFrame(list(top_users.items()), columns=['Usuario', 'Acciones'])
    df = df.sort_values('Acciones', ascending=True)
    
    fig = px.bar(
        df,
        x='Acciones',
        y='Usuario',
        orientation='h',
        title='',
        color='Acciones',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    
    return fig


def create_actions_chart(stats: dict) -> go.Figure:
    """Crea gráfico de pie de distribución de acciones"""
    top_actions = stats.get('top_actions', {})
    
    if not top_actions:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Mapear nombres de acciones a español
    action_labels = {
        'login': 'Login',
        'logout': 'Logout',
        'view_dashboard': 'Ver Dashboard',
        'export_data': 'Exportar Datos',
        'permission_denied': 'Permiso Denegado'
    }
    
    labels = [action_labels.get(action, action) for action in top_actions.keys()]
    values = list(top_actions.values())
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=['#34536A', '#B35A5A', '#C2A869', '#5A8AAD', '#8AAD5A'])
    )])
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True
    )
    
    return fig


def create_dashboards_chart(logs_df: pd.DataFrame) -> go.Figure:
    """Crea gráfico de dashboards más visitados"""
    if logs_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Filtrar solo vistas de dashboard
    dashboard_views = logs_df[logs_df['action'] == 'view_dashboard'].copy()
    
    if dashboard_views.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay visitas a dashboards registradas",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Extraer nombres de dashboards
    dashboards = []
    for _, row in dashboard_views.iterrows():
        if isinstance(row['details'], dict) and 'dashboard' in row['details']:
            dashboards.append(row['details']['dashboard'])
    
    if not dashboards:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos de dashboards",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Contar visitas
    dashboard_counts = pd.Series(dashboards).value_counts()
    
    fig = px.bar(
        x=dashboard_counts.values,
        y=dashboard_counts.index,
        orientation='h',
        title='',
        labels={'x': 'Visitas', 'y': 'Dashboard'}
    )
    
    fig.update_traces(marker_color='#B35A5A')
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

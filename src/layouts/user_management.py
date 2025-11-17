"""
============================================================================
LAYOUT DE GESTIÓN DE USUARIOS (ADMIN)
============================================================================
Interfaz para crear, editar y gestionar usuarios del sistema
"""

import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import pandas as pd

from src.utils.user_management import user_manager
from src.utils.auth import USER_PROFILES


def create_user_management_layout():
    """Crea el layout de gestión de usuarios para administradores"""
    
    layout = html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H2([
                    html.I(className="fas fa-users-cog me-2"),
                    "Gestión de Usuarios"
                ], className="mb-3"),
                html.P(
                    "Administración de cuentas, perfiles y permisos del sistema",
                    className="text-muted"
                )
            ])
        ]),
        
        html.Hr(),
        
        # Resumen de usuarios
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📊 Resumen de Usuarios", className="card-title"),
                        html.Div(id='user-summary-cards')
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Botón para agregar usuario
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    [html.I(className="fas fa-user-plus me-2"), "Crear Nuevo Usuario"],
                    id="btn-new-user",
                    color="primary",
                    className="mb-3"
                )
            ])
        ]),
        
        # Modal para crear/editar usuario
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="modal-user-title")),
            dbc.ModalBody([
                dbc.Form([
                    # Username
                    dbc.Row([
                        dbc.Label("Nombre de Usuario", html_for="input-username", width=3),
                        dbc.Col([
                            dbc.Input(
                                type="text",
                                id="input-username",
                                placeholder="ej: jperez",
                                required=True
                            ),
                            dbc.FormText("Debe ser único, sin espacios")
                        ], width=9)
                    ], className="mb-3"),
                    
                    # Full name
                    dbc.Row([
                        dbc.Label("Nombre Completo", html_for="input-fullname", width=3),
                        dbc.Col([
                            dbc.Input(
                                type="text",
                                id="input-fullname",
                                placeholder="ej: Juan Pérez González",
                                required=True
                            )
                        ], width=9)
                    ], className="mb-3"),
                    
                    # Email
                    dbc.Row([
                        dbc.Label("Email", html_for="input-email", width=3),
                        dbc.Col([
                            dbc.Input(
                                type="email",
                                id="input-email",
                                placeholder="ej: juan.perez@mineduc.cl"
                            )
                        ], width=9)
                    ], className="mb-3"),
                    
                    # Perfil
                    dbc.Row([
                        dbc.Label("Perfil", html_for="select-profile", width=3),
                        dbc.Col([
                            dbc.Select(
                                id="select-profile",
                                options=[
                                    {"label": f"{profile_info['name']} - {profile_info['description']}", 
                                     "value": profile}
                                    for profile, profile_info in USER_PROFILES.items()
                                ],
                                value="usuario"
                            )
                        ], width=9)
                    ], className="mb-3"),
                    
                    # Password
                    dbc.Row([
                        dbc.Label("Contraseña", html_for="input-password", width=3),
                        dbc.Col([
                            dbc.Input(
                                type="password",
                                id="input-password",
                                placeholder="Mínimo 6 caracteres"
                            ),
                            dbc.FormText("Dejar vacío para mantener contraseña actual (en modo edición)")
                        ], width=9)
                    ], className="mb-3"),
                    
                    # Hidden field para modo (create/edit)
                    dcc.Store(id='user-form-mode', data='create'),
                    dcc.Store(id='user-form-original-username', data='')
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Cancelar", id="btn-cancel-user", color="secondary", className="me-2"),
                dbc.Button("Guardar", id="btn-save-user", color="primary")
            ])
        ], id="modal-user-form", size="lg"),
        
        # Alertas
        html.Div(id='user-management-alert'),
        
        # Tabla de usuarios
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("👥 Lista de Usuarios")),
                    dbc.CardBody([
                        html.Div(id='users-table-container')
                    ])
                ])
            ])
        ])
    ], className="p-4")
    
    return layout


def create_users_table(users_df: pd.DataFrame) -> dash_table.DataTable:
    """
    Crea tabla interactiva de usuarios
    
    Args:
        users_df: DataFrame con información de usuarios
    
    Returns:
        DataTable de Dash
    """
    # Preparar datos para tabla
    if users_df.empty:
        return html.P("No hay usuarios registrados", className="text-muted")
    
    # Formatear datos
    users_df['created_at_formatted'] = pd.to_datetime(users_df['created_at']).dt.strftime('%Y-%m-%d')
    users_df['last_login_formatted'] = pd.to_datetime(users_df['last_login'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M')
    users_df['status'] = users_df['is_active'].apply(lambda x: '✅ Activo' if x == 1 else '🔒 Inactivo')
    
    # Seleccionar columnas para mostrar
    display_df = users_df[[
        'username', 'full_name', 'email', 'profile', 'status',
        'created_at_formatted', 'last_login_formatted'
    ]].copy()
    
    display_df.columns = [
        'Usuario', 'Nombre Completo', 'Email', 'Perfil', 'Estado',
        'Fecha Creación', 'Último Login'
    ]
    
    # Crear tabla
    table = dash_table.DataTable(
        id='users-datatable',
        columns=[
            {"name": col, "id": col} 
            for col in display_df.columns
        ],
        data=display_df.to_dict('records'),
        row_selectable='single',
        selected_rows=[],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontSize': '14px'
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
                    'filter_query': '{Estado} = "🔒 Inactivo"'
                },
                'opacity': 0.6
            }
        ],
        page_size=10,
        sort_action='native',
        filter_action='native'
    )
    
    # Botones de acción
    action_buttons = html.Div([
        dbc.ButtonGroup([
            dbc.Button(
                [html.I(className="fas fa-edit me-2"), "Editar"],
                id="btn-edit-user",
                color="warning",
                disabled=True,
                className="me-2"
            ),
            dbc.Button(
                [html.I(className="fas fa-lock me-2"), "Desactivar"],
                id="btn-deactivate-user",
                color="danger",
                disabled=True,
                className="me-2"
            ),
            dbc.Button(
                [html.I(className="fas fa-unlock me-2"), "Activar"],
                id="btn-activate-user",
                color="success",
                disabled=True
            )
        ])
    ], className="mb-3")
    
    return html.Div([action_buttons, table])


def create_user_summary_cards(user_counts: dict) -> dbc.Row:
    """
    Crea tarjetas de resumen de usuarios por perfil
    
    Args:
        user_counts: Diccionario con conteo por perfil
    
    Returns:
        Row con tarjetas de resumen
    """
    total_users = sum(user_counts.values())
    
    profile_icons = {
        'usuario': 'fas fa-user',
        'analista': 'fas fa-user-tie',
        'admin': 'fas fa-user-shield'
    }
    
    profile_colors = {
        'usuario': 'primary',
        'analista': 'info',
        'admin': 'danger'
    }
    
    cards = []
    
    # Tarjeta de total
    cards.append(
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-users fa-2x text-success mb-2"),
                        html.H4(total_users, className="mb-0"),
                        html.P("Total Usuarios", className="text-muted mb-0")
                    ], className="text-center")
                ])
            ], className="h-100")
        ], md=3)
    )
    
    # Tarjetas por perfil
    for profile, count in user_counts.items():
        profile_info = USER_PROFILES[profile]
        
        cards.append(
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className=f"{profile_icons[profile]} fa-2x text-{profile_colors[profile]} mb-2"),
                            html.H4(count, className="mb-0"),
                            html.P(profile_info['name'], className="text-muted mb-0")
                        ], className="text-center")
                    ])
                ], className="h-100")
            ], md=3)
        )
    
    return dbc.Row(cards, className="g-3")

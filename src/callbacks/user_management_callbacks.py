"""
============================================================================
CALLBACKS DE GESTIÓN DE USUARIOS
============================================================================
Manejo de eventos de creación, edición y gestión de usuarios
"""

from dash import Input, Output, State, callback_context, no_update
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd

from src.utils.user_management import user_manager
from src.utils.audit import audit_logger
from src.layouts.user_management import create_users_table, create_user_summary_cards


def register_user_management_callbacks(app):
    """Registra callbacks de gestión de usuarios"""
    
    # Cargar datos iniciales cuando se accede a la página
    @app.callback(
        [Output('users-table-container', 'children'),
         Output('user-summary-cards', 'children'),
         Output('audit-user-filter', 'options')],
        Input('url', 'pathname')
    )
    def load_users_data(pathname):
        """Carga datos de usuarios y opciones de filtros"""
        if pathname != '/gestion-usuarios':
            return no_update, no_update, no_update
        
        # Obtener usuarios
        users = user_manager.get_all_users(include_inactive=True)
        users_df = pd.DataFrame(users) if users else pd.DataFrame()
        
        # Tabla
        table = create_users_table(users_df)
        
        # Tarjetas de resumen
        counts = user_manager.get_user_count_by_profile()
        cards = create_user_summary_cards(counts)
        
        # Opciones de filtro de auditoría
        user_options = [{'label': u['username'], 'value': u['username']} for u in users]
        
        return table, cards, user_options
    
    # Abrir/cerrar modal y cargar datos según modo
    @app.callback(
        [Output('modal-user-form', 'is_open'),
         Output('modal-user-title', 'children'),
         Output('user-form-mode', 'data'),
         Output('input-username', 'value'),
         Output('input-username', 'disabled'),
         Output('input-fullname', 'value'),
         Output('input-email', 'value'),
         Output('select-profile', 'value'),
         Output('input-password', 'value'),
         Output('user-form-original-username', 'data')],
        [Input('btn-new-user', 'n_clicks'),
         Input('btn-edit-user', 'n_clicks'),
         Input('btn-cancel-user', 'n_clicks'),
         Input('btn-save-user', 'n_clicks')],
        [State('users-datatable', 'selected_rows'),
         State('users-datatable', 'data')],
        prevent_initial_call=True
    )
    def toggle_user_modal(n_new, n_edit, n_cancel, n_save, selected_rows, table_data):
        """Controla apertura/cierre del modal de usuario"""
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Cerrar modal
        if button_id in ['btn-cancel-user', 'btn-save-user']:
            return False, '', 'create', '', False, '', '', 'usuario', '', ''
        
        # Crear nuevo usuario
        if button_id == 'btn-new-user':
            return True, 'Crear Nuevo Usuario', 'create', '', False, '', '', 'usuario', '', ''
        
        # Editar usuario
        if button_id == 'btn-edit-user' and selected_rows and table_data:
            selected_user = table_data[selected_rows[0]]
            username = selected_user['Usuario']
            user_data = user_manager.get_user(username)
            
            if user_data:
                return (
                    True,
                    f'Editar Usuario: {username}',
                    'edit',
                    username,
                    True,  # Deshabilitar campo username en modo edición
                    user_data['full_name'],
                    user_data['email'] or '',
                    user_data['profile'],
                    '',
                    username
                )
        
        return no_update
    
    # Guardar usuario (crear o editar)
    @app.callback(
        [Output('user-management-alert', 'children'),
         Output('users-table-container', 'children', allow_duplicate=True),
         Output('user-summary-cards', 'children', allow_duplicate=True)],
        Input('btn-save-user', 'n_clicks'),
        [State('user-form-mode', 'data'),
         State('input-username', 'value'),
         State('input-fullname', 'value'),
         State('input-email', 'value'),
         State('select-profile', 'value'),
         State('input-password', 'value'),
         State('session-store', 'data')],
        prevent_initial_call=True
    )
    def save_user(n_clicks, mode, username, fullname, email, profile, password, session):
        """Guarda (crea o edita) un usuario"""
        if not n_clicks:
            return no_update, no_update, no_update
        
        admin_username = session.get('user_info', {}).get('username', 'admin')
        
        # Crear usuario
        if mode == 'create':
            if not username or not fullname or not password:
                return (
                    dbc.Alert("❌ Username, nombre completo y contraseña son obligatorios", color="danger"),
                    no_update,
                    no_update
                )
            
            if len(password) < 6:
                return (
                    dbc.Alert("❌ La contraseña debe tener al menos 6 caracteres", color="danger"),
                    no_update,
                    no_update
                )
            
            result = user_manager.create_user(
                username=username,
                password=password,
                profile=profile,
                full_name=fullname,
                email=email,
                created_by=admin_username
            )
            
            if result['success']:
                audit_logger.log_user_management(admin_username, 'created', username, {'profile': profile})
                
                # Recargar tabla y tarjetas
                users = user_manager.get_all_users(include_inactive=True)
                users_df = pd.DataFrame(users) if users else pd.DataFrame()
                table = create_users_table(users_df)
                counts = user_manager.get_user_count_by_profile()
                cards = create_user_summary_cards(counts)
                
                return (
                    dbc.Alert(f"✅ {result['message']}", color="success", duration=4000),
                    table,
                    cards
                )
            else:
                return (
                    dbc.Alert(f"❌ {result['error']}", color="danger"),
                    no_update,
                    no_update
                )
        
        # Editar usuario
        elif mode == 'edit':
            update_data = {
                'username': username,
                'full_name': fullname,
                'email': email,
                'profile': profile
            }
            
            if password:
                if len(password) < 6:
                    return (
                        dbc.Alert("❌ La contraseña debe tener al menos 6 caracteres", color="danger"),
                        no_update,
                        no_update
                    )
                update_data['password'] = password
            
            result = user_manager.update_user(**update_data)
            
            if result['success']:
                audit_logger.log_user_management(admin_username, 'updated', username, {'profile': profile})
                
                # Recargar tabla y tarjetas
                users = user_manager.get_all_users(include_inactive=True)
                users_df = pd.DataFrame(users) if users else pd.DataFrame()
                table = create_users_table(users_df)
                counts = user_manager.get_user_count_by_profile()
                cards = create_user_summary_cards(counts)
                
                return (
                    dbc.Alert(f"✅ {result['message']}", color="success", duration=4000),
                    table,
                    cards
                )
            else:
                return (
                    dbc.Alert(f"❌ {result['error']}", color="danger"),
                    no_update,
                    no_update
                )
        
        return no_update, no_update, no_update
    
    # Activar/Desactivar botones según selección en tabla
    @app.callback(
        [Output('btn-edit-user', 'disabled'),
         Output('btn-deactivate-user', 'disabled'),
         Output('btn-activate-user', 'disabled')],
        Input('users-datatable', 'selected_rows'),
        State('users-datatable', 'data'),
        prevent_initial_call=True
    )
    def toggle_action_buttons(selected_rows, table_data):
        """Habilita/deshabilita botones según usuario seleccionado"""
        if not selected_rows or not table_data:
            return True, True, True
        
        selected_user = table_data[selected_rows[0]]
        is_active = '✅' in selected_user['Estado']
        
        # Editar: siempre habilitado
        # Desactivar: solo si está activo
        # Activar: solo si está inactivo
        return False, not is_active, is_active
    
    # Desactivar usuario
    @app.callback(
        [Output('user-management-alert', 'children', allow_duplicate=True),
         Output('users-table-container', 'children', allow_duplicate=True),
         Output('user-summary-cards', 'children', allow_duplicate=True)],
        Input('btn-deactivate-user', 'n_clicks'),
        [State('users-datatable', 'selected_rows'),
         State('users-datatable', 'data'),
         State('session-store', 'data')],
        prevent_initial_call=True
    )
    def deactivate_user(n_clicks, selected_rows, table_data, session):
        """Desactiva un usuario seleccionado"""
        if not n_clicks or not selected_rows or not table_data:
            return no_update, no_update, no_update
        
        username = table_data[selected_rows[0]]['Usuario']
        admin_username = session.get('user_info', {}).get('username', 'admin')
        
        result = user_manager.deactivate_user(username)
        
        if result['success']:
            audit_logger.log_user_management(admin_username, 'deactivated', username)
            
            # Recargar tabla y tarjetas
            users = user_manager.get_all_users(include_inactive=True)
            users_df = pd.DataFrame(users) if users else pd.DataFrame()
            table = create_users_table(users_df)
            counts = user_manager.get_user_count_by_profile()
            cards = create_user_summary_cards(counts)
            
            return (
                dbc.Alert(f"✅ {result['message']}", color="success", duration=4000),
                table,
                cards
            )
        else:
            return (
                dbc.Alert(f"❌ {result['error']}", color="danger"),
                no_update,
                no_update
            )
    
    # Activar usuario
    @app.callback(
        [Output('user-management-alert', 'children', allow_duplicate=True),
         Output('users-table-container', 'children', allow_duplicate=True),
         Output('user-summary-cards', 'children', allow_duplicate=True)],
        Input('btn-activate-user', 'n_clicks'),
        [State('users-datatable', 'selected_rows'),
         State('users-datatable', 'data'),
         State('session-store', 'data')],
        prevent_initial_call=True
    )
    def activate_user(n_clicks, selected_rows, table_data, session):
        """Activa un usuario previamente desactivado"""
        if not n_clicks or not selected_rows or not table_data:
            return no_update, no_update, no_update
        
        username = table_data[selected_rows[0]]['Usuario']
        admin_username = session.get('user_info', {}).get('username', 'admin')
        
        result = user_manager.activate_user(username)
        
        if result['success']:
            audit_logger.log_user_management(admin_username, 'activated', username)
            
            # Recargar tabla y tarjetas
            users = user_manager.get_all_users(include_inactive=True)
            users_df = pd.DataFrame(users) if users else pd.DataFrame()
            table = create_users_table(users_df)
            counts = user_manager.get_user_count_by_profile()
            cards = create_user_summary_cards(counts)
            
            return (
                dbc.Alert(f"✅ {result['message']}", color="success", duration=4000),
                table,
                cards
            )
        else:
            return (
                dbc.Alert(f"❌ {result['error']}", color="danger"),
                no_update,
                no_update
            )

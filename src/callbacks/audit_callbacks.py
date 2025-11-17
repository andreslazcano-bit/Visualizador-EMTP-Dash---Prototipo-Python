"""
============================================================================
CALLBACKS DE AUDITORÍA
============================================================================
Manejo de visualización y filtrado de logs de auditoría
"""

from dash import Input, Output, State, no_update
from datetime import datetime, timedelta
import pandas as pd

from src.utils.audit import audit_logger
from src.layouts.audit import (
    create_audit_stats_cards,
    create_audit_logs_table,
    create_timeline_chart,
    create_users_chart,
    create_actions_chart,
    create_dashboards_chart
)


def register_audit_callbacks(app):
    """Registra callbacks de auditoría"""
    
    @app.callback(
        [Output('audit-stats-cards', 'children'),
         Output('audit-logs-table', 'children'),
         Output('audit-timeline-chart', 'figure'),
         Output('audit-users-chart', 'figure'),
         Output('audit-actions-chart', 'figure'),
         Output('audit-dashboards-chart', 'figure')],
        [Input('btn-refresh-audit', 'n_clicks'),
         Input('audit-date-range', 'value'),
         Input('audit-user-filter', 'value'),
         Input('audit-action-filter', 'value'),
         Input('audit-status-filter', 'value')],
        prevent_initial_call=False
    )
    def update_audit_dashboard(n_clicks, days, user_filter, action_filter, status_filter):
        """Actualiza dashboard de auditoría con filtros aplicados"""
        
        # Calcular fechas
        if days == 9999:  # Todo el historial
            start_date = None
        else:
            start_date = datetime.now() - timedelta(days=days)
        
        # Preparar filtros base
        filters = {}
        if start_date:
            filters['start_date'] = start_date
        
        # Aplicar filtro de usuario
        if user_filter:
            filters['username'] = user_filter
        
        # Aplicar filtro de estado
        if status_filter and status_filter != 'all':
            filters['status'] = status_filter
        
        # Obtener logs con filtros
        logs_df = audit_logger.get_audit_logs(**filters)
        
        # Aplicar filtro de acción (post-procesamiento para acciones que empiezan con 'user_')
        if action_filter and action_filter != 'all':
            if action_filter == 'user_':
                # Filtrar acciones que empiezan con user_
                logs_df = logs_df[logs_df['action'].str.startswith('user_')] if not logs_df.empty else logs_df
            else:
                # Filtro exacto de acción
                logs_df = logs_df[logs_df['action'] == action_filter] if not logs_df.empty else logs_df
        
        # Obtener estadísticas
        stats = audit_logger.get_statistics(days=days if days != 9999 else 365)
        
        # Crear componentes
        stats_cards = create_audit_stats_cards(stats)
        logs_table = create_audit_logs_table(logs_df)
        timeline_chart = create_timeline_chart(logs_df)
        users_chart = create_users_chart(stats)
        actions_chart = create_actions_chart(stats)
        dashboards_chart = create_dashboards_chart(logs_df)
        
        return stats_cards, logs_table, timeline_chart, users_chart, actions_chart, dashboards_chart

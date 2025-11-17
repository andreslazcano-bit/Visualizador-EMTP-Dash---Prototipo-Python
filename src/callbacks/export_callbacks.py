"""
============================================================================
CALLBACKS PARA EXPORTACIÓN DE DATOS
============================================================================
Maneja las exportaciones de datos a CSV, Excel y PDF con auditoría completa
"""

from dash import Input, Output, State, callback, dcc, no_update
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime
from src.utils.audit import audit_logger
import io


def register_export_callbacks(app):
    """Registra todos los callbacks para exportación de datos"""
    
    # Lista de secciones que tienen exportación
    sections = [
        'matricula-evolucion',
        'matricula-demografia', 
        'matricula-retencion',
        'matricula-comparacion',
        'egresados-transicion',
        'egresados-empleabilidad',
        'titulacion-tasas',
        'titulacion-tiempo',
        'establecimientos-geografia',
        'establecimientos-infraestructura',
        'docentes-perfil',
        'docentes-capacitacion'
    ]
    
    # Registrar callbacks para cada sección y tipo de exportación
    for section in sections:
        # CSV Export
        @app.callback(
            Output(f'export-{section}-csv-download', 'data'),
            Input(f'export-{section}-csv', 'n_clicks'),
            State('session-store', 'data'),
            prevent_initial_call=True
        )
        def export_csv(n_clicks, session_data, section=section):
            """Exporta datos a CSV y registra en auditoría"""
            if not n_clicks:
                raise PreventUpdate
            
            # Obtener username
            username = 'desconocido'
            if session_data and 'username' in session_data:
                username = session_data.get('username', 'desconocido')
            
            # Extraer nombre del dashboard y subtab
            parts = section.split('-')
            dashboard = parts[0] if len(parts) > 0 else 'desconocido'
            subtab = parts[1] if len(parts) > 1 else ''
            
            # Registrar exportación en auditoría
            audit_logger.log_export_data(
                username=username,
                export_type='csv',
                dashboard=dashboard,
                details={'subtab': subtab, 'section': section}
            )
            
            print(f"📊 Exportación CSV: {username} exportó {dashboard}/{subtab}")
            
            # TODO: Generar datos reales del dashboard actual
            # Por ahora, datos de ejemplo
            df = pd.DataFrame({
                'Dashboard': [dashboard],
                'Subtab': [subtab],
                'Exportado por': [username],
                'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            })
            
            return dcc.send_data_frame(
                df.to_csv,
                f"export_{dashboard}_{subtab}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                index=False
            )
        
        # Excel Export
        @app.callback(
            Output(f'export-{section}-excel-download', 'data'),
            Input(f'export-{section}-excel', 'n_clicks'),
            State('session-store', 'data'),
            prevent_initial_call=True
        )
        def export_excel(n_clicks, session_data, section=section):
            """Exporta datos a Excel y registra en auditoría"""
            if not n_clicks:
                raise PreventUpdate
            
            # Obtener username
            username = 'desconocido'
            if session_data and 'username' in session_data:
                username = session_data.get('username', 'desconocido')
            
            # Extraer nombre del dashboard y subtab
            parts = section.split('-')
            dashboard = parts[0] if len(parts) > 0 else 'desconocido'
            subtab = parts[1] if len(parts) > 1 else ''
            
            # Registrar exportación en auditoría
            audit_logger.log_export_data(
                username=username,
                export_type='excel',
                dashboard=dashboard,
                details={'subtab': subtab, 'section': section}
            )
            
            print(f"📊 Exportación Excel: {username} exportó {dashboard}/{subtab}")
            
            # TODO: Generar datos reales del dashboard actual
            # Por ahora, datos de ejemplo
            df = pd.DataFrame({
                'Dashboard': [dashboard],
                'Subtab': [subtab],
                'Exportado por': [username],
                'Fecha': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            })
            
            return dcc.send_data_frame(
                df.to_excel,
                f"export_{dashboard}_{subtab}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                index=False,
                sheet_name='Datos'
            )
        
        # PDF Export
        @app.callback(
            Output(f'export-{section}-pdf-alert', 'children'),
            Input(f'export-{section}-pdf', 'n_clicks'),
            State('session-store', 'data'),
            prevent_initial_call=True
        )
        def export_pdf(n_clicks, session_data, section=section):
            """Registra intento de exportación a PDF (funcionalidad pendiente)"""
            if not n_clicks:
                raise PreventUpdate
            
            # Obtener username
            username = 'desconocido'
            if session_data and 'username' in session_data:
                username = session_data.get('username', 'desconocido')
            
            # Extraer nombre del dashboard y subtab
            parts = section.split('-')
            dashboard = parts[0] if len(parts) > 0 else 'desconocido'
            subtab = parts[1] if len(parts) > 1 else ''
            
            # Registrar exportación en auditoría
            audit_logger.log_export_data(
                username=username,
                export_type='pdf',
                dashboard=dashboard,
                details={'subtab': subtab, 'section': section, 'status': 'pendiente'}
            )
            
            print(f"📊 Exportación PDF solicitada: {username} - {dashboard}/{subtab}")
            
            return "Exportación a PDF en desarrollo"

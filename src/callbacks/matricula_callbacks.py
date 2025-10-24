"""
============================================================================
CALLBACKS MATRÍCULA
============================================================================
"""

from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from loguru import logger


def register_matricula_callbacks(app):
    """Registra callbacks del módulo de matrícula"""
    
    @app.callback(
        [
            Output("kpi-total-estudiantes", "children"),
            Output("kpi-total-establecimientos", "children"),
            Output("kpi-total-especialidades", "children"),
            Output("kpi-ratio-genero", "children"),
        ],
        [
            Input("btn-apply-filters-matricula", "n_clicks"),
        ],
        [
            State("filter-region-matricula", "value"),
            State("filter-comuna-matricula", "value"),
        ],
        prevent_initial_call=False
    )
    def update_kpis_matricula(n_clicks, region, comuna):
        """Actualiza KPIs de matrícula - DATOS DE EJEMPLO"""
        # Datos de ejemplo mientras no hay datos reales
        return "15,234", "342", "45", "1.2:1"
    
    @app.callback(
        Output("graph-matricula-region", "figure"),
        [
            Input("btn-apply-filters-matricula", "n_clicks"),
        ],
        prevent_initial_call=False
    )
    def update_graph_region(n_clicks):
        """Actualiza gráfico de matrícula por región - DATOS DE EJEMPLO"""
        # Crear datos de ejemplo
        df_ejemplo = pd.DataFrame({
            'Region': ['Metropolitana', 'Valparaíso', 'Biobío', 'Araucanía', 'Los Lagos'],
            'Matricula': [5200, 3100, 2800, 1900, 2100]
        })
        
        fig = px.bar(
            df_ejemplo,
            x='Region',
            y='Matricula',
            title="📊 Matrícula por Región (Datos de Ejemplo)",
            template='plotly_white',
            color='Matricula',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            showlegend=False,
            xaxis_title="Región",
            yaxis_title="Número de Estudiantes"
        )
        
        return fig
    
    @app.callback(
        Output("graph-matricula-especialidades", "figure"),
        [
            Input("btn-apply-filters-matricula", "n_clicks"),
        ],
        prevent_initial_call=False
    )
    def update_graph_especialidades(n_clicks):
        """Actualiza gráfico de especialidades - DATOS DE EJEMPLO"""
        # Crear datos de ejemplo
        df_ejemplo = pd.DataFrame({
            'Especialidad': ['Administración', 'Contabilidad', 'Electricidad', 
                           'Mecánica', 'Enfermería', 'Gastronomía'],
            'Matricula': [1800, 1500, 1200, 1100, 900, 800]
        })
        
        fig = px.bar(
            df_ejemplo,
            x='Matricula',
            y='Especialidad',
            title="🎓 Top Especialidades (Datos de Ejemplo)",
            template='plotly_white',
            orientation='h',
            color='Matricula',
            color_continuous_scale='Greens'
        )
        
        fig.update_layout(
            showlegend=False,
            xaxis_title="Número de Estudiantes",
            yaxis_title="Especialidad"
        )
        
        return fig
    
    logger.info("✅ Callbacks de matrícula registrados (modo demo)")

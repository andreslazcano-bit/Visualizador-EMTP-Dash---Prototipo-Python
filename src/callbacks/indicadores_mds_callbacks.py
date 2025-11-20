"""
============================================================================
CALLBACKS - INDICADORES MDS
============================================================================
Callbacks para los indicadores del Ministerio de Desarrollo Social
"""

from dash import Input, Output, State, callback, no_update
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime


def register_indicadores_mds_callbacks(app):
    """Registra todos los callbacks de Indicadores MDS"""
    
    # =======================================================================
    # INDICADORES DE PROPÓSITO
    # =======================================================================
    
    # Indicador 1: Ingreso a Educación Superior
    @app.callback(
        [Output('mds-prop1-kpi-actual', 'children'),
         Output('mds-prop1-kpi-variacion', 'children'),
         Output('mds-prop1-kpi-total', 'children'),
         Output('mds-prop1-kpi-es', 'children'),
         Output('mds-prop1-evolucion', 'figure'),
         Output('mds-prop1-region', 'figure'),
         Output('mds-prop1-especialidad', 'figure')],
        [Input('mds-tabs', 'active_tab')]
    )
    def update_prop1_ingreso_es(active_tab):
        """Actualiza indicador de ingreso a educación superior"""
        
        if active_tab != 'tab-proposito':
            return [no_update] * 7
        
        # Datos simulados
        total_egresados_2024 = 45230
        ingreso_es_2024 = 23115  # 51.1%
        porcentaje_2024 = (ingreso_es_2024 / total_egresados_2024) * 100
        porcentaje_2023 = 47.3
        variacion = porcentaje_2024 - porcentaje_2023
        
        # KPIs
        kpi_actual = f"{porcentaje_2024:.1f}%"
        kpi_variacion = f"+{variacion:.1f}%" if variacion >= 0 else f"{variacion:.1f}%"
        kpi_total = f"{total_egresados_2024:,}".replace(',', '.')
        kpi_es = f"{ingreso_es_2024:,}".replace(',', '.')
        
        # Gráfico 1: Evolución temporal
        años = list(range(2019, 2025))
        porcentajes = [42.5, 43.8, 44.2, 45.6, 47.3, porcentaje_2024]
        
        fig_evolucion = go.Figure()
        fig_evolucion.add_trace(go.Scatter(
            x=años,
            y=porcentajes,
            mode='lines+markers',
            name='% Ingreso ES',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=10),
            text=[f"{p:.1f}%" for p in porcentajes],
            textposition='top center'
        ))
        
        fig_evolucion.add_hline(
            y=50,
            line_dash="dash",
            line_color="green",
            annotation_text="Meta 50%",
            annotation_position="right"
        )
        
        fig_evolucion.update_layout(
            title="Evolución del Ingreso a Educación Superior",
            xaxis_title="Año",
            yaxis_title="Porcentaje (%)",
            hovermode='x unified',
            template='plotly_white'
        )
        
        # Gráfico 2: Por región
        regiones = [
            'Metropolitana', 'Valparaíso', 'Biobío', "O'Higgins", 'Maule',
            'Antofagasta', 'Coquimbo', 'La Araucanía', 'Los Lagos', 'Tarapacá'
        ]
        porcentajes_region = [58.2, 54.1, 52.3, 51.7, 49.8, 48.5, 47.2, 46.1, 44.8, 43.2]
        
        fig_region = go.Figure(go.Bar(
            x=porcentajes_region,
            y=regiones,
            orientation='h',
            marker_color='#06D6A0',
            text=[f"{p}%" for p in porcentajes_region],
            textposition='outside'
        ))
        
        fig_region.update_layout(
            title="Ingreso a ES por Región (2024)",
            xaxis_title="Porcentaje (%)",
            yaxis_title="",
            template='plotly_white',
            height=400
        )
        
        # Gráfico 3: Por especialidad
        especialidades = [
            'Administración', 'Contabilidad', 'Electricidad', 'Electrónica',
            'Construcción', 'Mecánica', 'Enfermería', 'Párvulos', 'Programación',
            'Gastronomía', 'Turismo', 'Agrícola'
        ]
        porcentajes_esp = [62.5, 58.3, 54.1, 52.7, 49.2, 48.5, 61.8, 59.3, 65.2, 42.1, 45.3, 38.7]
        
        fig_especialidad = go.Figure(go.Bar(
            x=especialidades,
            y=porcentajes_esp,
            marker_color='#F77F00',
            text=[f"{p}%" for p in porcentajes_esp],
            textposition='outside'
        ))
        
        fig_especialidad.update_layout(
            title="Ingreso a ES por Especialidad (2024)",
            xaxis_title="Especialidad",
            yaxis_title="Porcentaje (%)",
            template='plotly_white',
            xaxis_tickangle=-45,
            height=400
        )
        
        return kpi_actual, kpi_variacion, kpi_total, kpi_es, fig_evolucion, fig_region, fig_especialidad
    
    # Indicador 2: Competencias Docentes
    @app.callback(
        [Output('mds-prop2-kpi-actual', 'children'),
         Output('mds-prop2-kpi-capacitados', 'children'),
         Output('mds-prop2-kpi-mejoraron', 'children'),
         Output('mds-prop2-kpi-meta', 'children'),
         Output('mds-prop2-evolucion', 'figure'),
         Output('mds-prop2-region', 'figure')],
        [Input('mds-tabs', 'active_tab')]
    )
    def update_prop2_competencias_docentes(active_tab):
        """Actualiza indicador de competencias docentes"""
        
        if active_tab != 'tab-proposito':
            return [no_update] * 6
        
        # Datos simulados
        capacitados_2024 = 3250
        mejoraron_2024 = 2762  # 85%
        porcentaje_2024 = (mejoraron_2024 / capacitados_2024) * 100
        meta_anual = 80
        
        # KPIs
        kpi_actual = f"{porcentaje_2024:.1f}%"
        kpi_capacitados = f"{capacitados_2024:,}".replace(',', '.')
        kpi_mejoraron = f"{mejoraron_2024:,}".replace(',', '.')
        kpi_meta = f"{meta_anual}%"
        
        # Gráfico 1: Evolución anual
        años = list(range(2020, 2025))
        porcentajes = [72.5, 75.3, 78.8, 82.1, porcentaje_2024]
        
        fig_evolucion = go.Figure()
        fig_evolucion.add_trace(go.Bar(
            x=años,
            y=porcentajes,
            marker_color=['#A0C4FF', '#A0C4FF', '#A0C4FF', '#A0C4FF', '#2E86AB'],
            text=[f"{p:.1f}%" for p in porcentajes],
            textposition='outside'
        ))
        
        fig_evolucion.add_hline(
            y=meta_anual,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Meta {meta_anual}%",
            annotation_position="right"
        )
        
        fig_evolucion.update_layout(
            title="Evolución de Mejora en Competencias Docentes",
            xaxis_title="Año",
            yaxis_title="Porcentaje (%)",
            template='plotly_white'
        )
        
        # Gráfico 2: Por región
        regiones = [
            'Metropolitana', 'Valparaíso', 'Biobío', "O'Higgins", 'Maule',
            'Antofagasta', 'Coquimbo', 'La Araucanía'
        ]
        porcentajes_region = [88.5, 86.2, 85.1, 84.3, 83.7, 82.1, 81.5, 80.2]
        
        fig_region = go.Figure(go.Bar(
            x=regiones,
            y=porcentajes_region,
            marker_color='#06D6A0',
            text=[f"{p}%" for p in porcentajes_region],
            textposition='outside'
        ))
        
        fig_region.add_hline(
            y=meta_anual,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Meta {meta_anual}%"
        )
        
        fig_region.update_layout(
            title="Mejora en Competencias por Región (2024)",
            xaxis_title="Región",
            yaxis_title="Porcentaje (%)",
            template='plotly_white',
            xaxis_tickangle=-45
        )
        
        return kpi_actual, kpi_capacitados, kpi_mejoraron, kpi_meta, fig_evolucion, fig_region
    
    # =======================================================================
    # INDICADORES COMPLEMENTARIOS
    # =======================================================================
    
    # Indicador Complementario 1: Mejora de Equipamiento
    @app.callback(
        [Output('mds-comp1-kpi-actual', 'children'),
         Output('mds-comp1-kpi-total-ee', 'children'),
         Output('mds-comp1-kpi-mejorados', 'children'),
         Output('mds-comp1-kpi-periodo', 'children'),
         Output('mds-comp1-evolucion', 'figure'),
         Output('mds-comp1-equipamiento', 'figure'),
         Output('mds-comp1-region', 'figure')],
        [Input('mds-tabs', 'active_tab')]
    )
    def update_comp1_equipamiento(active_tab):
        """Actualiza indicador de mejora de equipamiento"""
        
        if active_tab != 'tab-complementarios':
            return [no_update] * 7
        
        # Datos simulados
        total_ee = 1050
        ee_mejorados = 683  # 65%
        porcentaje = (ee_mejorados / total_ee) * 100
        periodo = "2022-2024"
        
        # KPIs
        kpi_actual = f"{porcentaje:.1f}%"
        kpi_total = f"{total_ee:,}".replace(',', '.')
        kpi_mejorados = f"{ee_mejorados:,}".replace(',', '.')
        kpi_periodo = periodo
        
        # Gráfico 1: Evolución últimos 3 años
        años = ['2022', '2023', '2024']
        ee_por_año = [215, 238, 230]
        acumulado = np.cumsum(ee_por_año)
        
        fig_evolucion = go.Figure()
        fig_evolucion.add_trace(go.Bar(
            x=años,
            y=ee_por_año,
            name='EE Mejorados (año)',
            marker_color='#2E86AB',
            text=ee_por_año,
            textposition='outside'
        ))
        
        fig_evolucion.add_trace(go.Scatter(
            x=años,
            y=acumulado,
            name='Acumulado',
            mode='lines+markers',
            line=dict(color='#F77F00', width=3),
            marker=dict(size=10),
            text=acumulado,
            textposition='top center',
            yaxis='y2'
        ))
        
        fig_evolucion.update_layout(
            title="Evolución de EE con Equipamiento Mejorado",
            xaxis_title="Año",
            yaxis_title="EE Mejorados (año)",
            yaxis2=dict(title='EE Acumulado', overlaying='y', side='right'),
            template='plotly_white',
            hovermode='x unified'
        )
        
        # Gráfico 2: Por tipo de equipamiento
        tipos = [
            'Equipos Tecnológicos', 'Maquinaria Industrial', 'Laboratorios',
            'Herramientas', 'Mobiliario', 'Equipos Deportivos'
        ]
        cantidad = [245, 198, 156, 142, 98, 44]
        
        fig_tipo = go.Figure(go.Pie(
            labels=tipos,
            values=cantidad,
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set3)
        ))
        
        fig_tipo.update_layout(
            title="Distribución por Tipo de Equipamiento",
            template='plotly_white'
        )
        
        # Gráfico 3: Por región
        regiones = [
            'Metropolitana', 'Biobío', 'Valparaíso', "O'Higgins", 'Maule',
            'Antofagasta', 'La Araucanía', 'Los Lagos'
        ]
        porcentajes_region = [72.3, 68.5, 66.2, 64.1, 63.5, 61.8, 59.2, 58.1]
        
        fig_region = go.Figure(go.Bar(
            x=regiones,
            y=porcentajes_region,
            marker_color='#06D6A0',
            text=[f"{p}%" for p in porcentajes_region],
            textposition='outside'
        ))
        
        fig_region.update_layout(
            title="% EE con Equipamiento Mejorado por Región",
            xaxis_title="Región",
            yaxis_title="Porcentaje (%)",
            template='plotly_white',
            xaxis_tickangle=-45
        )
        
        return kpi_actual, kpi_total, kpi_mejorados, kpi_periodo, fig_evolucion, fig_tipo, fig_region
    
    # Indicador Complementario 2: SLEP - UAT-TP
    @app.callback(
        [Output('mds-comp2-kpi-actual', 'children'),
         Output('mds-comp2-kpi-total', 'children'),
         Output('mds-comp2-kpi-mejorados', 'children'),
         Output('mds-comp2-kpi-programa', 'children'),
         Output('mds-comp2-slep', 'figure'),
         Output('mds-comp2-competencias', 'figure')],
        [Input('mds-tabs', 'active_tab')]
    )
    def update_comp2_slep(active_tab):
        """Actualiza indicador de SLEP con UAT-TP"""
        
        if active_tab != 'tab-complementarios':
            return [no_update] * 6
        
        # Datos simulados
        total_slep = 11  # Total de SLEP en Chile
        slep_mejorados = 8  # 72.7%
        slep_en_programa = 10
        porcentaje = (slep_mejorados / total_slep) * 100
        
        # KPIs
        kpi_actual = f"{porcentaje:.1f}%"
        kpi_total = str(total_slep)
        kpi_mejorados = str(slep_mejorados)
        kpi_programa = str(slep_en_programa)
        
        # Gráfico 1: Progreso por SLEP
        sleps = [f'SLEP {i}' for i in range(1, 12)]
        estados = ['Mejorado', 'Mejorado', 'En Proceso', 'Mejorado', 'Mejorado',
                  'Mejorado', 'Mejorado', 'Sin Iniciar', 'Mejorado', 'Mejorado', 'En Proceso']
        colores = ['#06D6A0' if e == 'Mejorado' else '#F77F00' if e == 'En Proceso' else '#E63946' for e in estados]
        
        fig_slep = go.Figure(go.Bar(
            x=sleps,
            y=[1]*11,
            marker_color=colores,
            text=estados,
            textposition='inside',
            showlegend=False
        ))
        
        fig_slep.update_layout(
            title="Estado de Mejora por SLEP",
            xaxis_title="SLEP",
            yaxis_title="",
            yaxis_visible=False,
            template='plotly_white',
            height=300
        )
        
        # Gráfico 2: Áreas de competencia
        areas = [
            'Acompañamiento Pedagógico',
            'Gestión Curricular',
            'Evaluación Formativa',
            'Articulación con Sector Productivo',
            'Seguimiento de Egresados',
            'Innovación Pedagógica'
        ]
        porcentajes = [88.5, 85.2, 82.1, 78.5, 75.3, 71.8]
        
        fig_comp = go.Figure(go.Bar(
            x=porcentajes,
            y=areas,
            orientation='h',
            marker_color='#2E86AB',
            text=[f"{p}%" for p in porcentajes],
            textposition='outside'
        ))
        
        fig_comp.update_layout(
            title="Áreas de Competencia Mejoradas (Promedio SLEP)",
            xaxis_title="Porcentaje de Mejora (%)",
            yaxis_title="",
            template='plotly_white',
            height=400
        )
        
        return kpi_actual, kpi_total, kpi_mejorados, kpi_programa, fig_slep, fig_comp
    
    # Indicador Complementario 3: Redes de Trabajo
    @app.callback(
        [Output('mds-comp3-kpi-actual', 'children'),
         Output('mds-comp3-kpi-total', 'children'),
         Output('mds-comp3-kpi-participan', 'children'),
         Output('mds-comp3-kpi-redes', 'children'),
         Output('mds-comp3-region', 'figure'),
         Output('mds-comp3-tipos', 'figure'),
         Output('mds-comp3-frecuencia', 'figure')],
        [Input('mds-tabs', 'active_tab')]
    )
    def update_comp3_redes(active_tab):
        """Actualiza indicador de participación en redes"""
        
        if active_tab != 'tab-complementarios':
            return [no_update] * 7
        
        # Datos simulados
        total_ee = 1050
        ee_en_redes = 735  # 70%
        redes_activas = 42
        porcentaje = (ee_en_redes / total_ee) * 100
        
        # KPIs
        kpi_actual = f"{porcentaje:.0f}%"
        kpi_total = f"{total_ee:,}".replace(',', '.')
        kpi_participan = f"{ee_en_redes:,}".replace(',', '.')
        kpi_redes = str(redes_activas)
        
        # Gráfico 1: Por región
        regiones = [
            'Metropolitana', 'Biobío', 'Valparaíso', "O'Higgins", 'Maule',
            'La Araucanía', 'Antofagasta', 'Los Lagos'
        ]
        porcentajes_region = [78.5, 75.2, 72.1, 70.3, 68.5, 66.2, 64.8, 62.1]
        
        fig_region = go.Figure(go.Bar(
            x=regiones,
            y=porcentajes_region,
            marker_color='#06D6A0',
            text=[f"{p}%" for p in porcentajes_region],
            textposition='outside'
        ))
        
        fig_region.update_layout(
            title="Participación en Redes por Región (2024)",
            xaxis_title="Región",
            yaxis_title="Porcentaje (%)",
            template='plotly_white',
            xaxis_tickangle=-45
        )
        
        # Gráfico 2: Tipos de redes
        tipos_red = [
            'Especialidad',
            'Territorial',
            'Innovación Pedagógica',
            'Vinculación con Empresas',
            'Prácticas Profesionales'
        ]
        cantidad_redes = [15, 12, 8, 4, 3]
        
        fig_tipos = go.Figure(go.Pie(
            labels=tipos_red,
            values=cantidad_redes,
            hole=0.3,
            marker=dict(colors=['#2E86AB', '#06D6A0', '#F77F00', '#E63946', '#A0C4FF'])
        ))
        
        fig_tipos.update_layout(
            title="Distribución de Redes por Tipo",
            template='plotly_white'
        )
        
        # Gráfico 3: Frecuencia de actividades
        frecuencia = ['Mensual', 'Bimestral', 'Trimestral', 'Semestral', 'Anual']
        cantidad = [18, 12, 7, 3, 2]
        
        fig_freq = go.Figure(go.Bar(
            x=frecuencia,
            y=cantidad,
            marker_color='#F77F00',
            text=cantidad,
            textposition='outside'
        ))
        
        fig_freq.update_layout(
            title="Frecuencia de Reuniones de Redes",
            xaxis_title="Frecuencia",
            yaxis_title="Número de Redes",
            template='plotly_white'
        )
        
        return kpi_actual, kpi_total, kpi_participan, kpi_redes, fig_region, fig_tipos, fig_freq

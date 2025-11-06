"""
============================================================================
LAYOUTS MEJORADOS CON DATOS SIMULADOS REALES
============================================================================
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os
from src.utils.helpers import format_chilean


def load_simulated_data():
    """Carga los datos simulados generados"""
    data_dir = "data/processed"
    datasets = {}
    
    files = {
        'matricula': 'matricula_simulada.csv',
        'egresados': 'egresados_simulados.csv',
        'titulacion': 'titulacion_simulada.csv',
        'establecimientos': 'establecimientos_simulados.csv',
        'docentes': 'docentes_simulados.csv',
        'proyectos': 'proyectos_simulados.csv'
    }
    
    for name, filename in files.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            datasets[name] = pd.read_csv(filepath)
        else:
            print(f"⚠️ Archivo no encontrado: {filepath}")
            datasets[name] = pd.DataFrame()  # DataFrame vacío como fallback
    
    return datasets


def create_real_kpi_cards(dataset_name, filters=None):
    """Crea tarjetas KPI basadas en datos reales"""
    datasets = load_simulated_data()
    df = datasets.get(dataset_name, pd.DataFrame())
    
    if df.empty:
        return create_fallback_kpis(dataset_name)
    
    # Aplicar filtros si existen
    if filters:
        df = apply_filters(df, filters)
    
    cards = []
    colors = ['primary-custom', 'green', 'orange', 'purple']
    
    if dataset_name == 'matricula':
        # KPIs de matrícula
        total_matricula = df['matricula_total'].sum()
        crecimiento = calculate_growth(df, 'matricula_total', 'año')
        pct_mujeres = (df['matricula_mujeres'].sum() / total_matricula * 100) if total_matricula > 0 else 0
        tasa_retencion = df['tasa_retencion'].mean() * 100 if len(df) > 0 else 0
        
        metrics = {
            "Total Estudiantes": format_chilean(total_matricula),
            "Crecimiento Anual": f"+{crecimiento:.1f}%",
            "% Mujeres": f"{pct_mujeres:.1f}%",
            "Tasa Retención": f"{tasa_retencion:.1f}%"
        }
    
    elif dataset_name == 'egresados':
        total_egresados = df['egresados_total'].sum()
        tasa_transicion = df['tasa_transicion'].mean() * 100 if len(df) > 0 else 0
        pct_universidades = (df['a_universidades'].sum() / df['transicion_esup'].sum() * 100) if df['transicion_esup'].sum() > 0 else 0
        pct_institutos = (df['a_institutos'].sum() / df['transicion_esup'].sum() * 100) if df['transicion_esup'].sum() > 0 else 0
        
        metrics = {
            "Total Egresados": format_chilean(total_egresados),
            "Transición ESUP": f"{tasa_transicion:.1f}%",
            "A Universidades": f"{pct_universidades:.1f}%",
            "A Institutos": f"{pct_institutos:.1f}%"
        }
    
    elif dataset_name == 'titulacion':
        total_titulados = df['titulados'].sum()
        tasa_titulacion = df['tasa_titulacion'].mean() * 100 if len(df) > 0 else 0
        tiempo_promedio = df['tiempo_titulacion_meses'].mean() if len(df) > 0 else 0
        pct_oportuna = (df['titulacion_oportuna'].sum() / len(df) * 100) if len(df) > 0 else 0
        
        metrics = {
            "Titulados": format_chilean(total_titulados),
            "Tasa Titulación": f"{tasa_titulacion:.1f}%",
            "Tiempo Promedio": f"{format_chilean(tiempo_promedio, 1)} meses",
            "% Oportuna": f"{pct_oportuna:.1f}%"
        }
    
    elif dataset_name == 'establecimientos':
        total_establecimientos = df['establecimiento_id'].nunique()
        total_especialidades = df['especialidad'].nunique()
        pct_municipal = (len(df[df['dependencia'] == 'Municipal']) / len(df) * 100) if len(df) > 0 else 0
        pct_urbano = (len(df[df['zona'] == 'Urbana']) / len(df) * 100) if len(df) > 0 else 0
        
        metrics = {
            "Establecimientos": format_chilean(total_establecimientos),
            "Especialidades": format_chilean(total_especialidades),
            "% Municipal": f"{pct_municipal:.1f}%",
            "% Urbano": f"{pct_urbano:.1f}%"
        }
    
    elif dataset_name == 'docentes':
        total_docentes = len(df)
        edad_promedio = df['edad'].mean() if len(df) > 0 else 0
        pct_mujeres = (len(df[df['genero'] == 'Femenino']) / len(df) * 100) if len(df) > 0 else 0
        pct_titulo_ped = (len(df[df['titulo_pedagogico'] == True]) / len(df) * 100) if len(df) > 0 else 0
        
        metrics = {
            "Total Docentes": format_chilean(total_docentes),
            "Edad Promedio": f"{format_chilean(edad_promedio, 1)} años",
            "% Mujeres": f"{pct_mujeres:.1f}%",
            "% Título Ped.": f"{pct_titulo_ped:.1f}%"
        }
    
    elif dataset_name == 'proyectos':
        inversion_total = df['monto_asignado'].sum() / 1_000_000  # Millones
        proyectos_activos = len(df[df['estado'] == 'En ejecución'])
        pct_ejecucion = (df['monto_ejecutado'].sum() / df['monto_asignado'].sum() * 100) if df['monto_asignado'].sum() > 0 else 0
        establecimientos_beneficiados = df['establecimientos_beneficiados'].sum()
        
        metrics = {
            "Inversión": f"${format_chilean(inversion_total)}M",
            "Proyectos Activos": format_chilean(proyectos_activos),
            "% Ejecución": f"{pct_ejecucion:.1f}%",
            "Establecimientos": format_chilean(establecimientos_beneficiados)
        }
    
    else:
        return create_fallback_kpis(dataset_name)
    
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


def create_real_chart(dataset_name, chart_type="line", title="Gráfico", filters=None):
    """Crea gráficos basados en datos reales"""
    datasets = load_simulated_data()
    df = datasets.get(dataset_name, pd.DataFrame())
    
    if df.empty:
        return create_fallback_chart(title)
    
    # Aplicar filtros
    if filters:
        df = apply_filters(df, filters)
    
    # Colores de la paleta oficial (basada en app Shiny original)
    color_palette = ['#34536A', '#5A6E79', '#B35A5A', '#C2A869', '#6E5F80']
    
    try:
        if chart_type == "line" and 'año' in df.columns:
            # Gráfico de línea temporal
            if dataset_name == 'matricula':
                df_grouped = df.groupby('año')['matricula_total'].sum().reset_index()
                fig = px.line(df_grouped, x='año', y='matricula_total', 
                             title=title, color_discrete_sequence=[color_palette[0]])
            elif dataset_name == 'egresados':
                df_grouped = df.groupby('año')['tasa_transicion'].mean().reset_index()
                fig = px.line(df_grouped, x='año', y='tasa_transicion', 
                             title=title, color_discrete_sequence=[color_palette[1]])
            else:
                # Fallback genérico
                return create_fallback_chart(title)
        
        elif chart_type == "bar":
            # Gráfico de barras
            if dataset_name == 'matricula':
                df_grouped = df.groupby('especialidad')['matricula_total'].sum().head(10).reset_index()
                fig = px.bar(df_grouped, x='especialidad', y='matricula_total', 
                            title=title, color_discrete_sequence=[color_palette[0]])
                fig.update_xaxes(tickangle=45)
            elif dataset_name == 'establecimientos':
                df_grouped = df.groupby('region')['establecimiento_id'].nunique().reset_index()
                fig = px.bar(df_grouped, x='region', y='establecimiento_id', 
                            title=title, color_discrete_sequence=[color_palette[2]])
                fig.update_xaxes(tickangle=45)
            else:
                return create_fallback_chart(title)
        
        elif chart_type == "pie":
            # Gráfico circular
            if dataset_name == 'matricula':
                df_grouped = df.groupby('dependencia')['matricula_total'].sum().reset_index()
                fig = px.pie(df_grouped, values='matricula_total', names='dependencia', 
                            title=title, color_discrete_sequence=color_palette)
            elif dataset_name == 'docentes':
                df_grouped = df.groupby('genero').size().reset_index(name='count')
                fig = px.pie(df_grouped, values='count', names='genero', 
                            title=title, color_discrete_sequence=color_palette)
            else:
                return create_fallback_chart(title)
        
        else:
            return create_fallback_chart(title)
    
        # Configurar el layout del gráfico
        fig.update_layout(
            template="plotly_white",
            font=dict(size=12),
            title_font=dict(size=16),
            height=400,
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#FFFFFF',
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return dcc.Graph(figure=fig, className="mb-4")
    
    except Exception as e:
        print(f"⚠️ Error creando gráfico {chart_type} para {dataset_name}: {e}")
        return create_fallback_chart(title)


def create_real_table(dataset_name, filters=None):
    """Crea tablas basadas en datos reales"""
    datasets = load_simulated_data()
    df = datasets.get(dataset_name, pd.DataFrame())
    
    if df.empty:
        return create_fallback_table()
    
    # Aplicar filtros
    if filters:
        df = apply_filters(df, filters)
    
    # Preparar tabla según el dataset
    try:
        if dataset_name == 'matricula':
            # Tabla resumen por especialidad
            table_data = df.groupby('especialidad').agg({
                'matricula_total': 'sum',
                'matricula_hombres': 'sum',
                'matricula_mujeres': 'sum',
                'tasa_retencion': 'mean'
            }).round(2).reset_index()
            
            table_data.columns = ['Especialidad', 'Matrícula Total', 'Hombres', 'Mujeres', 'Tasa Retención']
            table_data = table_data.head(10)  # Top 10
        
        elif dataset_name == 'egresados':
            table_data = df.groupby('especialidad').agg({
                'egresados_total': 'sum',
                'tasa_transicion': 'mean',
                'a_universidades': 'sum',
                'a_institutos': 'sum'
            }).round(2).reset_index()
            
            table_data.columns = ['Especialidad', 'Egresados', 'Tasa Transición', 'A Universidades', 'A Institutos']
            table_data = table_data.head(10)
        
        elif dataset_name == 'establecimientos':
            table_data = df.groupby(['region', 'dependencia']).agg({
                'establecimiento_id': 'nunique',
                'matricula_especialidad': 'sum'
            }).reset_index()
            
            table_data.columns = ['Región', 'Dependencia', 'N° Establecimientos', 'Matrícula']
            table_data = table_data.head(15)
        
        elif dataset_name == 'docentes':
            table_data = df.groupby('especialidad').agg({
                'docente_id': 'count',
                'edad': 'mean',
                'experiencia_años': 'mean',
                'titulo_pedagogico': lambda x: (x == True).sum() / len(x) * 100
            }).round(2).reset_index()
            
            table_data.columns = ['Especialidad', 'N° Docentes', 'Edad Promedio', 'Experiencia', '% Título Ped.']
            table_data = table_data.head(10)
        
        elif dataset_name == 'proyectos':
            table_data = df.groupby(['region', 'tipo_proyecto']).agg({
                'monto_asignado': 'sum',
                'pct_ejecucion': 'mean',
                'establecimientos_beneficiados': 'sum'
            }).reset_index()
            
            table_data['monto_asignado'] = table_data['monto_asignado'] / 1_000_000  # Millones
            table_data.columns = ['Región', 'Tipo Proyecto', 'Monto (M$)', '% Ejecución', 'Establecimientos']
            table_data = table_data.head(15)
        
        else:
            return create_fallback_table()
        
        return dbc.Table.from_dataframe(
            table_data, 
            striped=True, 
            bordered=True, 
            hover=True,
            responsive=True,
            className="mb-4"
        )
    
    except Exception as e:
        print(f"⚠️ Error creando tabla para {dataset_name}: {e}")
        return create_fallback_table()


def apply_filters(df, filters):
    """Aplica filtros a un DataFrame"""
    if not filters:
        return df
    
    # Filtro por año
    if 'years' in filters and 'año' in df.columns:
        year_min, year_max = filters['years']
        df = df[df['año'].between(year_min, year_max)]
    
    # Filtro por región
    if 'region' in filters and 'region' in df.columns:
        if filters['region'] != 'Todas las regiones':
            df = df[df['region'] == filters['region']]
    
    # Filtro por especialidad
    if 'especialidad' in filters and 'especialidad' in df.columns:
        if filters['especialidad'] != 'Todas las especialidades':
            if isinstance(filters['especialidad'], list):
                df = df[df['especialidad'].isin(filters['especialidad'])]
            else:
                df = df[df['especialidad'] == filters['especialidad']]
    
    # Filtro por dependencia
    if 'dependencia' in filters and 'dependencia' in df.columns:
        if filters['dependencia'] != 'todas':
            df = df[df['dependencia'] == filters['dependencia']]
    
    # Filtro por género
    if 'genero' in filters and 'genero' in df.columns:
        if filters['genero'] != 'ambos':
            df = df[df['genero'] == filters['genero']]
    
    # Filtro por zona
    if 'zona' in filters and 'zona' in df.columns:
        if filters['zona'] != 'ambas':
            df = df[df['zona'] == filters['zona']]
    
    return df


def calculate_growth(df, value_col, year_col):
    """Calcula la tasa de crecimiento anual"""
    if len(df) < 2 or year_col not in df.columns or value_col not in df.columns:
        return 0
    
    try:
        df_yearly = df.groupby(year_col)[value_col].sum().sort_index()
        if len(df_yearly) < 2:
            return 0
        
        first_year = df_yearly.iloc[0]
        last_year = df_yearly.iloc[-1]
        years_diff = df_yearly.index[-1] - df_yearly.index[0]
        
        if first_year > 0 and years_diff > 0:
            growth = ((last_year / first_year) ** (1/years_diff) - 1) * 100
            return growth
        return 0
    except:
        return 0


def create_fallback_kpis(dataset_name):
    """Crea KPIs de fallback si no hay datos"""
    fallback_metrics = {
        "Sin datos": "N/A",
        "Disponibles": "0",
        "En el sistema": "---",
        "Para mostrar": "⚠️"
    }
    
    cards = []
    colors = ['primary-custom', 'green', 'orange', 'purple']
    
    for i, (label, value) in enumerate(fallback_metrics.items()):
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


def create_fallback_chart(title):
    """Crea un gráfico de fallback"""
    fig = go.Figure()
    fig.add_annotation(
        text="Datos no disponibles<br>Verifique la generación de datos simulados",
        xref="paper", yref="paper",
        x=0.5, y=0.5, xanchor='center', yanchor='middle',
        showarrow=False,
        font=dict(size=16, color="#666666")
    )
    fig.update_layout(
        title=title,
        template="plotly_white",
        height=400,
        showlegend=False
    )
    return dcc.Graph(figure=fig, className="mb-4")


def create_fallback_table():
    """Crea una tabla de fallback"""
    fallback_data = pd.DataFrame({
        'Estado': ['Sin datos disponibles'],
        'Descripción': ['Los datos simulados no se han generado correctamente'],
        'Acción': ['Execute: python src/data/fake_data_generator.py'],
        'Resultado': ['Datos disponibles para visualización']
    })
    
    return dbc.Table.from_dataframe(
        fallback_data, 
        striped=True, 
        bordered=True, 
        hover=True,
        responsive=True,
        className="mb-4"
    )
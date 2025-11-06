"""
============================================================================
CALLBACKS PARA MAPAS GEOGRÁFICOS
============================================================================
Maneja la interacción con los mapas de Chile (regional y comunal)
"""

from dash import Input, Output, callback
from src.layouts.mapas import (
    create_chile_map, 
    create_establecimientos_map,
    create_chile_comunas_map,
    create_establecimientos_comunas_map,
    create_tabla_resumen_matricula,
    create_tabla_resumen_establecimientos
)


@callback(
    [
        Output('mapa-matricula', 'figure'),
        Output('mapa-establecimientos', 'figure'),
        Output('mapa-num-territorios', 'children'),
        Output('mapa-label-territorios', 'children'),
        Output('tabla-resumen-matricula', 'children'),
        Output('tabla-resumen-establecimientos', 'children')
    ],
    [
        Input('mapa-granularidad', 'value')
    ]
)
def update_mapas_granularidad(granularidad):
    """
    Actualiza los mapas y tablas según la granularidad seleccionada (regional o comunal)
    
    Args:
        granularidad: 'regional' o 'comunal'
        
    Returns:
        tuple: (fig_matricula, fig_establecimientos, num_territorios, label_territorios, tabla_mat, tabla_est)
    """
    print(f"🗺️  Callback de mapas ejecutado con granularidad: {granularidad}")
    
    if granularidad == 'comunal':
        # Mapas comunales
        print("Generando mapas comunales...")
        fig_matricula = create_chile_comunas_map()
        fig_establecimientos = create_establecimientos_comunas_map()
        num_territorios = "345"
        label_territorios = "Comunas"
        print("✓ Mapas comunales generados")
    else:
        # Mapas regionales (default)
        print("Generando mapas regionales...")
        fig_matricula = create_chile_map()
        fig_establecimientos = create_establecimientos_map()
        num_territorios = "16"
        label_territorios = "Regiones"
        print("✓ Mapas regionales generados")
    
    # Generar tablas
    print("Generando tablas resumen...")
    tabla_matricula = create_tabla_resumen_matricula(granularidad)
    tabla_establecimientos = create_tabla_resumen_establecimientos(granularidad)
    print("✓ Tablas generadas")
    
    return fig_matricula, fig_establecimientos, num_territorios, label_territorios, tabla_matricula, tabla_establecimientos

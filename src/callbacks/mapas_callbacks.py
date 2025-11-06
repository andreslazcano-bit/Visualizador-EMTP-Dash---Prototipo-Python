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
    create_establecimientos_comunas_map
)


@callback(
    [
        Output('mapa-matricula', 'figure'),
        Output('mapa-establecimientos', 'figure'),
        Output('kpi-territorios', 'children'),
        Output('kpi-territorios-label', 'children')
    ],
    [
        Input('mapa-granularidad', 'value')
    ]
)
def update_mapas_granularidad(granularidad):
    """
    Actualiza los mapas según la granularidad seleccionada (regional o comunal)
    
    Args:
        granularidad: 'regional' o 'comunal'
        
    Returns:
        tuple: (fig_matricula, fig_establecimientos, num_territorios, label_territorios)
    """
    if granularidad == 'comunal':
        # Mapas comunales
        fig_matricula = create_chile_comunas_map()
        fig_establecimientos = create_establecimientos_comunas_map()
        num_territorios = "345"
        label_territorios = "Comunas"
    else:
        # Mapas regionales (default)
        fig_matricula = create_chile_map()
        fig_establecimientos = create_establecimientos_map()
        num_territorios = "16"
        label_territorios = "Regiones"
    
    return fig_matricula, fig_establecimientos, num_territorios, label_territorios

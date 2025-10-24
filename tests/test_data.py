"""
Tests para módulo de datos
"""

import pytest
import pandas as pd
from src.data.processors import DataProcessor


def test_process_matricula():
    """Test de procesamiento de matrícula"""
    # Datos de prueba
    df = pd.DataFrame({
        'rbd': ['1', '2', '3'],
        'cod_ense': [510, 520, 630],
        'gen_alu': [1, 2, 1]
    })
    
    result = DataProcessor.process_matricula(df)
    
    assert len(result) == 3
    assert 'rbd' in result.columns


def test_asignar_rft():
    """Test de asignación de RFT"""
    assert DataProcessor.asignar_rft('ARICA') == 'Norte 1'
    assert DataProcessor.asignar_rft('SANTIAGO NORTE') == 'Metropolitana Norte'
    assert DataProcessor.asignar_rft('DESCONOCIDO') == 'Sin Asignar'

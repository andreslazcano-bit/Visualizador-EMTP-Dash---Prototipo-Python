"""
============================================================================
FUNCIONES AUXILIARES
============================================================================
"""

import re
from typing import Optional, Union
import unicodedata


def format_number_chilean(
    value: Union[int, float],
    decimals: int = 0,
    thousands_sep: str = '.',
    decimal_sep: str = ','
) -> str:
    """
    Formatea un número con separadores
    
    Args:
        value: Número a formatear
        decimals: Cantidad de decimales
        thousands_sep: Separador de miles
        decimal_sep: Separador decimal
    
    Returns:
        String formateado
    """
    try:
        if decimals > 0:
            formatted = f"{value:,.{decimals}f}"
        else:
            formatted = f"{int(value):,}"
        
        # Reemplazar separadores
        formatted = formatted.replace(',', 'TEMP')
        formatted = formatted.replace('.', decimal_sep)
        formatted = formatted.replace('TEMP', thousands_sep)
        
        return formatted
    except:
        return str(value)


def format_chilean(value: Union[int, float], decimals: int = 0) -> str:
    """
    Formatea número usando convención chilena: . para miles, , para decimales
    
    Args:
        value: Número a formatear
        decimals: Cantidad de decimales (default: 0)
    
    Returns:
        String formateado según convención chilena
    """
    return format_number_chilean(value, decimals=decimals, thousands_sep='.', decimal_sep=',')


def clean_text(text: str) -> str:
    """
    Limpia y normaliza texto
    
    Args:
        text: Texto a limpiar
    
    Returns:
        Texto limpio
    """
    if not isinstance(text, str):
        return str(text)
    
    # Normalizar unicode
    text = unicodedata.normalize('NFKC', text)
    
    # Eliminar espacios extras
    text = ' '.join(text.split())
    
    # Trim
    text = text.strip()
    
    return text


def remove_accents(text: str) -> str:
    """
    Elimina acentos de un texto
    
    Args:
        text: Texto con acentos
    
    Returns:
        Texto sin acentos
    """
    if not isinstance(text, str):
        return str(text)
    
    nfkd_form = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def slugify(text: str) -> str:
    """
    Convierte texto a formato slug (URL-friendly)
    
    Args:
        text: Texto a convertir
    
    Returns:
        Slug
    """
    text = remove_accents(text.lower())
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def percentage(value: float, total: float, decimals: int = 1) -> str:
    """
    Calcula y formatea porcentaje
    
    Args:
        value: Valor
        total: Total
        decimals: Decimales
    
    Returns:
        String con porcentaje
    """
    try:
        if total == 0:
            return "0%"
        pct = (value / total) * 100
        return f"{pct:.{decimals}f}%"
    except:
        return "N/A"

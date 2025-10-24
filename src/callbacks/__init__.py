"""
Paquete de callbacks. Este archivo se deja intencionalmente mínimo.

La versión activa de la app (app_v2.py) registra callbacks específicos
importando directamente:
- src.callbacks.auth_callbacks
- src.callbacks.sidebar_callbacks
- src.callbacks.theme_callbacks

No hay registro global aquí para evitar dependencias a módulos antiguos.
"""

__all__ = []

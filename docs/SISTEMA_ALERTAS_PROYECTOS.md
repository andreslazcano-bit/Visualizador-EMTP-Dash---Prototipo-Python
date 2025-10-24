# 🚨 Sistema de Alertas para Proyectos SEEMTP

## Descripción General

Sistema automatizado de alertas y notificaciones para la gestión de proyectos SEEMTP, que monitorea fechas críticas, ejecución presupuestaria y cumplimiento de metas.

---

## 📋 Características Principales

### 1. **Alertas en la Aplicación (UI)**

#### 🔴 Panel de Alertas en Dashboard
```python
# Ubicación: Pantalla principal o sección de Proyectos
Componentes:
- Badge con número de alertas activas
- Panel desplegable con lista de alertas
- Priorización por criticidad (Alta/Media/Baja)
- Filtros por tipo de alerta
```

#### Tipos de Alertas Visuales:
- **🔴 Críticas** (Rojo): Convenios vencidos, proyectos con 0% ejecución después de 3 meses
- **🟡 Advertencia** (Amarillo): Convenios próximos a vencer (30 días), baja ejecución presupuestaria
- **🔵 Informativas** (Azul): Hitos alcanzados, recordatorios de reportes

#### Ubicaciones en la UI:
1. **Navbar Superior**: Badge con contador de alertas
2. **Sidebar**: Sección "Alertas Activas" con las 3 más críticas
3. **Pantalla de Proyectos**: Panel destacado con alertas del proyecto actual
4. **Dashboard Inicio**: Widget de alertas pendientes

---

### 2. **Sistema de Notificaciones por Email**

#### 📧 Configuración de Emails

```python
# Librerías recomendadas:
- smtplib (nativo Python)
- python-dotenv (para credenciales)
- Jinja2 (templates HTML)
- schedule o APScheduler (tareas periódicas)

# Archivo: src/utils/email_notifications.py
```

#### Plantillas de Email:

**A. Alerta de Convenio por Vencer**
```
Asunto: ⚠️ Convenio SEEMTP próximo a vencer - [Nombre Proyecto]

Estimado/a [Nombre],

El convenio del proyecto [ID_PROYECTO] está próximo a finalizar:
- Fecha de Término: [FECHA]
- Días Restantes: [DÍAS]
- Región: [REGIÓN]
- Establecimiento: [NOMBRE]
- Monto Ejecutado: [MONTO] ([PORCENTAJE]%)

Recomendaciones:
- Revisar estado de ejecución presupuestaria
- Preparar documentación de cierre
- Evaluar necesidad de extensión

[Ver detalles en el sistema]
```

**B. Alerta de Convenio Vencido**
```
Asunto: 🔴 URGENTE - Convenio SEEMTP vencido - [Nombre Proyecto]

El convenio del proyecto [ID_PROYECTO] ha finalizado:
- Fecha de Término: [FECHA]
- Días Transcurridos: [DÍAS]
- Ejecución Presupuestaria: [PORCENTAJE]%

Acciones requeridas:
- Generar informe final
- Cierre administrativo
- Rendición de cuentas
```

**C. Reporte Semanal Consolidado**
```
Asunto: 📊 Reporte Semanal - Proyectos SEEMTP [Fecha]

Resumen de la Semana:
- Proyectos Activos: [N]
- Alertas Críticas: [N]
- Proyectos por Vencer (30 días): [N]
- Ejecución Promedio: [%]

[Tabla con top 10 proyectos críticos]
```

---

### 3. **Lógica de Detección de Alertas**

```python
# Archivo: src/utils/alert_engine.py

from datetime import datetime, timedelta
import pandas as pd

class AlertEngine:
    """Motor de detección de alertas para proyectos SEEMTP"""
    
    ALERT_TYPES = {
        'CONVENIO_VENCIDO': {
            'prioridad': 'CRITICA',
            'color': '#dc3545',
            'icon': 'fas fa-exclamation-triangle'
        },
        'CONVENIO_POR_VENCER': {
            'prioridad': 'ALTA',
            'color': '#ffc107',
            'icon': 'fas fa-clock'
        },
        'BAJA_EJECUCION': {
            'prioridad': 'MEDIA',
            'color': '#fd7e14',
            'icon': 'fas fa-chart-line'
        },
        'SIN_ACTIVIDAD': {
            'prioridad': 'ALTA',
            'color': '#dc3545',
            'icon': 'fas fa-pause-circle'
        }
    }
    
    def __init__(self, df_proyectos):
        self.df = df_proyectos
        self.today = datetime.now()
    
    def detectar_convenios_vencidos(self):
        """
        Detecta proyectos con convenio vencido
        Condición: fecha_termino < fecha_actual
        """
        alertas = []
        # Lógica aquí
        return alertas
    
    def detectar_convenios_proximos_vencer(self, dias=30):
        """
        Detecta proyectos que vencen en los próximos N días
        Condición: fecha_actual <= fecha_termino <= fecha_actual + N días
        """
        alertas = []
        fecha_limite = self.today + timedelta(days=dias)
        # Lógica aquí
        return alertas
    
    def detectar_baja_ejecucion(self, umbral_meses=3, umbral_porcentaje=30):
        """
        Detecta proyectos con baja ejecución presupuestaria
        Condición: 
        - Más de N meses desde inicio
        - Ejecución < X%
        """
        alertas = []
        # Lógica aquí
        return alertas
    
    def detectar_proyectos_sin_actividad(self, dias=60):
        """
        Detecta proyectos sin movimientos recientes
        Condición: última_actualizacion > N días
        """
        alertas = []
        # Lógica aquí
        return alertas
    
    def generar_reporte_alertas(self):
        """Genera reporte consolidado de todas las alertas"""
        todas_alertas = {
            'convenios_vencidos': self.detectar_convenios_vencidos(),
            'convenios_por_vencer': self.detectar_convenios_proximos_vencer(),
            'baja_ejecucion': self.detectar_baja_ejecucion(),
            'sin_actividad': self.detectar_proyectos_sin_actividad()
        }
        return todas_alertas
```

---

### 4. **Sistema de Notificaciones Periódicas**

```python
# Archivo: src/utils/notification_scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

class NotificationScheduler:
    """Programa envío periódico de notificaciones"""
    
    def __init__(self, alert_engine, email_service):
        self.scheduler = BackgroundScheduler()
        self.alert_engine = alert_engine
        self.email_service = email_service
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """Inicia el programador de tareas"""
        
        # Alertas diarias - 8:00 AM
        self.scheduler.add_job(
            func=self.enviar_alertas_diarias,
            trigger=CronTrigger(hour=8, minute=0),
            id='alertas_diarias',
            name='Envío de alertas críticas diarias'
        )
        
        # Reporte semanal - Lunes 9:00 AM
        self.scheduler.add_job(
            func=self.enviar_reporte_semanal,
            trigger=CronTrigger(day_of_week='mon', hour=9, minute=0),
            id='reporte_semanal',
            name='Reporte semanal consolidado'
        )
        
        # Reporte mensual - Primer día del mes, 10:00 AM
        self.scheduler.add_job(
            func=self.enviar_reporte_mensual,
            trigger=CronTrigger(day=1, hour=10, minute=0),
            id='reporte_mensual',
            name='Reporte mensual de proyectos'
        )
        
        self.scheduler.start()
        self.logger.info("✅ Programador de notificaciones iniciado")
    
    def enviar_alertas_diarias(self):
        """Envía alertas críticas diarias"""
        alertas_criticas = self.alert_engine.detectar_convenios_vencidos()
        alertas_proximas = self.alert_engine.detectar_convenios_proximos_vencer(dias=7)
        
        if alertas_criticas or alertas_proximas:
            self.email_service.enviar_alerta_diaria(
                alertas_criticas, 
                alertas_proximas
            )
    
    def enviar_reporte_semanal(self):
        """Envía reporte semanal consolidado"""
        reporte = self.alert_engine.generar_reporte_alertas()
        self.email_service.enviar_reporte_semanal(reporte)
    
    def enviar_reporte_mensual(self):
        """Envía reporte mensual con estadísticas"""
        # Incluye: nuevos proyectos, finalizados, estadísticas, gráficos
        pass
    
    def stop(self):
        """Detiene el programador"""
        self.scheduler.shutdown()
        self.logger.info("🛑 Programador de notificaciones detenido")
```

---

### 5. **Componentes de UI para Alertas**

```python
# Archivo: src/components/alerts.py

import dash_bootstrap_components as dbc
from dash import html

def create_alert_badge(num_alertas):
    """Badge con contador de alertas"""
    if num_alertas == 0:
        return None
    
    return dbc.Badge(
        num_alertas,
        color="danger",
        pill=True,
        className="ms-1 position-absolute top-0 start-100 translate-middle"
    )

def create_alert_panel(alertas_list):
    """Panel desplegable con lista de alertas"""
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-bell me-2"),
            html.Strong(f"Alertas Activas ({len(alertas_list)})")
        ]),
        dbc.CardBody([
            html.Div([
                create_alert_item(alerta) for alerta in alertas_list[:10]
            ]),
            html.Hr(),
            dbc.Button(
                "Ver todas las alertas →",
                color="link",
                size="sm",
                href="/proyectos/alertas"
            )
        ])
    ])

def create_alert_item(alerta):
    """Item individual de alerta"""
    icon_class = alerta.get('icon', 'fas fa-info-circle')
    color = alerta.get('color', '#6c757d')
    
    return dbc.Alert([
        dbc.Row([
            dbc.Col([
                html.I(className=f"{icon_class} fa-2x", 
                       style={"color": color})
            ], width=1),
            dbc.Col([
                html.Strong(alerta['titulo'], className="d-block"),
                html.Small(alerta['mensaje'], className="text-muted"),
                html.Small(
                    f"Proyecto: {alerta['proyecto_id']} | {alerta['fecha']}",
                    className="d-block text-muted mt-1"
                )
            ], width=10),
            dbc.Col([
                dbc.Button(
                    html.I(className="fas fa-external-link-alt"),
                    size="sm",
                    color="primary",
                    outline=True,
                    href=f"/proyectos/{alerta['proyecto_id']}"
                )
            ], width=1)
        ])
    ], color="light", className="mb-2")

def create_alert_widget_inicio(alertas_criticas):
    """Widget de alertas para pantalla de inicio"""
    return dbc.Card([
        dbc.CardHeader([
            html.I(className="fas fa-exclamation-triangle me-2 text-danger"),
            html.Strong("Alertas Críticas")
        ]),
        dbc.CardBody([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H2(
                            len([a for a in alertas_criticas 
                                 if a['prioridad'] == 'CRITICA']),
                            className="text-danger mb-0"
                        ),
                        html.P("Críticas", className="text-muted small")
                    ], width=4),
                    dbc.Col([
                        html.H2(
                            len([a for a in alertas_criticas 
                                 if a['prioridad'] == 'ALTA']),
                            className="text-warning mb-0"
                        ),
                        html.P("Altas", className="text-muted small")
                    ], width=4),
                    dbc.Col([
                        html.H2(
                            len([a for a in alertas_criticas 
                                 if a['prioridad'] == 'MEDIA']),
                            className="text-info mb-0"
                        ),
                        html.P("Medias", className="text-muted small")
                    ], width=4)
                ])
            ]),
            html.Hr(),
            html.Div([
                html.Small(alerta['titulo'], className="d-block mb-1")
                for alerta in alertas_criticas[:3]
            ]),
            dbc.Button(
                "Ver todas →",
                color="danger",
                outline=True,
                size="sm",
                className="w-100 mt-2"
            )
        ])
    ], className="mb-3 border-danger")
```

---

### 6. **Configuración de Email**

```python
# Archivo: config/email_config.py

import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 587)),
    'email_sender': os.getenv('EMAIL_SENDER'),
    'email_password': os.getenv('EMAIL_PASSWORD'),
    
    # Destinatarios por tipo de alerta
    'destinatarios': {
        'CRITICA': [
            os.getenv('EMAIL_DIRECTOR'),
            os.getenv('EMAIL_COORDINADOR')
        ],
        'ALTA': [
            os.getenv('EMAIL_COORDINADOR'),
            os.getenv('EMAIL_ANALISTA')
        ],
        'MEDIA': [
            os.getenv('EMAIL_ANALISTA')
        ]
    },
    
    # Configuración de reportes periódicos
    'reportes': {
        'semanal': {
            'activo': True,
            'destinatarios': [
                os.getenv('EMAIL_EQUIPO_GESTION')
            ],
            'incluir_graficos': True
        },
        'mensual': {
            'activo': True,
            'destinatarios': [
                os.getenv('EMAIL_DIRECCION'),
                os.getenv('EMAIL_MINEDUC')
            ],
            'incluir_graficos': True,
            'incluir_anexos': True
        }
    }
}
```

```bash
# Archivo: .env (ejemplo)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_SENDER=alertas.seemtp@mineduc.cl
EMAIL_PASSWORD=tu_contraseña_segura

EMAIL_DIRECTOR=director@mineduc.cl
EMAIL_COORDINADOR=coordinador.emtp@mineduc.cl
EMAIL_ANALISTA=analista.proyectos@mineduc.cl
EMAIL_EQUIPO_GESTION=equipo.gestion@mineduc.cl
EMAIL_MINEDUC=seguimiento.emtp@mineduc.cl
```

---

### 7. **Integración con la Aplicación**

```python
# Archivo: app_v2.py (modificaciones)

from src.utils.alert_engine import AlertEngine
from src.utils.notification_scheduler import NotificationScheduler
from src.utils.email_service import EmailService
import atexit

# ... código existente ...

# Inicializar sistema de alertas
df_proyectos = pd.read_csv('data/processed/proyectos_simulados.csv')
alert_engine = AlertEngine(df_proyectos)
email_service = EmailService()
notification_scheduler = NotificationScheduler(alert_engine, email_service)

# Iniciar programador de notificaciones
notification_scheduler.start()

# Asegurar que se detenga al cerrar la app
atexit.register(notification_scheduler.stop)

# ... resto del código ...
```

---

### 8. **Base de Datos de Alertas (Opcional)**

Para llevar histórico de alertas enviadas:

```sql
-- Tabla para registro de alertas
CREATE TABLE alertas_proyectos (
    id SERIAL PRIMARY KEY,
    proyecto_id VARCHAR(50) NOT NULL,
    tipo_alerta VARCHAR(50) NOT NULL,
    prioridad VARCHAR(20) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    mensaje TEXT,
    fecha_deteccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_envio_email TIMESTAMP,
    destinatarios TEXT[],
    estado VARCHAR(20) DEFAULT 'ACTIVA', -- ACTIVA, RESUELTA, DESCARTADA
    fecha_resolucion TIMESTAMP,
    notas TEXT
);

-- Índices
CREATE INDEX idx_alertas_proyecto ON alertas_proyectos(proyecto_id);
CREATE INDEX idx_alertas_fecha ON alertas_proyectos(fecha_deteccion);
CREATE INDEX idx_alertas_estado ON alertas_proyectos(estado);
```

---

## 🎯 Roadmap de Implementación

### Fase 1: Alertas en UI (2-3 días)
- [ ] Crear componente de badge de alertas
- [ ] Implementar panel desplegable de alertas
- [ ] Agregar widget de alertas en dashboard
- [ ] Crear motor de detección básico

### Fase 2: Sistema de Email (3-4 días)
- [ ] Configurar servicio de email
- [ ] Crear plantillas HTML de emails
- [ ] Implementar envío de alertas críticas
- [ ] Pruebas de envío

### Fase 3: Notificaciones Periódicas (2-3 días)
- [ ] Instalar y configurar APScheduler
- [ ] Programar tareas diarias, semanales, mensuales
- [ ] Implementar reportes consolidados
- [ ] Pruebas de programación

### Fase 4: Refinamiento (2 días)
- [ ] Agregar base de datos de alertas (opcional)
- [ ] Implementar histórico de alertas
- [ ] Panel de configuración de alertas
- [ ] Documentación de usuario

---

## 📦 Dependencias Necesarias

```bash
# Agregar a requirements.txt
APScheduler==3.10.4       # Programación de tareas
python-dotenv==1.0.0      # Variables de entorno
Jinja2==3.1.2             # Templates HTML
reportlab==4.0.7          # Generación de PDFs (opcional)
pandas==2.1.1             # Ya instalado
```

---

## 🔒 Consideraciones de Seguridad

1. **Credenciales de Email**: Usar variables de entorno, nunca hardcodear
2. **Rate Limiting**: Limitar número de emails por día
3. **Validación de Destinatarios**: Lista blanca de emails permitidos
4. **Logs de Auditoría**: Registrar todos los envíos
5. **Manejo de Errores**: No exponer información sensible en logs de error

---

## 📊 Métricas y Monitoreo

Registrar:
- Número de alertas generadas por día/semana
- Número de emails enviados
- Tasa de apertura de emails (si se usa tracking)
- Tiempo promedio de resolución de alertas
- Alertas más frecuentes por tipo

---

## 🎨 Mockups de UI

```
╔══════════════════════════════════════════════════╗
║  🏠 Inicio     📊 Matrícula    [🔔 3]  👤 Admin ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  ┌─────────────────────────────────────────┐   ║
║  │ 🚨 ALERTAS CRÍTICAS                     │   ║
║  ├─────────────────────────────────────────┤   ║
║  │  5 Críticas   8 Altas   12 Medias       │   ║
║  ├─────────────────────────────────────────┤   ║
║  │ ⚠️ Convenio vencido - SEEMTP-2023-001   │   ║
║  │ ⏰ Vence en 7 días - SEEMTP-2024-045    │   ║
║  │ 📉 Baja ejecución - SEEMTP-2024-123     │   ║
║  ├─────────────────────────────────────────┤   ║
║  │         [Ver todas las alertas →]       │   ║
║  └─────────────────────────────────────────┘   ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

---

## ✅ Conclusión

Este sistema de alertas transformará el Visualizador EMTP en una herramienta proactiva de gestión, permitiendo:

- ✨ **Prevención**: Detectar problemas antes de que sean críticos
- 📧 **Comunicación**: Mantener informado al equipo automáticamente
- 📊 **Trazabilidad**: Registro completo de alertas y acciones
- ⏱️ **Eficiencia**: Reducir tiempo de monitoreo manual
- 🎯 **Foco**: Priorizar proyectos que requieren atención inmediata

**¿Listo para implementar?** Este documento servirá como guía completa para desarrollar el sistema de alertas en el futuro.

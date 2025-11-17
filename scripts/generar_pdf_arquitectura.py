#!/usr/bin/env python3
"""
Script para generar PDF con el diagrama de arquitectura del Visualizador EMTP
Usa Mermaid Ink API para generar la imagen del diagrama y ReportLab para crear el PDF
"""

import base64
import urllib.parse
import urllib.request
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import zlib

# Diagrama Mermaid (el código principal)
MERMAID_CODE = """
graph TB
    %% Definición de nodos principales
    subgraph USUARIOS["👥 USUARIOS"]
        style USUARIOS fill:#E3F2FD,stroke:#1976D2,stroke-width:3px
        U1["👤 Usuario Básico<br/><small>Solo visualización</small>"]
        U2["👔 Analista SEEMTP<br/><small>Análisis + Exportación</small>"]
        U3["⚙️ Administrador<br/><small>Gestión completa</small>"]
    end

    subgraph AUTH["🔐 AUTENTICACIÓN"]
        style AUTH fill:#FFF3E0,stroke:#F57C00,stroke-width:3px
        LOGIN["📝 Login<br/><small>Usuario + Contraseña</small>"]
        BCRYPT["🔒 bcrypt<br/><small>Hash seguro</small>"]
        JWT["🎫 JWT Token<br/><small>Expiración: 24h</small>"]
        VERIFY["✅ Verificación<br/><small>Permisos por perfil</small>"]
    end

    subgraph FRONTEND["🖥️ INTERFAZ DE USUARIO"]
        style FRONTEND fill:#E8F5E9,stroke:#388E3C,stroke-width:3px
        NAV["🧭 Sidebar<br/><small>Navegación principal</small>"]
        MAPAS["🗺️ Mapas Geográficos<br/><small>Regiones y comunas</small>"]
        DASHBOARDS["📊 Dashboards<br/><small>Datos en tiempo real</small>"]
        REPORTES["📄 Reportes<br/><small>Excel/PDF (futuro)</small>"]
    end

    subgraph BACKEND["⚙️ LÓGICA DE NEGOCIO"]
        style BACKEND fill:#FCE4EC,stroke:#C2185B,stroke-width:3px
        CALLBACKS["🔄 Callbacks Dash<br/><small>Reactividad</small>"]
        FILTERS["🔍 Filtros<br/><small>Región, Año, Indicador</small>"]
        PROCESS["⚡ Procesamiento<br/><small>Agregación + Cálculos</small>"]
        PLOTLY["📈 Plotly Engine<br/><small>Visualizaciones</small>"]
    end

    subgraph DATA_ACTUAL["💾 DATOS ACTUALES (CSV)"]
        style DATA_ACTUAL fill:#F3E5F5,stroke:#7B1FA2,stroke-width:3px
        CSV1["📋 establecimientos.csv<br/><small>1,124 registros</small>"]
        CSV2["📋 matricula_region.csv<br/><small>144 registros</small>"]
        CSV3["📋 docentes_especialidad.csv<br/><small>960 registros</small>"]
        CSV4["📋 titulados_2023.csv<br/><small>1,124 registros</small>"]
        CSV5["📋 establecimientos_full.csv<br/><small>174,348 registros</small>"]
    end

    subgraph DATA_FUTURO["🔮 DATOS FUTUROS (Preparado)"]
        style DATA_FUTURO fill:#E0F2F1,stroke:#00796B,stroke-width:3px,stroke-dasharray: 5 5
        SQL1["💿 SQL Server - SIGE<br/><small>Sistema de matrícula</small>"]
        SQL2["💿 SQL Server - Titulados<br/><small>Base titulados</small>"]
        SQL3["💿 SQL Server - Financiero<br/><small>Presupuestos</small>"]
        SP["☁️ SharePoint MINEDUC<br/><small>Documentos Excel</small>"]
    end

    subgraph GEO["🗺️ GEODATOS"]
        style GEO fill:#FFF9C4,stroke:#F57F17,stroke-width:3px
        GEOJSON["🌎 GeoJSON Chile<br/><small>16 regiones<br/>345 comunas</small>"]
    end

    %% Flujo de autenticación
    U1 & U2 & U3 --> LOGIN
    LOGIN --> BCRYPT
    BCRYPT --> JWT
    JWT --> VERIFY
    VERIFY --> NAV

    %% Flujo de navegación
    NAV --> MAPAS
    NAV --> DASHBOARDS
    NAV --> REPORTES

    %% Flujo de datos a callbacks
    MAPAS & DASHBOARDS --> CALLBACKS
    CALLBACKS --> FILTERS
    FILTERS --> PROCESS

    %% Datos actuales
    CSV1 & CSV2 & CSV3 & CSV4 & CSV5 --> PROCESS
    GEOJSON --> PROCESS

    %% Datos futuros (líneas punteadas)
    SQL1 & SQL2 & SQL3 & SP -.->|"No conectado"| PROCESS

    %% Procesamiento a visualización
    PROCESS --> PLOTLY
    PLOTLY --> MAPAS
    PLOTLY --> DASHBOARDS

    %% Ciclo de retroalimentación
    MAPAS --> |"Interacción usuario"| CALLBACKS
    DASHBOARDS --> |"Filtros dinámicos"| CALLBACKS

    %% Estilos de nodos
    classDef userStyle fill:#4A90E2,stroke:#2E5C8A,color:#fff,stroke-width:2px
    classDef authStyle fill:#FFB84D,stroke:#CC8A3D,color:#000,stroke-width:2px
    classDef frontStyle fill:#50C878,stroke:#2E7D52,color:#fff,stroke-width:2px
    classDef backStyle fill:#E85D75,stroke:#B84A5F,color:#fff,stroke-width:2px
    classDef dataStyle fill:#9B59B6,stroke:#6C3E7E,color:#fff,stroke-width:2px
    classDef futureStyle fill:#34D1BF,stroke:#00796B,color:#000,stroke-width:2px,stroke-dasharray: 5 5
    classDef geoStyle fill:#FFD54F,stroke:#F57F17,color:#000,stroke-width:2px

    class U1,U2,U3 userStyle
    class LOGIN,BCRYPT,JWT,VERIFY authStyle
    class NAV,MAPAS,DASHBOARDS,REPORTES frontStyle
    class CALLBACKS,FILTERS,PROCESS,PLOTLY backStyle
    class CSV1,CSV2,CSV3,CSV4,CSV5 dataStyle
    class SQL1,SQL2,SQL3,SP futureStyle
    class GEOJSON geoStyle
"""

def generate_mermaid_image_url(mermaid_code):
    """
    Genera URL de Mermaid.ink para renderizar el diagrama
    """
    # Codificar el código Mermaid
    encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
    
    # URL de la API de Mermaid.ink
    url = f"https://mermaid.ink/img/{encoded}"
    
    return url

def download_image(url):
    """
    Descarga la imagen desde la URL
    """
    print(f"Descargando diagrama desde Mermaid.ink...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            image_data = response.read()
            return BytesIO(image_data)
    except Exception as e:
        print(f"Error al descargar imagen: {e}")
        return None

def create_pdf():
    """
    Crea el PDF con el diagrama de arquitectura
    """
    pdf_filename = "docs/Arquitectura_Vision_General.pdf"
    
    # Configurar página en modo landscape para el diagrama
    page_width, page_height = landscape(A4)
    
    # Crear el PDF
    c = canvas.Canvas(pdf_filename, pagesize=landscape(A4))
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Página 1: Título y contexto
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_width/2, page_height - 60, "Visualizador EMTP - Dash")
    
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_width/2, page_height - 90, "Arquitectura General del Sistema")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_width/2, page_height - 120, "Visión Completa de Componentes y Flujos")
    
    # Línea separadora
    c.setStrokeColor(colors.HexColor("#1976D2"))
    c.setLineWidth(2)
    c.line(100, page_height - 140, page_width - 100, page_height - 140)
    
    # Información del proyecto
    y_position = page_height - 180
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Proyecto:")
    c.setFont("Helvetica", 11)
    c.drawString(200, y_position, "Visualizador de Datos EMTP (Educación Media Técnico-Profesional)")
    
    y_position -= 25
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Versión:")
    c.setFont("Helvetica", 11)
    c.drawString(200, y_position, "2.0 - Python/Dash")
    
    y_position -= 25
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Fecha:")
    c.setFont("Helvetica", 11)
    c.drawString(200, y_position, "17 de Noviembre 2025")
    
    y_position -= 25
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Desarrollador:")
    c.setFont("Helvetica", 11)
    c.drawString(200, y_position, "Andrés Lazcano - MINEDUC")
    
    y_position -= 25
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_position, "Estado:")
    c.setFont("Helvetica", 11)
    c.drawString(200, y_position, "Desarrollo/Demostración")
    
    # Resumen ejecutivo
    y_position -= 50
    c.setFont("Helvetica-Bold", 13)
    c.drawString(100, y_position, "Resumen Ejecutivo")
    
    y_position -= 25
    c.setFont("Helvetica", 10)
    description_lines = [
        "El Visualizador EMTP es una aplicación web moderna de dashboards interactivos para",
        "visualizar y analizar datos de Educación Media Técnico-Profesional en Chile.",
        "",
        "Construido con Python, Dash y Plotly, integra:",
        "  • Autenticación basada en roles (3 perfiles de usuario)",
        "  • Visualizaciones geográficas interactivas (16 regiones, 345 comunas)",
        "  • Sistema de dashboards con filtros dinámicos",
        "  • 178,700+ registros de datos simulados",
        "  • Preparación para conexión a bases de datos productivas (SQL Server, SharePoint)",
    ]
    
    for line in description_lines:
        c.drawString(100, y_position, line)
        y_position -= 18
    
    # Tecnologías principales
    y_position -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(100, y_position, "Stack Tecnológico Principal")
    
    y_position -= 25
    c.setFont("Helvetica", 10)
    tech_lines = [
        "• Python 3.12+  |  • Dash 2.14.2  |  • Plotly 5.18.0  |  • Dash Bootstrap Components 1.5.0",
        "• bcrypt 4.1.2 + PyJWT 2.8.0 (autenticación)  |  • pandas 2.2.0 (datos)",
        "• Docker + Docker Compose (contenedores)  |  • GeoJSON (mapas de Chile)",
    ]
    
    for line in tech_lines:
        c.drawString(100, y_position, line)
        y_position -= 18
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(page_width/2, 30, "Documento generado automáticamente - Visualizador EMTP Dash v2.0")
    
    c.showPage()
    
    # Página 2: Diagrama de arquitectura
    print("Generando diagrama de arquitectura...")
    
    # Generar URL del diagrama
    diagram_url = generate_mermaid_image_url(MERMAID_CODE)
    
    # Descargar imagen
    image_data = download_image(diagram_url)
    
    if image_data:
        # Título de la página
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(page_width/2, page_height - 40, "Diagrama de Arquitectura Completa")
        
        # Insertar diagrama
        try:
            img = ImageReader(image_data)
            
            # Calcular dimensiones para ajustar al ancho de la página
            img_width = page_width - 120  # Margen de 60px a cada lado
            img_height = page_height - 160  # Espacio para título y footer
            
            # Centrar la imagen
            x = (page_width - img_width) / 2
            y = 80
            
            c.drawImage(img, x, y, width=img_width, height=img_height, preserveAspectRatio=True)
            
            print("✅ Diagrama agregado correctamente")
        except Exception as e:
            print(f"⚠️ Error al insertar diagrama: {e}")
            c.setFont("Helvetica", 12)
            c.drawCentredString(page_width/2, page_height/2, 
                              "El diagrama se puede visualizar en:")
            c.drawCentredString(page_width/2, page_height/2 - 30, 
                              diagram_url)
    else:
        c.setFont("Helvetica", 12)
        c.drawCentredString(page_width/2, page_height/2, 
                          "No se pudo descargar el diagrama automáticamente.")
        c.drawCentredString(page_width/2, page_height/2 - 30, 
                          "Visualiza el diagrama en: docs/ARQUITECTURA_VISION_GENERAL.md")
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(page_width/2, 30, "Página 2 de 3 - Diagrama generado con Mermaid.js")
    
    c.showPage()
    
    # Página 3: Descripción de componentes
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_width/2, page_height - 40, "Descripción de Componentes")
    
    y_pos = page_height - 80
    
    components = [
        ("👥 USUARIOS (3 Perfiles)", [
            "• Usuario Básico: Acceso de solo lectura a dashboards y mapas",
            "• Analista SEEMTP: Análisis avanzado + exportación a Excel/PDF",
            "• Administrador: Gestión completa del sistema y usuarios"
        ]),
        ("🔐 AUTENTICACIÓN", [
            "• bcrypt: Hash seguro de contraseñas (12 rounds)",
            "• JWT: Tokens de sesión con expiración de 24 horas",
            "• Verificación: Control de permisos por perfil de usuario"
        ]),
        ("🖥️ INTERFAZ DE USUARIO", [
            "• Sidebar: Navegación lateral con menú colapsable",
            "• Mapas Geográficos: Visualizaciones coropléticas de 16 regiones y 345 comunas",
            "• Dashboards: Gráficos interactivos con filtros dinámicos",
            "• Reportes: Exportación a Excel/PDF (en desarrollo)"
        ]),
        ("⚙️ LÓGICA DE NEGOCIO", [
            "• Callbacks: Sistema reactivo de Dash para interactividad",
            "• Filtros: Por región, año, indicador, especialidad",
            "• Procesamiento: Agregaciones (SUM, AVG, COUNT) y cálculos",
            "• Plotly Engine: Motor de visualizaciones interactivas"
        ]),
        ("💾 DATOS", [
            "• Actuales: 178,824 registros en 6 archivos CSV",
            "• GeoJSON: 345 polígonos de comunas de Chile",
            "• Futuros (preparado): SQL Server (SIGE, Titulados, Financiero), SharePoint MINEDUC"
        ])
    ]
    
    c.setFont("Helvetica-Bold", 11)
    for title, items in components:
        if y_pos < 150:  # Nueva página si no hay espacio
            c.showPage()
            y_pos = page_height - 60
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(80, y_pos, title)
        y_pos -= 20
        
        c.setFont("Helvetica", 10)
        for item in items:
            c.drawString(100, y_pos, item)
            y_pos -= 18
        
        y_pos -= 15
    
    # Flujos principales
    y_pos -= 10
    c.setFont("Helvetica-Bold", 14)
    c.drawString(80, y_pos, "Flujos Principales")
    y_pos -= 25
    
    flows = [
        "1️⃣ Autenticación: Usuario → Login → bcrypt → JWT → Verificación → Dashboard",
        "2️⃣ Navegación: Dashboard → Sidebar → Mapas/Dashboards/Reportes",
        "3️⃣ Datos: CSV/GeoJSON → Procesamiento → Plotly → Visualización → Usuario → Interacción → Callbacks"
    ]
    
    c.setFont("Helvetica", 10)
    for flow in flows:
        c.drawString(100, y_pos, flow)
        y_pos -= 22
    
    # Estado del proyecto
    y_pos -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(80, y_pos, "Estado del Proyecto")
    y_pos -= 25
    
    c.setFillColor(colors.HexColor("#50C878"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_pos, "✅ COMPLETADO:")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    y_pos -= 18
    completed_items = [
        "• Arquitectura completa Python/Dash",
        "• Autenticación con 3 perfiles de usuario",
        "• Mapas interactivos de 16 regiones y 345 comunas",
        "• 178,824 registros simulados en CSV",
        "• Dockerización completa"
    ]
    for item in completed_items:
        c.drawString(110, y_pos, item)
        y_pos -= 16
    
    y_pos -= 10
    c.setFillColor(colors.HexColor("#FFB84D"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_pos, "🔄 EN DESARROLLO:")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    y_pos -= 18
    dev_items = [
        "• Conexión a SQL Server (código preparado)",
        "• Cache con Redis",
        "• Exportación a Excel/PDF"
    ]
    for item in dev_items:
        c.drawString(110, y_pos, item)
        y_pos -= 16
    
    y_pos -= 10
    c.setFillColor(colors.HexColor("#4A90E2"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(100, y_pos, "🔜 PLANIFICADO:")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    y_pos -= 18
    planned_items = [
        "• Integración SharePoint MINEDUC",
        "• Reportería automatizada",
        "• API REST para terceros"
    ]
    for item in planned_items:
        c.drawString(110, y_pos, item)
        y_pos -= 16
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(page_width/2, 30, "Página 3 de 3 - Para más información: docs/ARQUITECTURA_DETALLADA.md")
    
    # Guardar PDF
    c.save()
    print(f"\n✅ PDF generado exitosamente: {pdf_filename}")

if __name__ == "__main__":
    create_pdf()

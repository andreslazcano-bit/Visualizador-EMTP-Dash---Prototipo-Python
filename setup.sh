#!/bin/bash

# ============================================================================
# SCRIPT DE SETUP INICIAL - Visualizador EMTP Dash
# ============================================================================

set -e  # Salir si hay errores

echo "🚀 Iniciando setup de Visualizador EMTP - Dash Python"
echo "============================================================================"

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo "ℹ️  $1"
}

# ============================================================================
# 1. Verificar Python
# ============================================================================
echo ""
print_info "Verificando instalación de Python..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    echo "Por favor instala Python 3.9 o superior desde https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python encontrado: $PYTHON_VERSION"

# ============================================================================
# 2. Crear entorno virtual
# ============================================================================
echo ""
print_info "Creando entorno virtual..."

if [ -d "venv" ]; then
    print_warning "El entorno virtual ya existe. ¿Deseas recrearlo? (s/n)"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Entorno virtual recreado"
    else
        print_info "Usando entorno virtual existente"
    fi
else
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# ============================================================================
# 3. Activar entorno virtual
# ============================================================================
echo ""
print_info "Activando entorno virtual..."

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

print_success "Entorno virtual activado"

# ============================================================================
# 4. Actualizar pip
# ============================================================================
echo ""
print_info "Actualizando pip..."
python -m pip install --upgrade pip --quiet
print_success "pip actualizado"

# ============================================================================
# 5. Instalar dependencias
# ============================================================================
echo ""
print_info "Instalando dependencias (esto puede tomar varios minutos)..."

if pip install -r requirements.txt --quiet; then
    print_success "Dependencias instaladas correctamente"
else
    print_error "Error instalando dependencias"
    exit 1
fi

# ============================================================================
# 6. Configurar archivo .env
# ============================================================================
echo ""
print_info "Configurando archivo .env..."

if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success "Archivo .env creado desde .env.example"
    print_warning "IMPORTANTE: Edita .env con tus configuraciones antes de ejecutar la app"
else
    print_info "Archivo .env ya existe"
fi

# ============================================================================
# 7. Crear directorios necesarios
# ============================================================================
echo ""
print_info "Verificando estructura de directorios..."

mkdir -p data/raw data/processed data/geographic
mkdir -p reports/output reports/templates
mkdir -p logs
mkdir -p assets

print_success "Estructura de directorios verificada"

# ============================================================================
# 8. Verificar instalación de herramientas opcionales
# ============================================================================
echo ""
print_info "Verificando herramientas opcionales..."

# pyreadr para leer archivos RDS
if python -c "import pyreadr" 2>/dev/null; then
    print_success "pyreadr instalado (para archivos .rds)"
else
    print_warning "pyreadr no instalado. Si necesitas convertir archivos .rds, instala con:"
    echo "           pip install pyreadr"
fi

# Redis
if command -v redis-cli &> /dev/null; then
    print_success "Redis instalado"
else
    print_info "Redis no instalado (opcional para cache)"
fi

# ============================================================================
# 9. Test de importaciones básicas
# ============================================================================
echo ""
print_info "Verificando importaciones básicas..."

python -c "
import dash
import pandas
import plotly
import dash_bootstrap_components
print('✅ Todas las librerías principales importadas correctamente')
" || {
    print_error "Error en importaciones básicas"
    exit 1
}

# ============================================================================
# 10. Resumen
# ============================================================================
echo ""
echo "============================================================================"
print_success "SETUP COMPLETADO EXITOSAMENTE"
echo "============================================================================"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Edita el archivo .env con tus configuraciones:"
echo "   nano .env"
echo ""
echo "2. (Opcional) Convierte archivos .rds si los tienes:"
echo "   python scripts/convert_rds_to_parquet.py --all"
echo ""
echo "3. (Opcional) Prueba conexiones a bases de datos:"
echo "   python scripts/test_connections.py"
echo ""
echo "4. Ejecuta la aplicación:"
echo "   python app.py"
echo ""
echo "5. Abre tu navegador en:"
echo "   http://localhost:8050"
echo ""
echo "============================================================================"
echo ""
print_info "Para más información, revisa:"
echo "   - README.md: Visión general"
echo "   - INICIO_RAPIDO.md: Guía detallada"
echo "   - docs/MIGRACION_DATOS.md: Cómo migrar tus datos"
echo "   - docs/ROADMAP.md: Plan de desarrollo"
echo ""
print_success "¡Buena suerte con tu proyecto! 🚀"
echo ""

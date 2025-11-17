#!/bin/bash
################################################################################
# Script de Configuración de Actualización Automática Semanal
# Configura cron job para ejecutar actualización cada lunes a las 2:00 AM
################################################################################

set -e  # Salir si hay error

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  CONFIGURACIÓN DE ACTUALIZACIÓN AUTOMÁTICA SEMANAL             ║${NC}"
echo -e "${BLUE}║  Visualizador EMTP - Datos MINEDUC                             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Obtener directorio del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$PROJECT_DIR/scripts/actualizar_datos_semanal.py"

echo -e "${YELLOW}📂 Directorio del proyecto:${NC} $PROJECT_DIR"
echo -e "${YELLOW}📜 Script de actualización:${NC} $SCRIPT_PATH"
echo ""

# Verificar que existe el script
if [ ! -f "$SCRIPT_PATH" ]; then
    echo -e "${RED}❌ Error: No se encuentra el script de actualización${NC}"
    echo -e "${RED}   Ruta esperada: $SCRIPT_PATH${NC}"
    exit 1
fi

# Verificar que existe .env
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${YELLOW}⚠️  Advertencia: No se encuentra archivo .env${NC}"
    echo -e "${YELLOW}   Debes crear el archivo .env con las credenciales de MINEDUC${NC}"
    echo -e "${YELLOW}   Usa .env.example.mineduc como plantilla${NC}"
    echo ""
    read -p "¿Deseas continuar de todas formas? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 no está instalado${NC}"
    exit 1
fi

PYTHON_PATH=$(which python3)
echo -e "${GREEN}✅ Python encontrado:${NC} $PYTHON_PATH"

# Verificar dependencias
echo ""
echo -e "${BLUE}🔍 Verificando dependencias de Python...${NC}"

REQUIRED_PACKAGES=("pandas" "pyodbc" "python-dotenv")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! $PYTHON_PATH -c "import $package" 2>/dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Faltan paquetes: ${MISSING_PACKAGES[*]}${NC}"
    read -p "¿Deseas instalarlos ahora? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install "${MISSING_PACKAGES[@]}"
    else
        echo -e "${RED}❌ No se puede continuar sin las dependencias${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Todas las dependencias están instaladas${NC}"

# Crear entrada de crontab
echo ""
echo -e "${BLUE}⏰ Configurando cron job...${NC}"

CRON_COMMAND="0 2 * * 1 cd $PROJECT_DIR && $PYTHON_PATH $SCRIPT_PATH >> $PROJECT_DIR/logs/actualizacion_cron.log 2>&1"

echo -e "${YELLOW}Comando cron a agregar:${NC}"
echo -e "${GREEN}$CRON_COMMAND${NC}"
echo ""
echo -e "${YELLOW}Esto ejecutará el script:${NC}"
echo -e "  • Cada lunes a las 2:00 AM"
echo -e "  • Logs en: logs/actualizacion_cron.log"
echo ""

read -p "¿Deseas agregar este cron job? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}❌ Configuración cancelada${NC}"
    echo ""
    echo -e "${BLUE}Para configurar manualmente:${NC}"
    echo -e "  1. Ejecuta: ${GREEN}crontab -e${NC}"
    echo -e "  2. Agrega la línea:"
    echo -e "     ${GREEN}$CRON_COMMAND${NC}"
    exit 0
fi

# Agregar a crontab
(crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_COMMAND") | crontab -

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Resumen de Configuración:${NC}"
echo -e "  • Frecuencia: ${GREEN}Semanal (cada lunes)${NC}"
echo -e "  • Hora: ${GREEN}2:00 AM${NC}"
echo -e "  • Script: ${GREEN}$SCRIPT_PATH${NC}"
echo -e "  • Logs: ${GREEN}$PROJECT_DIR/logs/actualizacion_cron.log${NC}"
echo ""
echo -e "${BLUE}🔍 Ver cron jobs configurados:${NC}"
echo -e "  ${GREEN}crontab -l${NC}"
echo ""
echo -e "${BLUE}🧪 Probar actualización manualmente:${NC}"
echo -e "  ${GREEN}python3 $SCRIPT_PATH${NC}"
echo ""
echo -e "${BLUE}📊 Ver últimos logs de actualización:${NC}"
echo -e "  ${GREEN}tail -f $PROJECT_DIR/logs/actualizacion_datos.log${NC}"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE ANTES DE LA PRIMERA EJECUCIÓN:${NC}"
echo -e "  1. Configura las credenciales en ${GREEN}.env${NC}"
echo -e "  2. Verifica conectividad a SQL Server MINEDUC"
echo -e "  3. Prueba la conexión: ${GREEN}python3 scripts/test_connections.py${NC}"
echo ""

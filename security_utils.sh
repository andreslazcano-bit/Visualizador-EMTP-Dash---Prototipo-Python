#!/bin/bash
# ============================================================================
# UTILIDADES DE SEGURIDAD - VISUALIZADOR EMTP
# ============================================================================
# Script con comandos útiles para gestión de seguridad
# Uso: chmod +x security_utils.sh

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# FUNCIONES
# ============================================================================

print_header() {
    echo -e "${BLUE}"
    echo "============================================================================"
    echo "$1"
    echo "============================================================================"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ============================================================================
# 1. GENERAR SECRETS
# ============================================================================

generate_secrets() {
    print_header "GENERACIÓN DE SECRETS"
    
    echo "Generando SECRET_KEY..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo -e "${GREEN}SECRET_KEY=${SECRET_KEY}${NC}"
    echo ""
    
    echo "Generando JWT_SECRET_KEY..."
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    echo -e "${GREEN}JWT_SECRET_KEY=${JWT_SECRET}${NC}"
    echo ""
    
    print_warning "Agregar estos valores a tu archivo .env"
    print_warning "NUNCA commitear estos valores al repositorio"
}

# ============================================================================
# 2. GENERAR HASH DE CONTRASEÑA
# ============================================================================

generate_password_hash() {
    print_header "GENERACIÓN DE HASH DE CONTRASEÑA"
    
    if [ -z "$1" ]; then
        echo "Uso: ./security_utils.sh hash <contraseña>"
        print_warning "Ejemplo: ./security_utils.sh hash MiPasswordSegura123!"
        exit 1
    fi
    
    echo "Generando hash para la contraseña proporcionada..."
    python3 src/utils/auth.py "$1"
    echo ""
    print_warning "Agregar ADMIN_PASSWORD_HASH a tu archivo .env"
}

# ============================================================================
# 3. VERIFICAR CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

check_security() {
    print_header "VERIFICACIÓN DE SEGURIDAD"
    
    ERRORS=0
    WARNINGS=0
    
    # Verificar .env existe
    if [ ! -f ".env" ]; then
        print_error ".env no existe. Copiar desde .env.example"
        ERRORS=$((ERRORS + 1))
    else
        print_success ".env encontrado"
        
        # Verificar SECRET_KEY
        if grep -q "SECRET_KEY=your-secret-key-change-this-in-production" .env 2>/dev/null || \
           grep -q "SECRET_KEY=change-this-secret-key" .env 2>/dev/null; then
            print_error "SECRET_KEY sin cambiar en .env"
            ERRORS=$((ERRORS + 1))
        else
            print_success "SECRET_KEY configurado"
        fi
        
        # Verificar JWT_SECRET_KEY
        if grep -q "JWT_SECRET_KEY=jwt-secret-key" .env 2>/dev/null; then
            print_error "JWT_SECRET_KEY sin cambiar en .env"
            ERRORS=$((ERRORS + 1))
        else
            print_success "JWT_SECRET_KEY configurado"
        fi
        
        # Verificar DEBUG en producción
        if grep -q "ENVIRONMENT=production" .env 2>/dev/null; then
            if grep -q "DEBUG=True" .env 2>/dev/null; then
                print_error "DEBUG=True en producción"
                ERRORS=$((ERRORS + 1))
            else
                print_success "DEBUG=False en producción"
            fi
        fi
    fi
    
    # Verificar contraseña hardcodeada
    if grep -r "admin123" src/callbacks/ 2>/dev/null | grep -v ".pyc" | grep -q "=="; then
        print_error "Contraseña hardcodeada encontrada en código"
        ERRORS=$((ERRORS + 1))
    else
        print_success "No se encontraron contraseñas hardcodeadas"
    fi
    
    # Verificar .gitignore
    if grep -q "^.env$" .gitignore 2>/dev/null; then
        print_success ".env en .gitignore"
    else
        print_error ".env NO está en .gitignore"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Verificar permisos de .env
    if [ -f ".env" ]; then
        PERMS=$(stat -f "%A" .env 2>/dev/null || stat -c "%a" .env 2>/dev/null)
        if [ "$PERMS" == "600" ]; then
            print_success "Permisos de .env correctos (600)"
        else
            print_warning "Permisos de .env: $PERMS (recomendado: 600)"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
    
    echo ""
    echo "============================================================================"
    if [ $ERRORS -eq 0 ]; then
        print_success "Verificación completada: $ERRORS errores, $WARNINGS advertencias"
    else
        print_error "Verificación completada: $ERRORS errores, $WARNINGS advertencias"
        exit 1
    fi
}

# ============================================================================
# 4. ANÁLISIS DE SEGURIDAD CON BANDIT
# ============================================================================

run_bandit() {
    print_header "ANÁLISIS DE SEGURIDAD CON BANDIT"
    
    if ! command -v bandit &> /dev/null; then
        print_warning "Bandit no instalado. Instalando..."
        pip install bandit
    fi
    
    print_success "Ejecutando análisis de seguridad..."
    bandit -r src/ -f json -o security_report.json
    bandit -r src/ -f screen
    
    print_success "Reporte guardado en security_report.json"
}

# ============================================================================
# 5. VERIFICAR DEPENDENCIAS VULNERABLES
# ============================================================================

check_dependencies() {
    print_header "VERIFICACIÓN DE DEPENDENCIAS"
    
    if ! command -v safety &> /dev/null; then
        print_warning "Safety no instalado. Instalando..."
        pip install safety
    fi
    
    print_success "Verificando dependencias vulnerables..."
    safety check --json > dependencies_report.json || true
    safety check
    
    print_success "Reporte guardado en dependencies_report.json"
}

# ============================================================================
# 6. SETUP INICIAL DE SEGURIDAD
# ============================================================================

initial_setup() {
    print_header "CONFIGURACIÓN INICIAL DE SEGURIDAD"
    
    echo "Este script configurará los aspectos básicos de seguridad."
    echo ""
    
    # 1. Copiar .env.example
    if [ ! -f ".env" ]; then
        echo "1. Copiando .env.example a .env..."
        cp .env.example .env
        print_success ".env creado"
    else
        print_warning ".env ya existe, saltando..."
    fi
    
    # 2. Generar secrets
    echo ""
    echo "2. Generando secrets..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    # Actualizar .env (macOS compatible)
    if [ -f ".env" ]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s|SECRET_KEY=.*|SECRET_KEY=${SECRET_KEY}|" .env
            sed -i '' "s|JWT_SECRET_KEY=.*|JWT_SECRET_KEY=${JWT_SECRET}|" .env
        else
            # Linux
            sed -i "s|SECRET_KEY=.*|SECRET_KEY=${SECRET_KEY}|" .env
            sed -i "s|JWT_SECRET_KEY=.*|JWT_SECRET_KEY=${JWT_SECRET}|" .env
        fi
        print_success "Secrets generados y guardados en .env"
    fi
    
    # 3. Configurar permisos
    echo ""
    echo "3. Configurando permisos de .env..."
    chmod 600 .env
    print_success "Permisos configurados (600)"
    
    # 4. Verificar .gitignore
    echo ""
    echo "4. Verificando .gitignore..."
    if ! grep -q "^.env$" .gitignore 2>/dev/null; then
        echo ".env" >> .gitignore
        print_success ".env agregado a .gitignore"
    else
        print_success ".env ya está en .gitignore"
    fi
    
    echo ""
    print_header "CONFIGURACIÓN COMPLETADA"
    print_success "Secrets generados y guardados"
    print_warning "SIGUIENTE PASO: Generar contraseña admin"
    echo ""
    echo "Ejecuta: ./security_utils.sh hash TuPasswordSegura123!"
    echo "Luego agrega el hash a .env como ADMIN_PASSWORD_HASH"
}

# ============================================================================
# 7. TEST DE RATE LIMITER
# ============================================================================

test_rate_limiter() {
    print_header "TEST DE RATE LIMITER"
    
    print_success "Ejecutando test de rate limiter..."
    python3 src/utils/rate_limiter.py
}

# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================

show_menu() {
    print_header "UTILIDADES DE SEGURIDAD - VISUALIZADOR EMTP"
    
    echo "Comandos disponibles:"
    echo ""
    echo "  ./security_utils.sh setup          - Configuración inicial completa"
    echo "  ./security_utils.sh secrets        - Generar SECRET_KEY y JWT_SECRET_KEY"
    echo "  ./security_utils.sh hash <pass>    - Generar hash de contraseña"
    echo "  ./security_utils.sh check          - Verificar configuración de seguridad"
    echo "  ./security_utils.sh bandit         - Análisis de código con Bandit"
    echo "  ./security_utils.sh deps           - Verificar dependencias vulnerables"
    echo "  ./security_utils.sh test           - Test de rate limiter"
    echo "  ./security_utils.sh all            - Ejecutar todas las verificaciones"
    echo ""
    echo "Ejemplos:"
    echo "  ./security_utils.sh setup"
    echo "  ./security_utils.sh hash MiPasswordSegura123!"
    echo "  ./security_utils.sh check"
}

# ============================================================================
# EJECUCIÓN
# ============================================================================

case "${1:-}" in
    setup)
        initial_setup
        ;;
    secrets)
        generate_secrets
        ;;
    hash)
        generate_password_hash "$2"
        ;;
    check)
        check_security
        ;;
    bandit)
        run_bandit
        ;;
    deps)
        check_dependencies
        ;;
    test)
        test_rate_limiter
        ;;
    all)
        check_security
        echo ""
        run_bandit
        echo ""
        check_dependencies
        ;;
    *)
        show_menu
        ;;
esac

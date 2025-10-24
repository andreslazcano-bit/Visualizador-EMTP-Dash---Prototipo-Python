@echo off
REM ============================================================================
REM SCRIPT DE SETUP INICIAL - Visualizador EMTP Dash (Windows)
REM ============================================================================

echo ============================================================================
echo   SETUP VISUALIZADOR EMTP - DASH PYTHON
echo ============================================================================
echo.

REM ============================================================================
REM 1. Verificar Python
REM ============================================================================
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python 3.9 o superior desde https://www.python.org/
    pause
    exit /b 1
)

python --version
echo OK: Python encontrado
echo.

REM ============================================================================
REM 2. Crear entorno virtual
REM ============================================================================
echo Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe
    set /p recreate="Deseas recrearlo? (s/n): "
    if /i "%recreate%"=="s" (
        rmdir /s /q venv
        python -m venv venv
        echo OK: Entorno virtual recreado
    ) else (
        echo Usando entorno virtual existente
    )
) else (
    python -m venv venv
    echo OK: Entorno virtual creado
)
echo.

REM ============================================================================
REM 3. Activar entorno virtual
REM ============================================================================
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo OK: Entorno virtual activado
echo.

REM ============================================================================
REM 4. Actualizar pip
REM ============================================================================
echo Actualizando pip...
python -m pip install --upgrade pip --quiet
echo OK: pip actualizado
echo.

REM ============================================================================
REM 5. Instalar dependencias
REM ============================================================================
echo Instalando dependencias (puede tomar varios minutos)...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Fallo instalacion de dependencias
    pause
    exit /b 1
)
echo OK: Dependencias instaladas
echo.

REM ============================================================================
REM 6. Configurar .env
REM ============================================================================
echo Configurando archivo .env...
if not exist .env (
    copy .env.example .env
    echo OK: Archivo .env creado
    echo IMPORTANTE: Edita .env con tus configuraciones
) else (
    echo .env ya existe
)
echo.

REM ============================================================================
REM 7. Crear directorios
REM ============================================================================
echo Creando directorios necesarios...
mkdir data\raw 2>nul
mkdir data\processed 2>nul
mkdir data\geographic 2>nul
mkdir reports\output 2>nul
mkdir reports\templates 2>nul
mkdir logs 2>nul
mkdir assets 2>nul
echo OK: Estructura de directorios verificada
echo.

REM ============================================================================
REM Resumen
REM ============================================================================
echo.
echo ============================================================================
echo   SETUP COMPLETADO EXITOSAMENTE
echo ============================================================================
echo.
echo Proximos pasos:
echo.
echo 1. Edita .env con tus configuraciones
echo 2. (Opcional) Convierte archivos .rds:
echo    python scripts\convert_rds_to_parquet.py --all
echo 3. (Opcional) Prueba conexiones:
echo    python scripts\test_connections.py
echo 4. Ejecuta la aplicacion:
echo    python app.py
echo 5. Abre: http://localhost:8050
echo.
echo Para mas informacion revisa:
echo - README.md
echo - INICIO_RAPIDO.md
echo - docs\MIGRACION_DATOS.md
echo.
echo ============================================================================
echo.
pause

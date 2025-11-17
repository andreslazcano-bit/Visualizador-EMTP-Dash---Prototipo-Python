# Guía de Contribución

¡Gracias por tu interés en contribuir al Visualizador EMTP! Este documento te guiará en el proceso de contribución al proyecto.

## Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Guía de Estilo](#guía-de-estilo)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Pruebas](#pruebas)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)

## Código de Conducta

Este proyecto y todos los participantes están gobernados por nuestro Código de Conducta. Al participar, se espera que respetes este código. Por favor reporta comportamientos inaceptables.

### Nuestros Compromisos

- Usar lenguaje acogedor e inclusivo
- Respetar diferentes puntos de vista y experiencias
- Aceptar críticas constructivas con gracia
- Enfocarse en lo que es mejor para la comunidad
- Mostrar empatía hacia otros miembros de la comunidad

## Cómo Contribuir

### 1. Fork del Repositorio

```bash
# Haz fork del repositorio en GitHub, luego:
git clone https://github.com/TU-USUARIO/VisualizadorEMTP-Dash.git
cd VisualizadorEMTP-Dash
```

### 2. Crea una Rama

```bash
# Crea una rama para tu contribución
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

**Nomenclatura de Ramas:**
- `feature/nombre-descriptivo` - Para nuevas funcionalidades
- `fix/nombre-descriptivo` - Para correcciones de bugs
- `docs/nombre-descriptivo` - Para mejoras en documentación
- `refactor/nombre-descriptivo` - Para refactorización de código
- `test/nombre-descriptivo` - Para añadir o mejorar tests

### 3. Configura el Entorno de Desarrollo

```bash
# Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instala dependencias de desarrollo
pip install -r requirements-dev.txt
```

### 4. Realiza tus Cambios

- Escribe código limpio y bien documentado
- Sigue la [Guía de Estilo](#guía-de-estilo)
- Añade tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 5. Ejecuta las Pruebas

```bash
# Ejecuta todos los tests
pytest

# Con cobertura
pytest --cov=src tests/

# Tests específicos
pytest tests/test_data.py
```

### 6. Commit de tus Cambios

```bash
# Añade los archivos modificados
git add .

# Commit con mensaje descriptivo
git commit -m "feat: añade filtro por región en módulo de matrícula"
```

**Formato de Commits (Conventional Commits):**
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bug
- `docs:` - Cambios en documentación
- `style:` - Cambios de formato (no afectan lógica)
- `refactor:` - Refactorización de código
- `test:` - Añadir o modificar tests
- `chore:` - Tareas de mantenimiento

**Ejemplo de Buenos Commits:**
```
feat: añade exportación a PDF en reportes de egresados
fix: corrige cálculo de tasa de titulación en dashboard
docs: actualiza instrucciones de instalación en README
refactor: optimiza consultas SQL en módulo de matrícula
test: añade tests unitarios para filtros avanzados
```

### 7. Push a tu Fork

```bash
git push origin feature/nueva-funcionalidad
```

### 8. Crea un Pull Request

1. Ve a GitHub y navega a tu fork
2. Haz clic en "New Pull Request"
3. Selecciona tu rama y proporciona:
   - **Título descriptivo**
   - **Descripción detallada** de los cambios
   - **Capturas de pantalla** si aplica
   - **Referencias a issues** relacionados

**Template de Pull Request:**
```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de Cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo se ha probado?
Describe las pruebas realizadas.

## Checklist
- [ ] Mi código sigue la guía de estilo del proyecto
- [ ] He realizado una auto-revisión de mi código
- [ ] He comentado mi código en áreas difíciles de entender
- [ ] He actualizado la documentación correspondiente
- [ ] Mis cambios no generan nuevas advertencias
- [ ] He añadido tests que prueban que mi corrección es efectiva o que mi funcionalidad funciona
- [ ] Los tests unitarios pasan localmente con mis cambios
```

## 💻 Proceso de Desarrollo

### Configuración Local

1. **Instala las dependencias:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Configura variables de entorno:**
   ```bash
   cp .env.example .env
   # Edita .env con tus configuraciones locales
   ```

3. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

4. **Accede a la aplicación:**
   - URL: http://localhost:8051
   - Usuario: `usuario` (sin contraseña)
   - Admin: `admin` / `admin123`

### Flujo de Trabajo

1. **Sincroniza con el repositorio principal:**
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. **Desarrolla en tu rama local**

3. **Ejecuta tests antes de commit:**
   ```bash
   pytest
   flake8 src/
   black src/ --check
   ```

4. **Commit y push**

5. **Crea Pull Request**

## Guía de Estilo

### Python

Seguimos [PEP 8](https://pep8.org/) con algunas adaptaciones:

**Formato:**
```python
# Usa black para formateo automático
black src/

# Verifica con flake8
flake8 src/
```

**Nomenclatura:**
- `snake_case` para funciones y variables
- `PascalCase` para clases
- `UPPER_CASE` para constantes
- Nombres descriptivos en español o inglés (consistente)

**Ejemplo:**
```python
# Bueno
def calcular_tasa_titulacion(df_egresados, df_titulados):
    """
    Calcula la tasa de titulación por cohorte.
    
    Args:
        df_egresados (pd.DataFrame): DataFrame con egresados
        df_titulados (pd.DataFrame): DataFrame con titulados
        
    Returns:
        pd.DataFrame: Tasa de titulación por año
    """
    tasa = (len(df_titulados) / len(df_egresados)) * 100
    return round(tasa, 2)

# Malo
def calc(d1, d2):
    r = (len(d2) / len(d1)) * 100
    return r
```

**Importaciones:**
```python
# Orden de importaciones:
# 1. Librerías estándar
import os
import sys
from datetime import datetime

# 2. Librerías de terceros
import pandas as pd
import plotly.express as px
from dash import html, dcc

# 3. Módulos locales
from config.settings import SETTINGS
from src.utils.helpers import format_number
```

### Dash/React Components

**Nomenclatura de IDs:**
- Usa kebab-case: `'filtro-region'`, `'grafico-matricula'`
- Prefijos por módulo: `'mat-grafico-tendencia'`, `'doc-tabla-contratos'`

**Estructura de Layouts:**
```python
def create_layout():
    """Crea el layout del módulo."""
    return html.Div([
        # Header
        html.H1("Título del Módulo", className="mb-4"),
        
        # Filtros
        create_filters(),
        
        # Contenido principal
        html.Div([
            create_chart(),
            create_table()
        ], className="row"),
    ], className="container-fluid")
```

### SQL y Datos

**Consultas SQL:**
```python
# Bueno - Legible y mantenible
query = """
    SELECT 
        r.nombre_region,
        COUNT(m.id) as total_matricula,
        AVG(m.promedio) as promedio_notas
    FROM matricula m
    INNER JOIN regiones r ON m.id_region = r.id
    WHERE m.ano_lectivo = ?
    GROUP BY r.nombre_region
    ORDER BY total_matricula DESC
"""

# Malo - Difícil de leer
query = "SELECT r.nombre_region, COUNT(m.id) as total_matricula, AVG(m.promedio) as promedio_notas FROM matricula m INNER JOIN regiones r ON m.id_region = r.id WHERE m.ano_lectivo = ? GROUP BY r.nombre_region ORDER BY total_matricula DESC"
```

### Documentación

**Docstrings:**
```python
def procesar_datos_matricula(df, filtros=None):
    """
    Procesa y filtra los datos de matrícula según criterios especificados.
    
    Esta función aplica filtros múltiples a los datos de matrícula y calcula
    estadísticas agregadas por región y especialidad.
    
    Args:
        df (pd.DataFrame): DataFrame con datos de matrícula. Debe contener
            las columnas: 'ano_lectivo', 'region', 'especialidad', 'matricula'
        filtros (dict, optional): Diccionario con filtros a aplicar. Keys:
            - 'anos': List[int] - Años lectivos a incluir
            - 'regiones': List[str] - Regiones a filtrar
            - 'especialidades': List[str] - Especialidades a incluir
            
    Returns:
        pd.DataFrame: DataFrame procesado con columnas agregadas:
            - 'total_matricula': int
            - 'promedio_regional': float
            - 'variacion_anual': float (porcentaje)
            
    Raises:
        ValueError: Si el DataFrame está vacío o faltan columnas requeridas
        TypeError: Si los filtros no son del tipo esperado
        
    Examples:
        >>> filtros = {'anos': [2023, 2024], 'regiones': ['Metropolitana']}
        >>> df_procesado = procesar_datos_matricula(df_raw, filtros)
        >>> print(df_procesado.head())
        
    Note:
        Los datos de matrícula deben estar previamente validados con
        `validators.validate_matricula_data()` antes de usar esta función.
    """
    # Implementación...
```

## 📁 Estructura del Proyecto

Familiarízate con la estructura:

```
VisualizadorEMTP-Dash/
├── src/
│   ├── callbacks/       # Callbacks de Dash por módulo
│   ├── components/      # Componentes reutilizables (gráficos, tablas)
│   ├── data/           # Cargadores, procesadores, validadores
│   ├── layouts/        # Layouts de páginas
│   └── utils/          # Utilidades (auth, exports, helpers)
├── config/             # Configuración (settings, database)
├── data/               # Datos (raw, processed, geographic)
├── tests/              # Tests unitarios e integración
└── docs/               # Documentación completa
```

**Convenciones:**
- Un archivo por módulo/funcionalidad
- Nombres descriptivos en español
- Separación clara de responsabilidades

## Pruebas

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con verbose
pytest -v

# Solo un módulo
pytest tests/test_data.py

# Con cobertura
pytest --cov=src --cov-report=html
```

### Escribir Tests

```python
import pytest
import pandas as pd
from src.data.processors import procesar_datos_matricula

class TestProcesadorMatricula:
    """Tests para el procesador de datos de matrícula."""
    
    @pytest.fixture
    def df_matricula_mock(self):
        """Fixture con datos de prueba."""
        return pd.DataFrame({
            'ano_lectivo': [2023, 2023, 2024],
            'region': ['RM', 'RM', 'Valparaíso'],
            'matricula': [100, 150, 200]
        })
    
    def test_procesar_sin_filtros(self, df_matricula_mock):
        """Debe procesar todos los datos sin filtros."""
        resultado = procesar_datos_matricula(df_matricula_mock)
        assert len(resultado) == 3
        assert 'total_matricula' in resultado.columns
    
    def test_procesar_con_filtro_ano(self, df_matricula_mock):
        """Debe filtrar correctamente por año."""
        filtros = {'anos': [2023]}
        resultado = procesar_datos_matricula(df_matricula_mock, filtros)
        assert len(resultado) == 2
        assert all(resultado['ano_lectivo'] == 2023)
    
    def test_error_dataframe_vacio(self):
        """Debe lanzar ValueError con DataFrame vacío."""
        df_vacio = pd.DataFrame()
        with pytest.raises(ValueError, match="DataFrame vacío"):
            procesar_datos_matricula(df_vacio)
```

**Cobertura Mínima:**
- Funciones críticas: 90%
- Procesadores de datos: 85%
- Callbacks: 70%
- Utilidades: 80%

## Reportar Bugs

### Antes de Reportar

1. **Verifica que sea un bug nuevo** - Busca en [Issues](https://github.com/USER/VisualizadorEMTP-Dash/issues)
2. **Reproduce el bug** - Asegúrate de poder reproducirlo consistentemente
3. **Recopila información** - Logs, screenshots, configuración

### Cómo Reportar

Crea un [nuevo issue](https://github.com/USER/VisualizadorEMTP-Dash/issues/new) con:

**Template de Bug Report:**
```markdown
## Descripción del Bug
Descripción clara y concisa del problema.

## Para Reproducir
Pasos para reproducir:
1. Ir a '...'
2. Hacer clic en '...'
3. Scroll hasta '...'
4. Ver error

## Comportamiento Esperado
Qué esperabas que sucediera.

## Screenshots
Si aplica, añade capturas de pantalla.

## Entorno
- OS: [e.g. Windows 11, macOS 14]
- Python: [e.g. 3.12.0]
- Dash: [e.g. 2.14.2]
- Navegador: [e.g. Chrome 120]

## Logs
```
Pega los logs relevantes aquí
```

## Contexto Adicional
Cualquier otra información relevante.
```

## Sugerir Mejoras

### Template de Feature Request

```markdown
## ¿Tu solicitud está relacionada con un problema?
Descripción clara del problema. Ej: "Siempre me frustra cuando [...]"

## Describe la solución que te gustaría
Descripción clara y concisa de lo que quieres que suceda.

## Describe alternativas que has considerado
Otras soluciones o características que has considerado.

## Contexto Adicional
Capturas de pantalla, mockups, ejemplos de otras aplicaciones.

## Beneficios
- ¿A quién beneficiaría esta funcionalidad?
- ¿Qué problema resuelve?
- ¿Qué valor añade al proyecto?
```

##  Contacto y Ayuda

- **Issues:** [GitHub Issues](https://github.com/USER/VisualizadorEMTP-Dash/issues)
- **Discussions:** [GitHub Discussions](https://github.com/USER/VisualizadorEMTP-Dash/discussions)
- **Email:** ext.andres.lazcano@mineduc.com

---

**Última actualización:** Noviembre 2025  
**Versión:** 2.0.0

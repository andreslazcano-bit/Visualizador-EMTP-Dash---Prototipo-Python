# ============================================================================
# VISUALIZADOR EMTP - Aplicación Shiny Optimizada
# ============================================================================
# OPTIMIZACIONES IMPLEMENTADAS (15 Oct 2025):
# - Eliminada duplicación de matricula_raw (ahorro: ~151 MB)
# - Join selectivo con base_apoyo (solo columnas necesarias) (ahorro: ~150-180 MB)
# - Reutilización de datos en memoria vs recargar archivos (ahorro: ~151 MB)
# - Consolidación de mutate() y pipelines (ahorro: ~20-30 MB)
# - Limpieza estratégica con gc() (ahorro: ~40-50 MB)
# REDUCCIÓN TOTAL DE MEMORIA: ~65-70% (de 430-450 MB a 130-170 MB)
# ============================================================================

library(shiny)
library(shinyjs)  # Para show/hide de botones de login
library(bcrypt)   # Para hash seguro de contraseñas 🔒
# library(shinymanager)  # No se usa en este enfoque (login opcional manual)
library(leaflet)
library(dplyr)
library(sf)
library(colorspace)
library(stringr)
library(tidyr)
library(zip)
library(purrr)
library(rmarkdown)
library(plotly)
library(DT)
library(shinythemes)
library(openxlsx) # Agregar openxlsx a las librerías

# --- Configuración de usuarios 🔒 SEGURIDAD MEJORADA
# Hash bcrypt de contraseñas (NO almacenar en texto plano)
# Para generar nuevo hash: bcrypt::hashpw("tu_contraseña")
credentials <- data.frame(
  user = c("admin"),
  password_hash = c("$2a$12$LeZY20qZp73qRwCeFdeHPeSSUpmKKOf2QSgYSeWMbd3dGFpdbw8B."),
  admin = c(TRUE),
  stringsAsFactors = FALSE
)

# Sistema de seguridad
security_log <- data.frame(
  timestamp = character(),
  username = character(),
  action = character(),
  success = logical(),
  ip = character(),
  stringsAsFactors = FALSE
)


# --- Carga de datos iniciales (OPTIMIZADO: carga directa sin duplicación)
matricula_raw <- readRDS("data/processed/20240913_Matricula_unica_2024_TP.rds") %>%
  # Limpieza y selección de columnas relevantes en un solo paso
  select(rbd, nom_rbd, nom_reg_rbd_a, cod_com_rbd, nom_com_rbd, nom_deprov_rbd, cod_pro_rbd,
         cod_depe2, rural_rbd, cod_ense, cod_ense2, cod_grado, gen_alu, 
         cod_etnia_alu, emb_alu, int_alu, cod_int_alu, cod_nac_alu, pais_origen_alu,
         nom_espe, cod_men, rft, categoria_asis_anual) %>%
  # Asegura que rbd sea character
  mutate(rbd = as.character(rbd))

# --- Carga de base_apoyo (OPTIMIZADO: versión completa para minutas y versión slim para join)
base_apoyo_completo <- readRDS("data/processed/Base maestra_TP_2024-2025.rds")

# Crear versión slim solo con columnas necesarias para el join con matrícula
base_apoyo_slim <- base_apoyo_completo %>%
  select(
    rbd, cod_depe2, nombre_sost, RuralidadRBD,
    EquipamientoRegular_TOTAL, EquipamientoRegular_2020,
    EquipamientoRegular_2021, EquipamientoRegular_2022,
    EquipamientoRegular_2023, EquipamientoRegular_2024,
    EquipamientoRegular_Adjudica,
    EquipamientoSLEP_2023, EquipamientoSLEP_2024, EquipamientoSLEP_TOTAL
  ) %>%
  mutate(
    rbd = as.character(rbd),
    nombre_sost = as.character(nombre_sost),
    nombre_sost = trimws(toupper(nombre_sost)),
    cod_depe2 = trimws(toupper(cod_depe2)),
    RuralidadRBD = trimws(RuralidadRBD),
    EquipamientoRegular_TOTAL = suppressWarnings(as.numeric(EquipamientoRegular_TOTAL)),
    EquipamientoSLEP_TOTAL = suppressWarnings(as.numeric(EquipamientoSLEP_TOTAL))
  )

# Mantener base_apoyo completo para uso en minutas (convertir rbd a character para consistencia)
base_apoyo <- base_apoyo_completo %>%
  mutate(
    rbd = as.character(rbd),
    nombre_sost = as.character(nombre_sost),
    nombre_sost = trimws(toupper(nombre_sost)),
    cod_depe2 = trimws(toupper(cod_depe2)),
    RuralidadRBD = trimws(RuralidadRBD),
    EquipamientoRegular_TOTAL = suppressWarnings(as.numeric(EquipamientoRegular_TOTAL)),
    EquipamientoSLEP_TOTAL = suppressWarnings(as.numeric(EquipamientoSLEP_TOTAL))
  )

# Join de ambas bases (ahora con versión optimizada)
matricula_raw <- matricula_raw %>%
  left_join(base_apoyo_slim, by = c("rbd", "cod_depe2"))

# Limpiar objeto intermedio
rm(base_apoyo_slim, base_apoyo_completo)
gc(verbose = FALSE)

# --- Procesamiento consolidado de matrícula (OPTIMIZADO: todo en un solo pipeline)
matricula_raw <- matricula_raw %>%
  mutate(
    cod_ense = as.numeric(as.character(cod_ense)),
    nombre_sost = as.character(nombre_sost),
    cod_grado = as.numeric(as.character(cod_grado)),
    gen_alu = as.numeric(as.character(gen_alu))
  ) %>%
  filter(cod_ense >= 410 & cod_ense <= 863)

# Limpiar memoria después de transformación pesada
gc(verbose = FALSE)

# --- Carga y procesamiento de docentes (OPTIMIZADO: consolidado)
docentes_raw <- readRDS("data/processed/20250723_Docentes_2025_20250630_PUBL.rds") %>%
  mutate(
    rbd = as.character(rbd),
    COD_ENS_1 = as.numeric(as.character(COD_ENS_1)),
    COD_ENS_2 = as.numeric(as.character(COD_ENS_2)),
    # Clasificación población en el mismo mutate
    tiene_joven = (!is.na(COD_ENS_1) & COD_ENS_1 %% 100 == 10) | (!is.na(COD_ENS_2) & COD_ENS_2 %% 100 == 10),
    tiene_adulto = (!is.na(COD_ENS_1) & COD_ENS_1 %% 100 == 63) | (!is.na(COD_ENS_2) & COD_ENS_2 %% 100 == 63),
    Poblacion = case_when(
      tiene_joven & tiene_adulto ~ "Ambas",
      tiene_joven ~ "Jóvenes",
      tiene_adulto ~ "Adultos",
      TRUE ~ NA_character_
    )
  ) %>%
  filter(
    (COD_ENS_1 >= 410 & COD_ENS_1 <= 863) |
      (COD_ENS_2 >= 410 & COD_ENS_2 <= 863)
  ) %>%
  select(-tiene_joven, -tiene_adulto)

# Limpiar memoria
gc(verbose = FALSE)

# --- Diccionario de especialidades (SUBSECTOR códigos > 40000) ---
dic_especialidades <- tribble(
  ~codigo, ~nombre,
  41001, "Administración",
  41002, "Contabilidad",
  41003, "Secretariado",
  41004, "Ventas",
  51001, "Edificación",
  51002, "Terminaciones de Construcción",
  51003, "Montaje Industrial",
  51004, "Obras Viales y de Infraestructura",
  51005, "Instalaciones sanitarias",
  51006, "Refrigeración y climatización",
  52008, "Mecánica industrial",
  52009, "Construcciones metálicas",
  52010, "Mecánica",
  52011, "Matricería",
  52012, "Mecánica de mantención de aeronaves",
  53014, "Electricidad",
  53015, "Electrónica",
  53016, "Telecomunicaciones",
  54018, "Explotación minera",
  54019, "Metalurgia extractiva",
  54020, "Asistencia en geología",
  55022, "Gráfica",
  55023, "Dibujo técnico",
  56025, "Operación de planta química",
  56026, "Laboratorio químico",
  57028, "Tejido",
  57029, "Textil",
  57030, "Vestuario y confección textil",
  57031, "Productos del cuero",
  58033, "Conectividad y Redes",
  58034, "Programación",
  58035, "Telecomunicaciones (Redes)",
  61001, "Elaboración industrial de alimentos",
  61002, "Servicio de alimentación colectiva",
  62004, "Atención de párvulos",
  62005, "Atención de adultos mayores",
  62006, "Atención de enfermos",
  62007, "Atención social y recreativa",
  63009, "Servicio de Turismo",
  63010, "Servicio de Hotelería",
  71001, "Forestal",
  71002, "Procesamiento de la madera",
  71003, "Productos de la madera",
  71004, "Celulosa y papel",
  72006, "Agropecuaria",
  81001, "Naves mercantes y especiales",
  81002, "Pesquería",
  81003, "Acuicultura",
  81004, "Operación portuaria",
  91001, "Otro Formación Diferenciada" # Será filtrado fuera por rango
) %>% mutate(codigo = as.integer(codigo)) %>%
  dplyr::filter(codigo >= 40000, codigo <= 81004)

# --- Flujo nuevo Docentes: preparar estructura larga basada en ID_ICH y SUBSECTOR ---
if(!"ID_ICH" %in% names(docentes_raw)){
  docentes_raw <- docentes_raw %>% mutate(ID_ICH = dplyr::coalesce(COD_ENS_1, COD_ENS_2))
}
docentes_raw <- docentes_raw %>% mutate(ID_ICH = as.numeric(ID_ICH))

# Normalizar nombres críticos: RBD puede venir en minúscula
if(!"RBD" %in% names(docentes_raw) && "rbd" %in% names(docentes_raw)){
  docentes_raw <- docentes_raw %>% mutate(RBD = rbd)
}
# Asegurar existencia de SUBSECTOR1 / SUBSECTOR2 (si no vienen en la base)
if(!"SUBSECTOR1" %in% names(docentes_raw)) docentes_raw$SUBSECTOR1 <- NA_integer_
if(!"SUBSECTOR2" %in% names(docentes_raw)) docentes_raw$SUBSECTOR2 <- NA_integer_

# Normalizar posibles nombres de dependencia/ruralidad
if("cod_depe2" %in% names(docentes_raw) && !"COD_DEPE2" %in% names(docentes_raw)) docentes_raw <- docentes_raw %>% mutate(COD_DEPE2 = as.numeric(cod_depe2))
if("rural_rbd" %in% names(docentes_raw) && !"RURAL_RBD" %in% names(docentes_raw)) docentes_raw <- docentes_raw %>% mutate(RURAL_RBD = as.numeric(rural_rbd))

# 1. Filtrar por ID_ICH (410–863)
docentes_idich <- docentes_raw %>% filter(!is.na(ID_ICH), ID_ICH >= 410, ID_ICH <= 863)

# 2. Clasificar población Jóvenes/Adultos
docentes_idich <- docentes_idich %>% mutate(
  Poblacion = case_when(
    ID_ICH %% 100 == 10 ~ "Jóvenes",
    ID_ICH %% 100 == 63 ~ "Adultos",
    TRUE ~ NA_character_
  )
)

# 3. Normalizar SUBSECTOR (evitar duplicados triviales)
docentes_idich <- docentes_idich %>% mutate(
  SUBSECTOR1 = dplyr::na_if(SUBSECTOR1, 0),
  SUBSECTOR2 = dplyr::na_if(SUBSECTOR2, 0),
  SUBSECTOR2 = ifelse(!is.na(SUBSECTOR1) & SUBSECTOR2 == SUBSECTOR1, NA, SUBSECTOR2)
)

# 4. Formato largo de especialidades válidas
docentes_especialidad_long <- docentes_idich %>%
  tidyr::pivot_longer(cols = c(SUBSECTOR1,SUBSECTOR2), names_to='col_sub', values_to='SUBSECTOR') %>%
  filter(!is.na(SUBSECTOR), SUBSECTOR >= 40000, SUBSECTOR <= 81004) %>%
  distinct(MRUN, RBD, SUBSECTOR, .keep_all = TRUE) %>%
  left_join(dic_especialidades, by=c('SUBSECTOR'='codigo')) %>%
  mutate(Especialidad = ifelse(is.na(nombre), as.character(SUBSECTOR), nombre))

# Choices para selector (reemplaza choices_especialidades si se desea simplificar)
choices_especialidades_doc <- sort(unique(docentes_especialidad_long$SUBSECTOR))
choices_especialidades_doc <- {
  tmp <- docentes_especialidad_long %>% dplyr::distinct(SUBSECTOR, Especialidad) %>% dplyr::arrange(SUBSECTOR)
  stats::setNames(tmp$SUBSECTOR, paste(tmp$SUBSECTOR, tmp$Especialidad))
}

# Silenciar avisos de bindings no visibles en dplyr
utils::globalVariables(c('SUBSECTOR1','SUBSECTOR2','SUBSECTOR','RBD','MRUN','DOC_GENERO','NOM_REG_RBD_A','NOM_COM_RBD','Especialidad','nombre','Poblacion','HORAS','TITULO',
                         'COD_DEPE2','RURAL_RBD','Dependencia_label','Ruralidad_label'))

codigos_presentes <- sort(unique(
  docentes_raw$SUBSECTOR1[docentes_raw$SUBSECTOR1 %in% dic_especialidades$codigo]
))
choices_especialidades <- setNames(codigos_presentes,
                                   paste(codigos_presentes,
                                         dic_especialidades$nombre[match(codigos_presentes, dic_especialidades$codigo)],
                                         sep = " - "))

# Distribución de docentes por RBD y sexo
# Docentes del RBD seleccionado (directo desde la base de docentes)

# --- OPTIMIZADO: Reutilizar matricula_raw en vez de recargar archivo
matricula_comunas <- matricula_raw %>%
  mutate(cod_com_rbd = as.character(cod_com_rbd)) %>%
  select(cod_com_rbd, nom_reg_rbd_a, nombre_sost, cod_pro_rbd, nom_deprov_rbd, nom_com_rbd, nom_espe, cod_depe2) %>%
  distinct() %>%
  rename(cod_comuna = cod_com_rbd)

comunas <- readRDS("data/geographic/comunas_simplificado.rds")

# --- Asegurar tipo de dato consistente
matricula_raw <- matricula_raw %>%
  mutate(cod_com_rbd = as.character(cod_com_rbd))

# --- Join de comunas
comunas <- comunas %>%
  mutate(cod_comuna = as.character(cod_comuna)) %>%
  left_join(matricula_comunas, by = "cod_comuna")

# Limpiar objeto intermedio
rm(matricula_comunas)
gc(verbose = FALSE)

asignar_rft <- function(deprov) {
  case_when(
    deprov %in% c("ARICA", "IQUIQUE") ~ "Norte 1",
    deprov %in% c("ANTOFAGASTA - TOCOPILLA", "EL LOA", "COPIAPÓ", "HUASCO") ~ "Norte 2",
    deprov %in% c("ELQUI", "LIMARÍ", "CHOAPA", "QUILLOTA", "SAN FELIPE", "VALPARAÍSO", "SAN ANTONIO") ~ "Centro Norte",
    deprov %in% c("SANTIAGO CENTRO", "SANTIAGO NORTE", "SANTIAGO PONIENTE", "SANTIAGO ORIENTE") ~ "Metropolitana Norte",
    deprov %in% c("CORDILLERA", "SANTIAGO SUR", "TALAGANTE") ~ "Metropolitana Sur",
    deprov %in% c("CACHAPOAL", "COLCHAGUA", "CARDENAL CARO", "CURICÓ", "TALCA", "LINARES", "CAUQUENES") ~ "Centro Sur",
    deprov %in% c("ÑUBLE", "BIOBÍO", "CONCEPCIÓN", "ARAUCO") ~ "Sur 1",
    deprov %in% c("MALLECO", "CAUTÍN NORTE", "CAUTÍN SUR", "VALDIVIA", "RANCO") ~ "Sur 2",
    deprov %in% c("OSORNO", "LLANQUIHUE", "CHILOÉ", "COYHAIQUE", "MAGALLANES") ~ "Sur 3",
    FALSE ~ "Sin Asignar"
  )
}

matricula_raw <- matricula_raw %>%
  mutate(rft = asignar_rft(nom_deprov_rbd))

comunas <- comunas %>%
  mutate(rft = asignar_rft(nom_deprov_rbd))

# --- Matrículas
matricula_por_comuna <- matricula_raw %>%
  filter(gen_alu %in% c(1, 2)) %>%
  group_by(cod_com_rbd) %>%
  summarise(matricula = n(), .groups = "drop") %>%
  rename(cod_comuna = cod_com_rbd)

matricula_por_comuna_genero <- matricula_raw %>%
  filter(gen_alu %in% c(1, 2)) %>%
  group_by(cod_com_rbd, gen_alu) %>%
  summarise(matricula = n(), .groups = "drop") %>%
  rename(cod_comuna = cod_com_rbd)

# Agregar información sobre número de establecimientos por comuna
establecimientos_por_comuna <- matricula_raw %>%
  group_by(cod_com_rbd) %>%
  summarise(n_establecimientos = n_distinct(rbd), .groups = "drop") %>%
  rename(cod_comuna = cod_com_rbd)

matricula_genero_wide <- matricula_por_comuna_genero %>%
  tidyr::pivot_wider(
    names_from = gen_alu,
    values_from = matricula,
    values_fill = list(matricula = 0)
  ) %>%
  rename_with(~ c("matricula_hombres", "matricula_mujeres"), .cols = c(`1`, `2`))

comunas <- comunas %>%
  left_join(matricula_por_comuna, by = "cod_comuna") %>%
  left_join(matricula_genero_wide, by = "cod_comuna") %>%
  left_join(establecimientos_por_comuna, by = "cod_comuna")

# --- Normalización y colores
comunas$Region <- str_trim(comunas$Region)
comunas$Region <- ifelse(comunas$Region == "Región del Libertador Bernardo O'Higgins",
                         "Región del Libertador General Bernardo O'Higgins",
                         ifelse(comunas$Region == "Región de Magallanes y Antártica Chilena",
                                "Región de Magallanes y de la Antártica Chilena",
                                ifelse(comunas$Region == "Región del Bío-Bío",
                                       "Región del Biobío",
                                       ifelse(comunas$Region == "Región de Aysén del Gral.Ibañez del Campo",
                                              "Región de Aysén del General Carlos Ibáñez del Campo",
                                              comunas$Region))))

orden_norte_a_sur <- c(
  "Región de Arica y Parinacota",
  "Región de Tarapacá",
  "Región de Antofagasta",
  "Región de Atacama",
  "Región de Coquimbo",
  "Región de Valparaíso",
  "Región Metropolitana de Santiago",
  "Región del Libertador General Bernardo O'Higgins",
  "Región del Maule",
  "Región de Ñuble",
  "Región del Biobío",
  "Región de La Araucanía",
  "Región de Los Ríos",
  "Región de Los Lagos",
  "Región de Aysén del General Carlos Ibáñez del Campo",
  "Región de Magallanes y de la Antártica Chilena"
)

regiones_presentes <- intersect(orden_norte_a_sur, unique(comunas$Region))
num_regiones <- length(regiones_presentes)
colores_originales <- qualitative_hcl(num_regiones, palette = "Dark 3")
mitad <- ceiling(num_regiones / 2)
indices_reordenados <- as.vector(rbind(1:mitad, (mitad + 1):num_regiones))
indices_reordenados <- indices_reordenados[!is.na(indices_reordenados)]
colores_reordenados <- colores_originales[indices_reordenados]
colores_regiones <- setNames(colores_reordenados, regiones_presentes)
comunas$fill_color_base <- colores_regiones[comunas$Region]

mat_min <- min(comunas$matricula, na.rm = TRUE)
mat_max <- max(comunas$matricula, na.rm = TRUE)
opacidad_min <- 0.3
opacidad_max <- 1
comunas$fill_opacity <- (comunas$matricula - mat_min) / (mat_max - mat_min)
comunas$fill_opacity <- opacidad_min + comunas$fill_opacity * (opacidad_max - opacidad_min)
comunas$fill_opacity[is.na(comunas$fill_opacity)] <- opacidad_min
comunas$fill_opacity <- pmin(pmax(comunas$fill_opacity, opacidad_min), opacidad_max)

comunas$fill_color_final <- ifelse(
  is.na(comunas$matricula) | comunas$matricula == 0,
  "#BBBBBB",
  comunas$fill_color_base
)

# ---- Tema Global Plotly ----
# Tema global Plotly
plotly_theme <- list(
  font = list(family = "Roboto", size = 14, color = "#2C3E50"),
  title = list(font = list(size = 18, color = "#2C3E50")),
  paper_bgcolor = "white",
  plot_bgcolor = "white",
  margin = list(l = 50, r = 50, t = 50, b = 50),
  xaxis = list(showgrid = TRUE, gridcolor = "#ECF0F1", zeroline = FALSE, linecolor = "#BDC3C7"),
  yaxis = list(showgrid = TRUE, gridcolor = "#ECF0F1", zeroline = FALSE, linecolor = "#BDC3C7"),
  legend = list(bgcolor = "rgba(0,0,0,0)", bordercolor = "rgba(0,0,0,0)", font = list(size = 13)),
  # Paleta sobria unificada
  colorway = c("#34536A", "#5A6E79", "#B35A5A", "#C2A869", "#6E5F80")
)

# Función para aplicar tema
apply_plotly_theme <- function(p) {
  p <- layout(p,
              font = plotly_theme$font,
              title = plotly_theme$title,
              paper_bgcolor = plotly_theme$paper_bgcolor,
              plot_bgcolor = plotly_theme$plot_bgcolor,
              margin = plotly_theme$margin,
              xaxis = plotly_theme$xaxis,
              yaxis = plotly_theme$yaxis,
              legend = plotly_theme$legend,
              colorway = plotly_theme$colorway)
  return(p)
}

# --- UI Shiny
# --- UI (acceso público con login opcional)
ui <- fluidPage(
  useShinyjs(),  # Necesario para show/hide
  
  # Pantalla de carga (se muestra mientras cargan los datos)
  div(id = "loading-screen",
      style = "position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
               background: linear-gradient(135deg, #34536A, #2A4255); 
               z-index: 9999; display: flex; align-items: center; justify-content: center;
               flex-direction: column;",
      tags$div(
        style = "text-align: center; color: white;",
        tags$div(
          class = "spinner",
          style = "border: 8px solid rgba(255,255,255,0.2);
                   border-top: 8px solid white;
                   border-radius: 50%;
                   width: 80px;
                   height: 80px;
                   animation: spin 1s linear infinite;
                   margin: 0 auto 30px auto;"
        ),
        tags$h2("Cargando Explorador de Datos EMTP", 
                style = "font-family: 'Roboto', sans-serif; font-weight: 300; margin-bottom: 10px;"),
        tags$p("Preparando datos 2024-2025...", 
               style = "font-size: 16px; opacity: 0.9;"),
        tags$style(HTML("
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        "))
      )
  ),
  
  # Contenido principal (oculto inicialmente)
  shinyjs::hidden(
    div(id = "main-content",
        navbarPage(
          title = "Explorador de Datos EMTP 2024-2025",
          id = "navbar",
          theme = shinytheme("flatly"),
          windowTitle = "Explorador EMTP",
          collapsible = TRUE,
          
          header = tagList(
            tags$head(
              # Tipografía Roboto
              tags$link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap"),
              # Font Awesome para iconos
              tags$link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"),
              
              # Script para mover botones a la navbar
              tags$script(HTML("
                $(document).ready(function() {
                  // Esperar que la navbar se renderice
                  setTimeout(function() {
                    var loginContainer = $('#login-container');
                    var navbar = $('.navbar-right, .navbar-nav').last();
                    
                    if(navbar.length > 0) {
                      // Mover el contenedor de login a la navbar
                      loginContainer.css({
                        'position': 'static',
                        'display': 'inline-block',
                        'float': 'right',
                        'margin-top': '8px',
                        'margin-right': '15px'
                      });
                      navbar.parent().append(loginContainer);
                    }
                  }, 500);
                });
              ")),
              
              tags$style(HTML("
    :root { --color-bg:#F4F6F7; --color-text:#2C3E50; --color-primary:#34536A; --color-primary-dark:#2A4255; --color-accent-green:#5A6E79; --color-accent-red:#B35A5A; --color-accent-yellow:#C2A869; --color-accent-purple:#6E5F80; --color-border-light:#ECF0F1; --color-panel-border:#BDC3C7; --color-muted:#7F8C8D; --color-neutral:#FAFAFA; }
    body { font-family:'Roboto',sans-serif; background:var(--color-bg); color:var(--color-text); }
    h1,h2,h3,h4,h5 { color:var(--color-text); font-weight:700; }
    .well { background:var(--color-neutral); border:none; border-radius:10px; box-shadow:0 2px 4px rgba(0,0,0,.08); transition:box-shadow .3s; }
    .well:hover { box-shadow:0 4px 8px rgba(0,0,0,.12); }
    .btn-primary { background:var(--color-primary); border:none; font-weight:600; border-radius:6px; transition:all .25s; }
    .btn-primary:hover { background:var(--color-primary-dark); transform:translateY(-1px); }
    .btn-success { background:var(--color-accent-red); border:none; }
    .btn-success:hover { background:#9E4848; }
    .btn-secondary { background:var(--color-text); border:none; color:#fff; }
    .btn-secondary:hover { background:#1b2730; }
    .navbar { background:var(--color-primary)!important; box-shadow:0 2px 4px rgba(0,0,0,.1); }
    .navbar-default .navbar-nav>li>a, .navbar-brand { color:#ECF0F1!important; }
    .navbar-default .navbar-nav>li>a:hover { color:var(--color-accent-red)!important; }
    
    /* Botones de login en navbar */
    .login-btn {
      background: transparent;
      color: #ECF0F1 !important;
      border: 1px solid #ECF0F1;
      padding: 6px 12px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.3s;
      font-size: 13px;
      margin-left: 8px;
    }
    .login-btn:hover {
      background: #ECF0F1;
      color: var(--color-primary) !important;
    }
    #user_info {
      color: #ECF0F1;
      margin-right: 10px;
      font-size: 13px;
      vertical-align: middle;
    }
    
    .info-card { background:linear-gradient(135deg,var(--color-primary),var(--color-accent-red)); color:#fff; padding:20px; border-radius:10px; margin-bottom:20px; box-shadow:0 4px 6px rgba(0,0,0,.12); }
    .metric-card { background:#fff; padding:15px; border-radius:8px; text-align:center; box-shadow:0 2px 4px rgba(0,0,0,.08); border-left:4px solid var(--color-primary); }
    .metric-number { font-size:2em; font-weight:700; color:var(--color-text); }
    .metric-label { font-size:.85em; color:var(--color-muted); }
    .loading-spinner { border:4px solid #f3f3f3; border-top:4px solid var(--color-primary); border-radius:50%; width:40px; height:40px; animation:spin 2s linear infinite; margin:20px auto; }
    @keyframes spin { 0%{transform:rotate(0deg);} 100%{transform:rotate(360deg);} }
    .update-box { border-left:5px solid var(--color-primary); padding:15px; background:var(--color-neutral); border-radius:6px; margin-bottom:20px; }
  .alert-info { background:#EEF3F5; border:1px solid #D3DBDF; color:#2C3E50; padding:15px; border-radius:6px; margin-bottom:20px; }
  .hero-title { color: var(--color-neutral); letter-spacing:.5px; text-shadow:0 1px 2px rgba(0,0,0,.35); }
  .hero-sub { opacity:.92; }
    table.dataTable thead th { background:var(--color-primary); color:#fff; }
    table.dataTable tbody tr.selected { background:rgba(52,83,106,0.15); }
  #descargar_minuta.btn, #descargar_minuta.shiny-download-link { opacity:1!important; pointer-events:auto!important; cursor:pointer!important; filter:none!important; }
  #descargar_minuta.btn.disabled, #descargar_minuta.shiny-download-link.disabled { background:var(--color-primary)!important; color:#fff!important; opacity:1!important; }
  #descargar_minuta_pdf.btn, #descargar_minuta_pdf.shiny-download-link { opacity:1!important; pointer-events:auto!important; cursor:pointer!important; filter:none!important; }
  #descargar_minuta_pdf.btn.disabled, #descargar_minuta_pdf.shiny-download-link.disabled { background:var(--color-primary)!important; color:#fff!important; opacity:1!important; }
  "))
            ),
            # Contenedor de botones de login (será movido por JavaScript)
            tags$div(id = "login-container",
                     # Botón login (visible por defecto)
                     actionButton("show_login_modal", 
                                  label = tagList(icon("user"), "Login Admin"),
                                  class = "btn login-btn"),
                     # Info usuario y logout (ocultos por defecto)
                     tags$span(id = "user_info",
                               style = "display: none;",
                               textOutput("username_display", inline = TRUE)),
                     actionButton("do_logout",
                                  label = tagList(icon("sign-out-alt"), "Logout"),
                                  class = "btn login-btn",
                                  style = "display: none;")
            )
          ),
          
          # --- Pestaña Inicio ---
          tabPanel(
            title = tagList(icon("home"), "Inicio"),
            fluidPage(
              div(class = "info-card",
                  fluidRow(
                    column(8,
                           h1("Explorador de Datos EMTP 2024-2025", class="hero-title", style="margin:0;"),
                           p("Sistema integrado de visualización y análisis de datos de Educación Media Técnico Profesional",
                             class="hero-sub", style="margin:5px 0 0 0;")
                    ),
                    column(4,
                           tags$div(tags$i(class="fas fa-chart-line fa-3x", style="float:right; opacity:0.7;"))
                    )
                  )
              ),
              # Métricas principales
              fluidRow(
                column(3,
                       div(class="metric-card",
                           div(class="metric-number", textOutput("kpi_total_matricula_inicio")),
                           div(class="metric-label", "Matrícula filtrada")
                       )
                ),
                column(3,
                       div(class="metric-card",
                           div(class="metric-number", textOutput("kpi_establecimientos_inicio")),
                           div(class="metric-label", "Establecimientos")
                       )
                ),
                column(3,
                       div(class="metric-card",
                           div(class="metric-number", textOutput("kpi_hombres_inicio")),
                           div(class="metric-label", "Hombres")
                       )
                ),
                column(3,
                       div(class="metric-card",
                           div(class="metric-number", textOutput("kpi_mujeres_inicio")),
                           div(class="metric-label", "Mujeres")
                       )
                )
              ),
              
              br(),
              
              # Descripción mejorada
              wellPanel(
                h3(tags$i(class="fas fa-info-circle"), " Acerca del Sistema"),
                p("Esta aplicación permite visualizar y descargar información completa de la matrícula y otros datos de apoyo 
          de la Educación Media Técnico Profesional (EMTP) correspondientes al año 2024-2025."),
                
                tags$div(class = "alert-info",
                         tags$strong("Importante: "), 
                         "Los datos presentados corresponden a estudiantes de 3° y 4° medio asociados a una especialidad EMTP, 
                 salvo en el caso de estudiantes adultos, donde se incluyen también los del 1° Nivel (equivalente a 1° y 2° medio)."
                )
              ),
              
              # Navegación mejorada
              wellPanel(
                h3(tags$i(class="fas fa-compass"), " Navegación del Sistema"),
                fluidRow(
                  column(3,
                         tags$div(
                           style = "border-left: 4px solid var(--color-primary); padding-left: 15px;",
                           h4(tags$i(class="fas fa-map"), " Mapa de Matrícula"),
                           p("Consulta la matrícula por territorio, visualiza datos geográficos y descarga minutas territoriales detalladas.")
                         )
                  ),
                  column(3,
                         tags$div(
                           style = "border-left: 4px solid var(--color-accent-red); padding-left: 15px;",
                           h4(tags$i(class="fas fa-search"), " Buscador de Establecimientos"),
                           p("Busca establecimientos por RBD, nombre o filtros, y descarga minutas específicas por establecimiento.")
                         )
                  ),
                  column(3,
                         tags$div(
                           style = "border-left: 4px solid var(--color-primary-dark); padding-left: 15px;",
                           h4(tags$i(class="fas fa-chart-bar"), " Visualizaciones"),
                           p("Explora datos mediante gráficos interactivos, tablas dinámicas y análisis comparativos.")
                         )
                  ),
                  column(3,
                         tags$div(
                           style = "border-left: 4px solid #B35A5A; padding-left: 15px;",
                           h4(tags$i(class="fas fa-chalkboard-teacher"), " Docentes"),
                           p("Analiza información de docentes EMTP: género, dependencia, ruralidad, experiencia y distribución territorial.")
                         )
                  )
                )
              ),
              
              # --- Cuadro de actualizaciones recientes ---
              tags$div(
                class = "update-box",
                h4("Actualizaciones recientes"),
                tags$ul(
                  tags$li("19 de agosto de 2025: Se agregaron datos de Cargos Docentes 2025"),
                  tags$li("21 de agosto de 2025: Se agregaron datos de Asistencia Anual por Categoría 2024 y Tasa de Titulación al año de Egreso"),
                  tags$li("25 de agosto de 2025: Se agregó pestaña de Visualización con gráficos interactivos y tabla descargable por tipo de enseñanza, grado y especialidad"),
                  tags$li("28 de agosto de 2025: Se complementó la pestaña de Visualización con más opciones de filtro e información"),
                  tags$li("14 de octubre de 2025: Se mejoró interfaz para navegación. Se agregó pestaña de análisis docentes EMTP")
                  
                )
              ),
              
              # En la pestaña de inicio, mejorar la sección de descarga
              wellPanel(
                h3(tags$i(class="fas fa-download"), " Descarga de Bases de Datos"),
                p("Descarga las bases completas en diferentes formatos:"),
                
                fluidRow(
                  column(4,
                         tags$div(style="text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin: 5px;",
                                  tags$i(class="fas fa-users fa-2x", style="color: var(--color-primary);"),
                                  h5("Matrícula EMTP 2024"),
                                  downloadButton("descargar_matricula_csv", "Descargar (.csv)", class = "btn-primary btn-sm")
                         )
                  ),
                  column(4,
                         tags$div(style="text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin: 5px;",
                                  tags$i(class="fas fa-school fa-2x", style="color: var(--color-accent-red);"),
                                  h5("Base de Establecimientos"),
                                  downloadButton("descargar_base_apoyo_csv", "Descargar (.csv)", class = "btn-primary btn-sm")
                         )
                  ),
                  column(4,
                         tags$div(style="text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin: 5px;",
                                  tags$i(class="fas fa-chalkboard-teacher fa-2x", style="color: var(--color-primary-dark);"),
                                  h5("Docentes EMTP 2025"),
                                  downloadButton("descargar_docentes_emtp_csv", "Descargar (.csv)", class = "btn-primary btn-sm")
                         )
                  )
                )
              )
            )
          ),
          
          # --- Pestaña Mapa de Matrícula ---
          tabPanel(
            title = tagList(icon("map"), "Mapa de Matrícula"),
            fluidPage(
              div(style = "text-align: center; margin-bottom: 20px;",
                  h3(icon("map-marked-alt"), "Visualización Geográfica de la Matrícula EMTP", style = "color: #2C3E50;")
              ),
              
              # Panel de filtros y descarga
              fluidRow(
                column(12, 
                       div(class = "panel-custom",
                           h4(icon("filter"), "Filtros Territoriales y Descarga de Reportes", style = "color: #2C3E50;"),
                           fluidRow(
                             # Filtros territoriales
                             column(8,
                                    fluidRow(
                                      column(3,
                                             selectInput("rft", tagList(icon("globe"), "RFT:"), 
                                                         choices = c("Todas", sort(unique(comunas$rft))), 
                                                         selected = "Todas")
                                      ),
                                      column(3,
                                             selectInput("region", tagList(icon("map-marker-alt"), "Región:"), 
                                                         choices = c("Todas", sort(unique(comunas$nom_reg_rbd_a))), 
                                                         selected = "Todas")
                                      ),
                                      column(3,
                                             selectInput("provincia", tagList(icon("map-pin"), "DEPROV:"), 
                                                         choices = c("Todas", sort(unique(comunas$nom_deprov_rbd))), 
                                                         selected = "Todas")
                                      ),
                                      column(3,
                                             selectInput("comuna", tagList(icon("city"), "Comuna:"), 
                                                         choices = c("Todas", sort(unique(comunas$nom_com_rbd))), 
                                                         selected = "Todas")
                                      )
                                    ),
                                    fluidRow(
                                      column(4,
                                             selectizeInput(
                                               "especialidad",
                                               tagList(icon("cogs"), "Especialidad:"),
                                               choices = c("", sort(unique(comunas$nom_espe))),
                                               selected = "",
                                               multiple = TRUE,
                                               options = list(
                                                 placeholder = 'Selecciona especialidad...',
                                                 plugins = list('remove_button')
                                               )
                                             )
                                      ),
                                      column(4,
                                             selectInput("dependencia", tagList(icon("building"), "Dependencia:"), 
                                                         choices = c("Todas", sort(unique(comunas$cod_depe2))), 
                                                         selected = "Todas")
                                      ),
                                      column(4,
                                             selectInput("sostenedor_mapa", tagList(icon("users"), "Sostenedor:"), 
                                                         choices = c("Todos", sort(unique(matricula_raw$nombre_sost))), 
                                                         selected = "Todos")
                                      )
                                    ),
                                    fluidRow(
                                      column(12,
                                             div(style = "margin-top: 15px;",
                                                 actionButton("reset_filtros_mapa", tagList(icon("redo"), " Reiniciar filtros"), 
                                                              class = "btn-warning", style = "width: 100%; padding: 12px;")
                                             )
                                      )
                                    )
                             ),
                             
                             # Panel de descarga
                             column(4,
                                    div(style = "background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid var(--color-primary);",
                                        h5(icon("file-word"), "Minutas Territoriales", style = "color: #2C3E50; margin-bottom: 10px;"),
                                        p(style = "font-size: 12px; color: #666; margin-bottom: 10px;",
                                          icon("info-circle"), " Descarga reportes detallados del territorio seleccionado"),
                                        downloadButton("descargar_resumen_territorial", 
                                                       tagList(icon("download"), " Descargar minuta (.docx)"), 
                                                       class = "btn-primary", style = "width: 100%; margin-bottom: 8px;"),
                                        downloadButton("descargar_resumen_territorial_pdf", 
                                                       tagList(icon("file-pdf"), " Descargar minuta (.pdf)"), 
                                                       class = "btn-danger", style = "width: 100%; margin-bottom: 8px;"),
                                        checkboxInput("incluir", tagList(icon("list"), " Incluir lista de establecimientos"), 
                                                      value = FALSE, width = "100%")
                                    )
                             )
                           )
                       )
                )
              ),
              
              # Mapa principal
              fluidRow(
                column(12,
                       div(class = "panel-custom",
                           h4(icon("map"), "Mapa Interactivo de Matrícula", style = "color: #2C3E50;"),
                           leafletOutput("mapa_matricula", height = "650px")
                       )
                )
              ),
              
              # Tabla de resumen debajo del mapa
              fluidRow(
                column(12,
                       div(class = "panel-custom",
                           div(style = "text-align: center; margin-bottom: 15px;",
                               h4(icon("chart-bar"), "Resumen Detallado de Matrícula Filtrada", style = "color: #2C3E50;")
                           ),
                           div(style = "background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);",
                               uiOutput("resumen_matricula")
                           )
                       )
                )
              )
            )
          ),
          
          # --- Pestaña Buscador de Establecimientos ---
          tabPanel(
            title = tagList(icon("search"), "Buscador de Establecimientos"),
            fluidPage(
              div(style = "text-align: center; margin-bottom: 20px;",
                  h3(icon("search-plus"), "Búsqueda y Descarga de Minutas por Establecimiento", style = "color: #2C3E50;")
              ),
              
              # Panel de filtros y descarga
              fluidRow(
                column(12, 
                       div(class = "panel-custom",
                           h4(icon("filter"), "Filtros de Búsqueda y Descarga de Reportes", style = "color: #2C3E50;"),
                           fluidRow(
                             # Filtros de búsqueda
                             column(8,
                                    fluidRow(
                                      column(3,
                                             selectInput("rft_busqueda", tagList(icon("globe"), "RFT:"), 
                                                         choices = c("Todas", sort(unique(matricula_raw$rft))), 
                                                         selected = "Todas")
                                      ),
                                      column(3,
                                             selectInput("region_busqueda", tagList(icon("map-marker-alt"), "Región:"), 
                                                         choices = c("Todas", sort(unique(matricula_raw$nom_reg_rbd_a))), 
                                                         selected = "Todas")
                                      ),
                                      column(3,
                                             selectInput("provincia_busqueda", tagList(icon("map-pin"), "DEPROV:"), 
                                                         choices = c("Todas", sort(unique(matricula_raw$nom_deprov_rbd))), 
                                                         selected = "Todas")
                                      ),
                                      column(3,
                                             selectInput("comuna_busqueda", tagList(icon("city"), "Comuna:"), 
                                                         choices = c("Todas", sort(unique(matricula_raw$nom_com_rbd))), 
                                                         selected = "Todas")
                                      )
                                    ),
                                    fluidRow(
                                      column(4,
                                             selectInput("dependencia_busqueda", tagList(icon("building"), "Dependencia:"), 
                                                         choices = c("Todas", sort(unique(comunas$cod_depe2))), 
                                                         selected = "Todas")
                                      ),
                                      column(4,
                                             selectInput("sostenedor_busqueda", tagList(icon("users"), "Sostenedor:"), 
                                                         choices = c("Todos", sort(unique(matricula_raw$nombre_sost))), 
                                                         selected = "Todos")
                                      ),
                                      column(4,
                                             selectizeInput(
                                               "especialidad_busqueda",
                                               tagList(icon("cogs"), "Especialidad:"),
                                               choices = c("", sort(unique(matricula_raw$nom_espe))),
                                               selected = "",
                                               multiple = TRUE,
                                               options = list(
                                                 placeholder = 'Selecciona especialidad...',
                                                 plugins = list('remove_button')
                                               )
                                             )
                                      )
                                    ),
                                    fluidRow(
                                      column(6,
                                             textInput("rbd_busqueda", tagList(icon("id-card"), "Buscar por RBD (1234, 5678)"), "")
                                      ),
                                      column(6,
                                             textInput("nombre_busqueda", tagList(icon("school"), "Buscar por Nombre"), "")
                                      )
                                    ),
                                    fluidRow(
                                      column(6,
                                             div(style = "margin-top: 15px;",
                                                 actionButton("buscar", tagList(icon("search"), " Buscar Establecimientos"), 
                                                              class = "btn-success", style = "width: 100%; padding: 12px;")
                                             )
                                      ),
                                      column(6,
                                             div(style = "margin-top: 15px;",
                                                 actionButton("reset_filtros", tagList(icon("redo"), " Reiniciar filtros"), 
                                                              class = "btn-warning", style = "width: 100%; padding: 12px;")
                                             )
                                      )
                                    )
                             ),
                             
                             # Panel de descarga
                             column(4,
                                    div(style = "background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid var(--color-primary);",
                                        h5(icon("file-alt"), "Minutas por Establecimiento", style = "color: #2C3E50; margin-bottom: 10px;"),
                                        p(style = "font-size: 12px; color: #666; margin-bottom: 10px;",
                                          icon("info-circle"), " Descarga reportes detallados de establecimientos específicos"),
                                        p(style = "font-size: 11px; color: #856404; background: #fff3cd; padding: 8px; border-radius: 4px; margin-bottom: 10px;",
                                          icon("exclamation-triangle"), " Importante: Se descargará una minuta individual por cada establecimiento filtrado o buscado. No se genera un Word agregado, sino un archivo ZIP con una minuta por cada RBD seleccionado."),
                                        downloadButton("descargar_minuta", 
                                                       tagList(icon("download"), " Descargar minutas (.zip)"), 
                                                       class = "btn-primary", style = "width: 100%; margin-bottom: 8px;", disabled = TRUE),
                                        downloadButton("descargar_minuta_pdf", 
                                                       tagList(icon("file-pdf"), " Descargar minutas PDF (.zip)"), 
                                                       class = "btn-danger", style = "width: 100%; margin-bottom: 8px;", disabled = TRUE),
                                        p(style = "font-size: 11px; color: #666;",
                                          icon("file-archive"), " Archivo ZIP con documentos Word (.docx) individuales para cada establecimiento")
                                    )
                             )
                           )
                       )
                )
              ),
              
              # Tabla de resultados
              fluidRow(
                column(12,
                       div(class = "panel-custom",
                           h4(icon("table"), "Resultados de Búsqueda", style = "color: #2C3E50;"),
                           div(style = "background: #ffffff; padding: 12px 20px 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);",
                               div(style = "display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:10px;",
                                   tags$strong(icon("info-circle"), " Selección de establecimientos:"),
                                   span(style="font-size:12px; color:#555;", "Por defecto todos quedan seleccionados tras la búsqueda. Puedes deseleccionar filas o usar los botones."),
                                   actionButton("seleccionar_todos_est", label = tagList(icon("check-square"), "Seleccionar todos"), class = "btn btn-sm btn-success"),
                                   actionButton("deseleccionar_todos_est", label = tagList(icon("square"), "Quitar selección"), class = "btn btn-sm btn-secondary"),
                                   span(style="margin-left:auto; font-size:12px;", textOutput("contador_seleccion", inline = TRUE))
                               ),
                               DT::dataTableOutput("tabla_establecimientos")
                           )
                       )
                )
              )
            )
          ),
          
          # --- Pestaña Visualizaciones ---
          tabPanel(
            title = tagList(icon("chart-line"), "Visualizaciones Matrícula"),
            fluidPage(
              div(style = "text-align: center; margin-bottom: 20px;",
                  h3(icon("chart-bar"), "Exploración Visual de la Matrícula EMTP", style = "color: #2C3E50;")
              ),
              
              fluidRow(
                column(12, 
                       div(class = "panel-custom",
                           h4(icon("filter"), "Filtros Generales", style = "color: #2C3E50;"),
                           fluidRow(
                             column(3,
                                    selectizeInput(
                                      "filtro_especialidad",
                                      tagList(icon("cogs"), "Especialidad:"),
                                      choices = c("", sort(unique(matricula_raw$nom_espe))),
                                      selected = "",
                                      multiple = TRUE,
                                      options = list(
                                        placeholder = 'Selecciona especialidad...',
                                        plugins = list('remove_button')
                                      )
                                    )
                             ),
                             column(3,
                                    selectInput("nivel", tagList(icon("graduation-cap"), "Tipo de enseñanza:"), 
                                                choices = c("Ambos", "Niños y Jóvenes", "Adultos"), 
                                                selected = "Ambos")
                             ),
                             column(3,
                                    selectizeInput(
                                      "filtro_region",
                                      tagList(icon("map-marker-alt"), "Región:"),
                                      choices = c("", sort(unique(matricula_raw$nom_reg_rbd_a))),
                                      selected = "",
                                      multiple = TRUE,
                                      options = list(
                                        placeholder = 'Selecciona región...',
                                        plugins = list('remove_button')
                                      )
                                    )
                             ),
                             column(3,
                                    selectInput("filtro_dependencia", tagList(icon("building"), "Dependencia:"), 
                                                choices = c("Todas", sort(unique(matricula_raw$cod_depe2))), 
                                                selected = "Todas")
                             )
                           ),
                           fluidRow(
                             column(6, uiOutput("grado_ui")),
                             column(6, 
                                    div(style = "margin-top: 25px;",
                                        h5(icon("info-circle"), "Matrícula Total Filtrada: ", 
                                           textOutput("total_matricula_filtrada", inline = TRUE), 
                                           style = "color: #2C3E50; font-weight: bold;")
                                    )
                             )
                           ),
                           fluidRow(
                             column(12,
                                    div(style = "margin-top: 15px;",
                                        actionButton("reset_filtros_viz", tagList(icon("redo"), " Reiniciar filtros"), 
                                                     class = "btn-warning", style = "width: 100%; padding: 12px;")
                                    )
                             )
                           )
                       )
                )
              ),
              
              tabsetPanel(
                id = "viz_tabs",
                
                # Sub-pestaña: Resumen General
                tabPanel(
                  title = tagList(icon("tachometer-alt"), "Resumen General"),
                  br(),
                  
                  # Primera fila: Métricas principales
                  fluidRow(
                    column(3,
                           div(class = "metric-card", style = "padding:20px; border-left:6px solid #34536A;",
                               h5("Total Matrícula", style = "margin:0; font-size:14px; color: var(--color-muted); text-transform:uppercase; letter-spacing:.5px;"),
                               h2(textOutput("total_matricula"), style = "margin:8px 0 0 0; font-weight:700; color: var(--color-text);")
                           )),
                    column(3,
                           div(class = "metric-card", style = "padding:20px; border-left:6px solid #3B5268;",
                               h5("Hombres", style = "margin:0; font-size:14px; color: var(--color-muted); text-transform:uppercase; letter-spacing:.5px;"),
                               h2(textOutput("total_hombres"), style = "margin:8px 0 0 0; font-weight:700; color: var(--color-text);"),
                               p(textOutput("pct_hombres"), style = "margin:0; font-size:12px; color: #3B5268; font-weight:600;")
                           )),
                    column(3,
                           div(class = "metric-card", style = "padding:20px; border-left:6px solid #A75F5D;",
                               h5("Mujeres", style = "margin:0; font-size:14px; color: var(--color-muted); text-transform:uppercase; letter-spacing:.5px;"),
                               h2(textOutput("total_mujeres"), style = "margin:8px 0 0 0; font-weight:700; color: var(--color-text);"),
                               p(textOutput("pct_mujeres"), style = "margin:0; font-size:12px; color: #A75F5D; font-weight:600;")
                           )),
                    column(3,
                           div(class = "metric-card", style = "padding:20px; border-left:6px solid #6E5F80;",
                               h5("Establecimientos", style = "margin:0; font-size:14px; color: var(--color-muted); text-transform:uppercase; letter-spacing:.5px;"),
                               h2(textOutput("total_establecimientos"), style = "margin:8px 0 0 0; font-weight:700; color: var(--color-text);")
                           ))
                  ),
                  
                  # Segunda fila: Gráficos y tablas
                  fluidRow(
                    column(6,
                           div(class = "panel-custom",
                               h4(icon("chart-pie"), "Distribución por Género", style = "color: #2C3E50; margin-bottom: 15px;"),
                               plotlyOutput("grafico_torta", height = "300px")
                           )
                    ),
                    column(6,
                           div(class = "panel-custom",
                               h4(icon("building"), "Establecimientos por Dependencia", style = "color: #2C3E50; margin-bottom: 15px;"),
                               DTOutput("tabla_dependencia", height = "300px")
                           )
                    )
                  )
                ),
                
                # Sub-pestaña: Análisis por Grado
                tabPanel(
                  title = tagList(icon("layer-group"), "Análisis por Grado"),
                  br(),
                  fluidRow(
                    column(12,
                           div(class = "panel-custom",
                               h4(icon("chart-column"), "Matrícula por Nivel y Grado", style = "color: #2C3E50;"),
                               plotlyOutput("grafico_nivel_grado", height = "500px")
                           )
                    )
                  )
                ),
                
                # Sub-pestaña: Análisis por Especialidad
                tabPanel(
                  title = tagList(icon("cogs"), "Análisis por Especialidad"),
                  br(),
                  fluidRow(
                    column(12,
                           div(class = "panel-custom",
                               h4(icon("chart-bar"), "Matrícula por Especialidad (% por Género)", style = "color: #2C3E50;"),
                               plotlyOutput("grafico_barras", height = "600px")
                           )
                    )
                  )
                ),
                
                # Sub-pestaña: Tabla Detallada
                tabPanel(
                  title = tagList(icon("table"), "Tabla Detallada"),
                  br(),
                  fluidRow(
                    column(12,
                           div(class = "panel-custom",
                               h4(icon("list"), "Detalle de la Matrícula por RBD-Especialidad", style = "color: #2C3E50;"),
                               DTOutput("tabla_matricula"),
                               br(),
                               downloadButton("descargar_csv", 
                                              tagList(icon("download"), " Descargar lista filtrada"), 
                                              class = "btn-primary")
                           )
                    )
                  )
                )
              )
            )
          ),
          
          # --- Pestaña Docentes (reestructurada flujo ID_ICH -> SUBSECTOR) ---
          tabPanel(
            title = tagList(icon("chalkboard-teacher"), "Docentes"),
            fluidPage(
              div(style="text-align:center;margin-bottom:15px;",
                  h3(icon("chalkboard-teacher"), "Docentes de Especialidad (EMTP)")
              ),
              div(class="alert-info", style="margin-bottom:15px;",
                  HTML("<strong>Nota:</strong> Se muestran <em>docentes de especialidad</em> agregados por establecimiento (RBD). La unidad principal es <strong>Docente–RBD–Especialidad</strong>. Una persona puede aparecer varias veces si trabaja en más de un RBD o especialidad. Inclusión: ID_ICH 410–863 (terminación 10 = Jóvenes, 63 = Adultos); luego SUBSECTOR 40000–81004.")),
              div(class="panel-custom", style="margin-bottom:15px;",
                  h4(icon("filter"), "Filtros"),
                  fluidRow(
                    column(3, selectInput("doc_f_region", tagList(icon("map-marker-alt"), "Región"), choices = c("Todas", sort(unique(docentes_especialidad_long$NOM_REG_RBD_A))), selected="Todas")),
                    column(3, selectInput("doc_f_comuna", tagList(icon("map-pin"), "Comuna"), choices = c("Todas", sort(unique(docentes_especialidad_long$NOM_COM_RBD))), selected="Todas")),
                    column(2, selectInput("doc_f_poblacion", tagList(icon("graduation-cap"), "Enseñanza"), choices = c("Todas","Jóvenes","Adultos"), selected="Todas")),
                    column(2, selectizeInput("doc_f_especialidad", tagList(icon("cogs"), "Especialidad"), choices = choices_especialidades_doc, multiple=TRUE, options=list(placeholder='Todas',plugins=list('remove_button')))),
                    column(2, selectInput("doc_f_genero", tagList(icon("venus-mars"), "Género"), choices = c("Todos","Femenino","Masculino"), selected="Todos"))
                  ),
                  fluidRow(
                    column(3, selectInput("doc_f_dependencia", tagList(icon("building"), "Dependencia Adm."), 
                                          choices = c("Todas","Municipal","Particular Subvencionado",
                                                      "Corporación de Administración Delegada","Servicio Local de Educación Pública"),
                                          selected="Todas")),
                    column(3, selectInput("doc_f_ruralidad", tagList(icon("map"), "Ruralidad"), choices = c("Todas","Urbana","Rural"), selected="Todas"))
                  ),
                  fluidRow(
                    column(2, actionButton("doc_aplicar", tagList(icon("filter"), " Aplicar filtros"), class="btn-primary", width="100%")),
                    column(2, actionButton("doc_reset", tagList(icon("redo"), " Reiniciar filtros"), class="btn-warning", width="100%")),
                    column(3, downloadButton("doc_descarga", tagList(icon("download"), " Descargar CSV"), class="btn-primary", style="width:100%")),
                    column(3, downloadButton("doc_descarga_pdf", tagList(icon("file-pdf"), " Descargar Reporte PDF"), class="btn-danger", style="width:100%")),
                    column(2, div(style="padding-top:8px;font-size:11px;color:#555;text-align:center;", HTML("Unidad: MRUN–RBD–Especialidad")))
                  )
              ),
              tabsetPanel(
                id="doc_subtabs",
                tabPanel(tagList(icon("tachometer-alt"), "Resumen"),
                         fluidRow(
                           column(3, div(class="metric-card", h5("Registros"), h2(textOutput("kpi_registros")))),
                           column(3, div(class="metric-card", h5("Docentes únicos"), h2(textOutput("kpi_personas")), div(style="font-size:12px;", textOutput("kpi_promedio")))),
                           column(3, div(class="metric-card", h5("Mediana edad"), h2(textOutput("kpi_mediana_edad")))),
                           column(3, div(class="metric-card", h5("Prom. años servicio"), h2(textOutput("kpi_prom_servicio"))))
                         ),
                         fluidRow(
                           column(6, div(class="panel-custom", h4(icon("table"), "Resumen por Especialidad"), DTOutput("doc_tab_resumen"))),
                           column(6, div(class="panel-custom", h4(icon("chart-pie"), "% Mujeres (personas)"), h2(textOutput("kpi_mujeres")), plotlyOutput("doc_plot_genero", height="300px")))
                         )
                ),
                tabPanel(tagList(icon("venus-mars"), "Género"),
                         tabsetPanel(
                           id = "doc_genero_tabs",
                           tabPanel(
                             tagList(icon("cogs"), "Por especialidad"),
                             fluidRow(
                               column(12, div(class="panel-custom", h4(icon("chart-bar"), "Género por Especialidad (% interno)"), plotlyOutput("doc_plot_genero_especialidad", height="520px")))
                             )
                           ),
                           tabPanel(
                             tagList(icon("map-marker-alt"), "Por región"),
                             fluidRow(
                               column(12, div(class="panel-custom", h4(icon("chart-bar"), "Género por Región (% interno)"), plotlyOutput("doc_plot_genero_region", height="420px")))
                             ),
                             fluidRow(
                               column(12, div(class="panel-custom", h4(icon("chart-column"), "Cantidad de Docentes por Región"), plotlyOutput("doc_plot_cantidad_region", height="420px")))
                             )
                           )
                         )
                ),
                tabPanel(tagList(icon("building"), "Dependencia"),
                         fluidRow(
                           column(12, div(class="panel-custom", h4(icon("building"), "Distribución por Dependencia"),
                                          plotlyOutput("doc_plot_dependencia", height="420px"),
                                          DTOutput("doc_tab_dependencia")))
                         )
                ),
                tabPanel(tagList(icon("map"), "Ruralidad"),
                         fluidRow(
                           column(12, div(class="panel-custom", h4(icon("map"), "Distribución por Ruralidad"),
                                          plotlyOutput("doc_plot_ruralidad", height="420px"),
                                          div(style="font-size:11px;color:#555;", "Ruralidad según RURAL_RBD (0=Urbana,1=Rural).")))
                         )
                ),
                tabPanel(tagList(icon("graduation-cap"), "Experiencia y Carrera"),
                         fluidRow(
                           column(4, div(class="panel-custom", h4(icon("chart-column"), "Tramo Carrera Docente (personas únicas)"), plotlyOutput("doc_plot_tramo", height="440px"),
                                         div(style="font-size:11px;color:#555;", "Fuente: TRAMO_CARR_DOCENTE. Muestra distribución porcentual de docentes con tramo reportado."))),
                           column(4, div(class="panel-custom", h4(icon("chart-column"), "Distribución de Edades (personas)"), plotlyOutput("doc_plot_edad", height="440px"),
                                         div(style="font-size:11px;color:#555;", "Edad calculada desde DOC_FEC_NAC (yyyymm). Línea vertical = mediana."))),
                           column(4, div(class="panel-custom", h4(icon("chart-column"), "Años en el Sistema (personas)"), plotlyOutput("doc_plot_servicio", height="440px"),
                                         div(style="font-size:11px;color:#555;", "Años según ANO_SERVICIO_SISTEMA truncado a 0–60. Líneas: mediana (línea continua), promedio (línea punteada).")))
                         )
                ),
                tabPanel(tagList(icon("list"), "Detalle"),
                         fluidRow(
                           column(12, div(class="panel-custom", h4(icon("table"), "Detalle Registros"), DTOutput("doc_tab_detalle")))
                         )
                )
              )
            )
          ),
          
          # --- PESTAÑA POWER BI (solo visible con autenticación admin) ---
          tabPanel(
            title = tagList(icon("lock"), icon("chart-bar"), "Dashboard Power BI"),
            value = "powerbi_tab",  # ID único para esta pestaña
            fluidPage(
              # Encabezado con estilo
              div(class = "info-card",
                  fluidRow(
                    column(10,
                           h1("Distribución de Establecimientos Educacionales 2024", class="hero-title", style="margin:0;"),
                           p("Dashboard oficial del Centro de Estudios MINEDUC - Datos Abiertos",
                             class="hero-sub", style="margin:5px 0 0 0;")
                    ),
                    column(2,
                           tags$div(tags$i(class="fas fa-school fa-3x", 
                                           style="float:right; opacity:0.7;"))
                    )
                  )
              ),
              
              # Instrucciones
              div(class = "alert-info", style="margin: 20px;",
                  h4(icon("info-circle"), " Sobre este Dashboard"),
                  p(strong("Visualización oficial de datos educacionales del MINEDUC.")),
                  p("Este dashboard presenta la distribución de establecimientos educacionales en Chile para el año 2024."),
                  p(HTML("<strong>Fuente:</strong> Centro de Estudios MINEDUC - Portal de Datos Abiertos")),
                  tags$hr(),
                  p(HTML("<strong>Para integrar tu propio dashboard de Power BI:</strong>")),
                  tags$ol(
                    tags$li("Publica tu reporte en Power BI Service"),
                    tags$li("Ve a Archivo → Insertar informe → Publicar en Web"),
                    tags$li("Copia la URL generada"),
                    tags$li("Reemplaza la URL en este código")
                  ),
                  p(HTML("<em>Nota: Esta integración funciona igual en servidor web que en modo local.</em>"))
              ),
              
              # Iframe con Power BI
              fluidRow(
                column(12,
                       wellPanel(
                         style = "padding: 10px; margin-top: 20px;",
                         h4(icon("chart-line"), "Dashboard Interactivo - Establecimientos Educacionales"),
                         tags$iframe(
                           # URL de Power BI - Distribución de Establecimientos Educacionales 2024 MINEDUC
                           src = "https://app.powerbi.com/view?r=eyJrIjoiMjE5NDAyYjgtYjdhOC00OTNhLTgyODctMWIzZTRhYjBmNjgwIiwidCI6IjJlNGNmZTUwLTA1ODAtNDE0MC05Mzg3LTRlY2RlMzlkZWY2MCIsImMiOjR9",
                           width = "100%",
                           height = "800px",
                           frameborder = "0",
                           allowfullscreen = TRUE,
                           style = "border: none; min-height: 800px;"
                         ),
                         tags$p(
                           style = "text-align: center; color: #7F8C8D; margin-top: 10px;",
                           tags$em("Fuente: Centro de Estudios MINEDUC - Datos Abiertos 2024")
                         )
                       )
                )
              ),
              
              # Panel con más información
              wellPanel(
                style = "margin: 20px;",
                h4(icon("lightbulb"), "Ventajas de integrar Power BI en Shiny"),
                tags$ul(
                  tags$li(strong("Interactividad completa:"), " Los usuarios pueden filtrar y explorar el dashboard directamente"),
                  tags$li(strong("Sin carga en tu servidor:"), " El dashboard se carga desde servidores de Microsoft"),
                  tags$li(strong("Actualización automática:"), " Si actualizas tu Power BI, los cambios se reflejan automáticamente"),
                  tags$li(strong("Responsive:"), " Se adapta a diferentes tamaños de pantalla"),
                  tags$li(strong("Compatible con todos los navegadores:"), " Funciona en Chrome, Firefox, Safari, Edge, etc.")
                )
              )
            )
          ),
          
          # --- PESTAÑA DE PRUEBA (solo visible con autenticación) ---
          tabPanel(
            title = tagList(icon("lock"), "Panel Admin (PRUEBA)"),
            value = "admin_prueba",  # ID único para esta pestaña
            fluidPage(
              div(class="info-card", style="margin:20px;",
                  h2(icon("shield-alt"), "Panel Administrativo - PRUEBA"),
                  p("Esta es una pestaña de prueba del sistema de autenticación con shinymanager.")
              ),
              
              wellPanel(
                h4(icon("user-circle"), "Información del usuario"),
                uiOutput("user_info_ui")
              ),
              
              
              conditionalPanel(
                condition = "output.es_admin == true",
                wellPanel(
                  h4(icon("tools"), "Funciones administrativas"),
                  p("Solo usuarios con rol de administrador ven este panel."),
                  fluidRow(
                    column(4,
                           div(class="metric-card",
                               h5("Total establecimientos"),
                               h2(textOutput("admin_total_establecimientos"))
                           )
                    ),
                    column(4,
                           div(class="metric-card",
                               h5("Total estudiantes"),
                               h2(textOutput("admin_total_estudiantes"))
                           )
                    ),
                    column(4,
                           div(class="metric-card",
                               h5("Total docentes"),
                               h2(textOutput("admin_total_docentes"))
                           )
                    )
                  )
                )
              )
            )
          ) # Fin tabPanel admin
        ) # Fin navbarPage
    ) # Fin div main-content
  ) # Fin shinyjs::hidden
) # Fin fluidPage (UI principal)


# --- Server Shiny
server <- function(input, output, session) {
  
  # 🎬 PANTALLA DE CARGA - Ocultar cuando los datos estén listos
  observe({
    # Esperar a que los datos estén cargados (verificar que existan las variables globales)
    req(exists("matricula_raw"), exists("base_apoyo"))
    
    # Pequeño delay adicional para asegurar que todo esté renderizado
    Sys.sleep(0.5)
    
    # Ocultar pantalla de carga
    shinyjs::hide("loading-screen", anim = TRUE, animType = "fade", time = 0.5)
    
    # Mostrar contenido principal
    shinyjs::show("main-content", anim = TRUE, animType = "fade", time = 0.5)
    
    # La pestaña admin se gestiona con hideTab/showTab más abajo
  })
  
  # --- Sistema de autenticación OPCIONAL con SEGURIDAD MEJORADA 🔒 ---
  usuario_autenticado <- reactiveValues(
    logged_in = FALSE,
    username = NULL,
    is_admin = FALSE,
    login_time = NULL,
    last_activity = Sys.time()
  )
  
  # Control de intentos de login (anti fuerza bruta)
  login_attempts <- reactiveValues(
    count = 0,
    last_attempt = NULL,
    blocked_until = NULL
  )
  
  # Función para registrar eventos de seguridad
  log_security_event <- function(username, action, success) {
    new_log <- data.frame(
      timestamp = as.character(Sys.time()),
      username = username,
      action = action,
      success = success,
      ip = session$clientData$url_hostname,
      stringsAsFactors = FALSE
    )
    security_log <<- rbind(security_log, new_log)
    
    # Guardar log en archivo (opcional)
    # write.csv(security_log, "security_log.csv", row.names = FALSE)
  }
  
  # Timer de inactividad de sesión (30 minutos)
  session_timeout <- reactiveTimer(60000)  # Revisar cada minuto
  
  observe({
    session_timeout()
    if(usuario_autenticado$logged_in) {
      tiempo_inactivo <- as.numeric(difftime(Sys.time(), usuario_autenticado$last_activity, units = "mins"))
      if(tiempo_inactivo > 30) {
        # Auto-logout por inactividad
        log_security_event(usuario_autenticado$username, "auto_logout_timeout", TRUE)
        showNotification("Sesión cerrada por inactividad (30 min)", type = "warning", duration = 5)
        
        # Reset estado
        usuario_autenticado$logged_in <- FALSE
        usuario_autenticado$username <- NULL
        usuario_autenticado$is_admin <- FALSE
        
        shinyjs::show("show_login_modal")
        shinyjs::hide("user_info")
        shinyjs::hide("do_logout")
        shinyjs::hide(selector = "a[data-value='admin_tab']")
      }
    }
  })
  
  # Actualizar última actividad en cada input
  observe({
    reactiveValuesToList(input)
    if(usuario_autenticado$logged_in) {
      usuario_autenticado$last_activity <- Sys.time()
    }
  })
  
  # Mostrar modal de login cuando se hace clic
  observeEvent(input$show_login_modal, {
    showModal(modalDialog(
      title = tagList(icon("user-shield"), " Login Administrativo"),
      size = "s",
      easyClose = TRUE,
      footer = tagList(
        modalButton("Cancelar"),
        actionButton("do_login", "Ingresar", class = "btn-primary", icon = icon("sign-in-alt"))
      ),
      
      wellPanel(
        textInput("login_username", "Usuario:", placeholder = "admin"),
        passwordInput("login_password", "Contraseña:", placeholder = "Ingrese contraseña"),
        uiOutput("login_error_msg")
      )
    ))
  })
  
  # Procesar login CON SEGURIDAD
  observeEvent(input$do_login, {
    req(input$login_username, input$login_password)
    
    # 🛡️ PASO 1: Verificar si está bloqueado por intentos fallidos
    if(!is.null(login_attempts$blocked_until)) {
      if(Sys.time() < login_attempts$blocked_until) {
        tiempo_restante <- as.numeric(difftime(login_attempts$blocked_until, Sys.time(), units = "secs"))
        output$login_error_msg <- renderUI({
          div(style="color:#d9534f;margin-top:10px;font-weight:bold;",
              icon("ban"), sprintf(" Bloqueado. Intente en %d segundos", ceiling(tiempo_restante)))
        })
        return()
      } else {
        # Desbloquear si ya pasó el tiempo
        login_attempts$blocked_until <- NULL
        login_attempts$count <- 0
      }
    }
    
    # 🛡️ PASO 2: Buscar usuario
    usuario_valido <- credentials %>%
      filter(user == input$login_username)
    
    # 🛡️ PASO 3: Verificar contraseña con bcrypt
    if(nrow(usuario_valido) > 0) {
      # Usar checkpw para comparar hash
      password_match <- tryCatch({
        bcrypt::checkpw(input$login_password, usuario_valido$password_hash)
      }, error = function(e) {
        FALSE
      })
      
      if(password_match) {
        # ✅ LOGIN EXITOSO
        usuario_autenticado$logged_in <- TRUE
        usuario_autenticado$username <- usuario_valido$user
        usuario_autenticado$is_admin <- usuario_valido$admin
        usuario_autenticado$login_time <- Sys.time()
        usuario_autenticado$last_activity <- Sys.time()
        
        # Resetear intentos
        login_attempts$count <- 0
        login_attempts$blocked_until <- NULL
        
        # Log de éxito
        log_security_event(usuario_valido$user, "login_success", TRUE)
        
        removeModal()
        
        # Actualizar UI
        shinyjs::hide("show_login_modal")
        shinyjs::show("user_info")
        shinyjs::show("do_logout")
        
        # Mostrar pestañas admin si es admin
        if(usuario_valido$admin) {
          showTab(inputId = "navbar", target = "admin_prueba")
          showTab(inputId = "navbar", target = "powerbi_tab")
        }
        
        showNotification(
          paste0("✅ Bienvenido ", usuario_valido$user, "!"),
          type = "message",
          duration = 3
        )
        
      } else {
        # ❌ Contraseña incorrecta
        login_attempts$count <- login_attempts$count + 1
        login_attempts$last_attempt <- Sys.time()
        
        log_security_event(input$login_username, "login_failed_password", FALSE)
        
        # Bloquear después de 3 intentos
        if(login_attempts$count >= 3) {
          login_attempts$blocked_until <- Sys.time() + 300  # 5 minutos
          log_security_event(input$login_username, "account_blocked", FALSE)
          
          output$login_error_msg <- renderUI({
            div(style="color:#d9534f;margin-top:10px;font-weight:bold;",
                icon("ban"), " Cuenta bloqueada por 5 minutos (demasiados intentos)")
          })
        } else {
          output$login_error_msg <- renderUI({
            div(style="color:#d9534f;margin-top:10px;",
                icon("exclamation-triangle"), 
                sprintf(" Contraseña incorrecta (%d/3 intentos)", login_attempts$count))
          })
        }
      }
    } else {
      # ❌ Usuario no existe
      login_attempts$count <- login_attempts$count + 1
      log_security_event(input$login_username, "login_failed_user", FALSE)
      
      output$login_error_msg <- renderUI({
        div(style="color:#d9534f;margin-top:10px;",
            icon("exclamation-triangle"), " Usuario no encontrado")
      })
    }
  })
  
  # Procesar logout
  observeEvent(input$do_logout, {
    # Log de logout
    if(!is.null(usuario_autenticado$username)) {
      log_security_event(usuario_autenticado$username, "logout", TRUE)
    }
    
    # Resetear estado
    usuario_autenticado$logged_in <- FALSE
    usuario_autenticado$username <- NULL
    usuario_autenticado$is_admin <- FALSE
    usuario_autenticado$login_time <- NULL
    usuario_autenticado$last_activity <- Sys.time()
    
    # Ocultar pestañas admin
    hideTab(inputId = "navbar", target = "admin_prueba")
    hideTab(inputId = "navbar", target = "powerbi_tab")
    
    # Actualizar UI: mostrar botón login, ocultar logout
    shinyjs::show("show_login_modal")
    shinyjs::hide("user_info")
    shinyjs::hide("do_logout")
    
    showNotification(
      "👋 Sesión cerrada",
      type = "warning",
      duration = 2
    )
  })
  
  # Renderizar el nombre de usuario
  output$username_display <- renderText({
    if(usuario_autenticado$logged_in) {
      paste0("👤 ", usuario_autenticado$username)
    } else {
      ""
    }
  })
  
  # --- FIN código de autenticación ---
  
  # Variables reactivas para outputs condicionales
  output$es_admin <- reactive({
    usuario_autenticado$is_admin
  })
  outputOptions(output, "es_admin", suspendWhenHidden = FALSE)
  
  # Ocultar pestañas admin por defecto
  observe({
    hideTab(inputId = "navbar", target = "admin_prueba", session = session)
    hideTab(inputId = "navbar", target = "powerbi_tab", session = session)
  })
  
  # Información del usuario autenticado
  output$user_info_ui <- renderUI({
    if(usuario_autenticado$logged_in) {
      div(
        p(strong("Usuario conectado: "), usuario_autenticado$username),
        p(strong("Rol: "), if(usuario_autenticado$is_admin) "Administrador" else "Usuario estándar"),
        p(strong("Hora de conexión: "), format(Sys.time(), "%d/%m/%Y %H:%M:%S"))
      )
    } else {
      div(
        p(icon("info-circle"), " No hay usuario autenticado."),
        p("Haz clic en 'Login Admin' en la barra superior para acceder a funciones administrativas.")
      )
    }
  })
  
  # Métricas para admin
  output$admin_total_establecimientos <- renderText({
    req(usuario_autenticado$is_admin)
    format(nrow(base_apoyo), big.mark = ".", decimal.mark = ",")
  })
  
  output$admin_total_estudiantes <- renderText({
    req(usuario_autenticado$is_admin)
    format(nrow(matricula_raw), big.mark = ".", decimal.mark = ",")
  })
  
  output$admin_total_docentes <- renderText({
    req(usuario_autenticado$is_admin)
    format(nrow(docentes_raw), big.mark = ".", decimal.mark = ",")
  })
  
  # --- TU CÓDIGO ORIGINAL DE LA APP CONTINÚA AQUÍ ---
  # --- Nueva lógica reactiva pestaña Docentes ---
  observeEvent(input$doc_reset, {
    updateSelectInput(session, "doc_f_region", selected = "Todas")
    updateSelectInput(session, "doc_f_comuna", selected = "Todas")
    updateSelectInput(session, "doc_f_poblacion", selected = "Todas")
    updateSelectizeInput(session, "doc_f_especialidad", selected = NULL)
    updateSelectInput(session, "doc_f_genero", selected = "Todos")
    updateSelectInput(session, "doc_f_dependencia", selected = "Todas")
    updateSelectInput(session, "doc_f_ruralidad", selected = "Todas")
  })
  
  doc_datos <- reactive({
    input$doc_aplicar
    isolate({
      df <- docentes_especialidad_long
      # Enriquecimiento dinámico (solo una vez por sesión se puede cachear si fuera necesario)
      df <- df %>% mutate(
        ANOS_SERV = suppressWarnings(as.numeric(ANO_SERVICIO_SISTEMA)),
        # DOC_FEC_NAC formato yyyymm -> edad
        FEC_NAC = suppressWarnings(as.character(DOC_FEC_NAC)),
        FEC_NAC = ifelse(nchar(FEC_NAC)==6, FEC_NAC, NA),
        NAC_YEAR = suppressWarnings(as.numeric(substr(FEC_NAC,1,4))),
        NAC_MONTH = suppressWarnings(as.numeric(substr(FEC_NAC,5,6))),
        NAC_MONTH = ifelse(NAC_MONTH>=1 & NAC_MONTH<=12, NAC_MONTH, NA),
        EDAD = ifelse(!is.na(NAC_YEAR), {
          hoy <- Sys.Date();
          age <- as.numeric(format(hoy, '%Y')) - NAC_YEAR - ifelse(!is.na(NAC_MONTH) & NAC_MONTH > as.numeric(format(hoy,'%m')), 1, 0);
          ifelse(age<15 | age>90, NA, age)
        }, NA),
        TRAMO_LABEL = dplyr::case_when(
          TRAMO_CARR_DOCENTE == 0 ~ '0: Sin Información',
          TRAMO_CARR_DOCENTE == 1 ~ '1: Acceso',
          TRAMO_CARR_DOCENTE == 2 ~ '2: Inicial',
          TRAMO_CARR_DOCENTE == 3 ~ '3: Temprano',
          TRAMO_CARR_DOCENTE == 4 ~ '4: Avanzado',
          TRAMO_CARR_DOCENTE == 5 ~ '5: Experto I',
          TRAMO_CARR_DOCENTE == 6 ~ '6: Experto II',
          TRUE ~ 'Sin dato'
        ),
        Dependencia_label = dplyr::case_when(
          COD_DEPE2 == 1 ~ 'Municipal',
          COD_DEPE2 == 2 ~ 'Particular Subvencionado',
          COD_DEPE2 == 4 ~ 'Corporación de Administración Delegada',
          COD_DEPE2 == 5 ~ 'Servicio Local de Educación Pública',
          TRUE ~ 'Otra/No informado'
        ),
        Ruralidad_label = dplyr::case_when(
          RURAL_RBD == 1 ~ 'Rural',
          RURAL_RBD == 0 ~ 'Urbana',
          TRUE ~ 'Sin dato'
        )
      )
      if(!is.null(input$doc_f_region) && input$doc_f_region != "Todas") df <- df[df$NOM_REG_RBD_A == input$doc_f_region,]
      if(!is.null(input$doc_f_comuna) && input$doc_f_comuna != "Todas") df <- df[df$NOM_COM_RBD == input$doc_f_comuna,]
      if(!is.null(input$doc_f_poblacion) && input$doc_f_poblacion != "Todas") df <- df[df$Poblacion == input$doc_f_poblacion,]
      if(!is.null(input$doc_f_especialidad) && length(input$doc_f_especialidad)>0) df <- df[df$SUBSECTOR %in% as.integer(input$doc_f_especialidad),]
      if(!is.null(input$doc_f_genero) && input$doc_f_genero != "Todos"){
        if(input$doc_f_genero == 'Femenino') df <- df[df$DOC_GENERO==2,] else df <- df[df$DOC_GENERO==1,]
      }
      if(!is.null(input$doc_f_dependencia) && input$doc_f_dependencia != 'Todas') df <- df[df$Dependencia_label == input$doc_f_dependencia,]
      if(!is.null(input$doc_f_ruralidad) && input$doc_f_ruralidad != 'Todas') df <- df[df$Ruralidad_label == input$doc_f_ruralidad,]
      df
    })
  })
  
  output$kpi_registros <- renderText({ df <- doc_datos(); format(nrow(df), big.mark='.', decimal.mark=',') })
  output$kpi_personas <- renderText({ df <- doc_datos(); format(length(unique(df$MRUN)), big.mark='.', decimal.mark=',') })
  output$kpi_promedio <- renderText({ df <- doc_datos(); p <- length(unique(df$MRUN)); if(p==0) '' else paste0('Promedio registros/persona: ', round(nrow(df)/p,2)) })
  output$kpi_mujeres <- renderText({ df <- doc_datos(); pers <- df %>% filter(!is.na(MRUN)) %>% distinct(MRUN, DOC_GENERO); if(nrow(pers)==0) '-' else paste0(round(100*sum(pers$DOC_GENERO==2)/nrow(pers),1),'%') })
  output$kpi_mediana_edad <- renderText({ df <- doc_datos(); pers <- df %>% distinct(MRUN, EDAD) %>% filter(!is.na(EDAD)); if(nrow(pers)==0) '-' else stats::median(pers$EDAD) })
  output$kpi_prom_servicio <- renderText({ df <- doc_datos(); pers <- df %>% distinct(MRUN, ANOS_SERV) %>% filter(!is.na(ANOS_SERV)); if(nrow(pers)==0) '-' else round(mean(pers$ANOS_SERV),1) })
  
  output$doc_tab_resumen <- DT::renderDT({
    df <- doc_datos(); if(nrow(df)==0) return(DT::datatable(data.frame(Mensaje='Sin datos'), options=list(dom='t')))
    resumen <- df %>%
      mutate(Genero = ifelse(DOC_GENERO==2,'Mujeres', ifelse(DOC_GENERO==1,'Hombres','Desconocido'))) %>%
      group_by(SUBSECTOR, Especialidad) %>%
      summarise(Total = n(), Hombres = sum(Genero=='Hombres'), Mujeres = sum(Genero=='Mujeres'), .groups='drop') %>%
      mutate(`% Hombres` = round(100*Hombres/Total,1), `% Mujeres` = round(100*Mujeres/Total,1)) %>% arrange(desc(Total))
    DT::datatable(resumen, options=list(pageLength=12, scrollX=TRUE), rownames=FALSE)
  })
  
  output$doc_plot_genero <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    # Calcular sobre PERSONAS únicas (no registros) para coincidir con kpi_mujeres
    datos <- df %>%
      filter(!is.na(MRUN)) %>%
      distinct(MRUN, DOC_GENERO) %>%
      mutate(Genero = ifelse(DOC_GENERO==2,'Mujeres', ifelse(DOC_GENERO==1,'Hombres','Desconocido'))) %>%
      count(Genero, name='n') %>%
      mutate(
        pct = round(100*n/sum(n), 1),
        color = dplyr::case_when(
          Genero == 'Mujeres' ~ '#B35A5A',
          Genero == 'Hombres' ~ '#34536A',
          TRUE ~ '#888888'
        )
      ) %>%
      arrange(match(Genero, c('Hombres','Mujeres','Desconocido')))
    plotly::plot_ly(
      datos,
      labels = ~Genero,
      values = ~n,
      type = 'pie',
      text = ~paste0(Genero,': ',pct,'% (',n,' personas)'),
      textinfo = 'text',
      hoverinfo = 'text',
      marker = list(colors = datos$color)
    ) %>%
      layout(showlegend=FALSE, margin=list(l=10,r=10,b=10,t=10))
  })
  
  # Género por Especialidad (% interno registros)
  output$doc_plot_genero_especialidad <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    datos <- df %>% mutate(Genero = ifelse(DOC_GENERO==2,'Mujeres', ifelse(DOC_GENERO==1,'Hombres','Desconocido'))) %>%
      count(Especialidad, Genero, name='n') %>% group_by(Especialidad) %>% mutate(total=sum(n), pct=round(100*n/total,1)) %>% ungroup()
    orden <- datos %>% filter(Genero=='Mujeres') %>% arrange(desc(pct)) %>% pull(Especialidad)
    # Si alguna especialidad no tiene Mujeres (solo Hombres), la agregamos al final manteniendo orden previo
    restantes <- setdiff(unique(datos$Especialidad), orden)
    niveles <- c(orden, restantes)
    datos$Especialidad <- factor(datos$Especialidad, levels=niveles)
    pal_genero <- c('Hombres'='#34536A', 'Mujeres'='#B35A5A', 'Desconocido'='#888888')
    plotly::plot_ly(
      datos,
      x = ~Especialidad,
      y = ~pct,
      color = ~Genero,
      colors = pal_genero,
      type = 'bar',
      text = ~paste0(pct, '% (n=', n, ')'),
      textposition = 'outside',
      texttemplate = '%{text}',
      customdata = ~paste0(Genero, ': ', pct, '% (n=', n, ')'),
      hovertemplate = '<b>%{x}</b><br>%{customdata}<extra></extra>'
    ) %>%
      layout(
        barmode='stack',
        xaxis=list(title='Especialidad', tickangle=-45),
        yaxis=list(title='% dentro de especialidad', range = c(0, 100)),
        height = 520
      )
  })
  
  # Género por Región (% interno registros)
  output$doc_plot_genero_region <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    datos <- df %>% mutate(Genero = ifelse(DOC_GENERO==2,'Mujeres', ifelse(DOC_GENERO==1,'Hombres','Desconocido'))) %>%
      count(NOM_REG_RBD_A, Genero, name='n') %>% group_by(NOM_REG_RBD_A) %>% mutate(total=sum(n), pct=round(100*n/total,1)) %>% ungroup()
    # Orden específico de regiones solicitado
    orden_deseado <- c("AYP", "TPCA", "ANTOF", "ATCMA", "COQ", "VALPO", "RM", "LGBO", "MAULE", "NUBLE", "BBIO", "ARAUC", "RIOS", "LAGOS", "AYSEN", "MAG")
    regiones_presentes <- intersect(orden_deseado, unique(datos$NOM_REG_RBD_A))
    regiones_faltantes <- setdiff(unique(datos$NOM_REG_RBD_A), orden_deseado)
    niveles_region <- c(regiones_presentes, regiones_faltantes)
    datos$NOM_REG_RBD_A <- factor(datos$NOM_REG_RBD_A, levels = niveles_region)
    pal_genero <- c('Hombres'='#34536A', 'Mujeres'='#B35A5A', 'Desconocido'='#888888')
    plotly::plot_ly(
      datos,
      x = ~NOM_REG_RBD_A,
      y = ~pct,
      color = ~Genero,
      colors = pal_genero,
      type = 'bar',
      text = ~paste0(pct, '% (n=', n, ')'),
      textposition = 'outside',
      texttemplate = '%{text}',
      customdata = ~paste0(Genero, ': ', pct, '% (n=', n, ')'),
      hovertemplate = '<b>%{x}</b><br>%{customdata}<extra></extra>'
    ) %>%
      layout(
        barmode='stack',
        xaxis=list(title='Región', tickangle=-45),
        yaxis=list(title='% dentro de región', range = c(0, 100)),
        height = 420
      )
  })
  
  # Cantidad de Docentes por Región
  output$doc_plot_cantidad_region <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    datos <- df %>% 
      count(NOM_REG_RBD_A, name='total') %>%
      arrange(desc(total))
    # Aplicar el mismo orden de regiones que en el gráfico de género
    orden_deseado <- c("AYP", "TPCA", "ANTOF", "ATCMA", "COQ", "VALPO", "RM", "LGBO", "MAULE", "NUBLE", "BBIO", "ARAUC", "RIOS", "LAGOS", "AYSEN", "MAG")
    regiones_presentes <- intersect(orden_deseado, unique(datos$NOM_REG_RBD_A))
    regiones_faltantes <- setdiff(unique(datos$NOM_REG_RBD_A), orden_deseado)
    niveles_region <- c(regiones_presentes, regiones_faltantes)
    datos$NOM_REG_RBD_A <- factor(datos$NOM_REG_RBD_A, levels = niveles_region)
    
    plotly::plot_ly(
      datos,
      x = ~NOM_REG_RBD_A,
      y = ~total,
      type = 'bar',
      marker = list(color = '#5A6E79'),
      text = ~total,
      textposition = 'outside',
      texttemplate = '%{text}',
      hovertemplate = '<b>%{x}</b><br>Total docentes: %{y}<extra></extra>'
    ) %>%
      layout(
        xaxis = list(title = 'Región', tickangle = -45),
        yaxis = list(title = 'Número de Docentes'),
        height = 420
      )
  })
  
  # Distribución por Dependencia administrativa (registros)
  output$doc_plot_dependencia <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    datos <- df %>% mutate(Dependencia = Dependencia_label) %>%
      count(Dependencia, name='n') %>% mutate(pct = round(100*n/sum(n),1)) %>% arrange(desc(n))
    plotly::plot_ly(datos, x=~pct, y=~reorder(Dependencia, pct), type='bar', orientation='h', text=~paste0(pct,'% (',n,')'), hoverinfo='text', marker=list(color='#34536A')) %>%
      layout(xaxis=list(title='% de registros'), yaxis=list(title='Dependencia'))
  })
  
  output$doc_tab_dependencia <- DT::renderDT({
    df <- doc_datos(); if(nrow(df)==0) return(DT::datatable(data.frame(Mensaje='Sin datos'), options=list(dom='t')))
    tabla <- df %>% mutate(Dependencia = Dependencia_label) %>%
      count(Dependencia, name='Registros') %>% mutate(`%` = round(100*Registros/sum(Registros),1)) %>% arrange(desc(Registros))
    DT::datatable(tabla, options=list(pageLength=8, dom='tip'), rownames=FALSE)
  })
  
  # Distribución por Ruralidad (registros)
  output$doc_plot_ruralidad <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    datos <- df %>% mutate(Ruralidad = Ruralidad_label) %>% filter(Ruralidad %in% c('Urbana','Rural')) %>%
      count(Ruralidad, name='n') %>% mutate(pct=round(100*n/sum(n),1))
    plotly::plot_ly(datos, labels=~Ruralidad, values=~n, type='pie', text=~paste0(Ruralidad,': ',pct,'% (',n,')'), textinfo='text', hoverinfo='text', marker=list(colors=c('#34536A','#B35A5A'))) %>%
      layout(showlegend=FALSE, margin=list(l=10,r=10,b=10,t=10))
  })
  
  # Tramo Carrera Docente
  output$doc_plot_tramo <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    datos <- df %>% distinct(MRUN, TRAMO_LABEL) %>% filter(!is.na(TRAMO_LABEL)) %>% count(TRAMO_LABEL, name='n') %>% mutate(pct=round(100*n/sum(n),1)) %>% arrange(n)
    plotly::plot_ly(datos, x=~pct, y=~TRAMO_LABEL, type='bar', orientation='h', text=~paste0(pct,'%'), marker=list(color='#34536A')) %>%
      layout(xaxis=list(title='% de docentes'), yaxis=list(title='Tramo'), margin=list(l=120))
  })
  
  # Distribución de Edades
  output$doc_plot_edad <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    edades <- df %>% distinct(MRUN, EDAD) %>% filter(!is.na(EDAD))
    if(nrow(edades)==0) return(NULL)
    med <- stats::median(edades$EDAD)
    plotly::plot_ly(edades, x=~EDAD, type='histogram', nbinsx=30, marker=list(color='#34536A')) %>%
      layout(
        shapes=list(list(type='line', x0=med, x1=med, y0=0, y1=1, xref='x', yref='paper', line=list(color='#B35A5A', dash='dash'))),
        annotations=list(list(x=med, y=1.02, xref='x', yref='paper', text=paste('Mediana:', med),
                              showarrow=FALSE, font=list(color='#B35A5A', size=12), yanchor='bottom')),
        xaxis=list(title='Edad'), yaxis=list(title='Docentes (personas)')
      )
  })
  
  # Años de servicio
  output$doc_plot_servicio <- renderPlotly({
    df <- doc_datos(); if(nrow(df)==0) return(NULL)
    serv <- df %>% distinct(MRUN, ANOS_SERV) %>% filter(!is.na(ANOS_SERV), ANOS_SERV>=0, ANOS_SERV<=60)
    if(nrow(serv)==0) return(NULL)
    med <- stats::median(serv$ANOS_SERV); prom <- mean(serv$ANOS_SERV)
    plotly::plot_ly(serv, x=~ANOS_SERV, type='histogram', nbinsx=30, marker=list(color='#B35A5A')) %>%
      layout(
        shapes=list(
          list(type='line', x0=med, x1=med, y0=0, y1=1, xref='x', yref='paper', line=list(color='#34536A', width=2)),
          list(type='line', x0=prom, x1=prom, y0=0, y1=1, xref='x', yref='paper', line=list(color='#34536A', dash='dash'))
        ),
        annotations=list(
          list(x=med, y=1.02, xref='x', yref='paper', text=paste('Mediana:', med),
               showarrow=FALSE, font=list(color='#34536A', size=12), yanchor='bottom'),
          list(x=prom, y=0.92, xref='x', yref='paper', text=paste('Promedio:', round(prom,1)),
               showarrow=FALSE, font=list(color='#34536A', size=12), yanchor='top')
        ),
        xaxis=list(title='Años de servicio'), yaxis=list(title='Docentes (personas)')
      )
  })
  
  output$doc_tab_detalle <- DT::renderDT({
    df <- doc_datos();
    cols <- c('MRUN','RBD','NOM_RBD','NOM_REG_RBD_A','NOM_COM_RBD','Dependencia_label','Ruralidad_label','Poblacion','SUBSECTOR','Especialidad','HORAS','TITULO')
    cols <- intersect(cols, names(df))
    DT::datatable(df[cols], options=list(pageLength=20, scrollX=TRUE), rownames=FALSE)
  })
  
  output$doc_descarga <- downloadHandler(
    filename = function(){ paste0('docentes_especialidad_', Sys.Date(), '.csv') },
    content = function(file){ write.csv(doc_datos(), file, row.names=FALSE, fileEncoding='UTF-8') }
  )
  
  # Descarga de reporte PDF de docentes
  output$doc_descarga_pdf <- downloadHandler(
    filename = function() {
      paste0("reporte_docentes_", format(Sys.Date(), "%Y%m%d"), ".pdf")
    },
    content = function(file) {
      # Mostrar mensaje de progreso
      showNotification("Generando reporte PDF... Por favor espere.", 
                       type = "message", duration = NULL, id = "pdf_progress")
      
      tryCatch({
        # Obtener datos filtrados
        datos <- doc_datos()
        
        if (nrow(datos) == 0) {
          showNotification("No hay datos para generar el reporte", type = "error")
          return(NULL)
        }
        
        # Calcular ANOS_SERV si no existe
        if (!"ANOS_SERV" %in% names(datos) && "ANO_SERVICIO_SISTEMA" %in% names(datos)) {
          datos <- datos %>%
            dplyr::mutate(ANOS_SERV = 2024 - ANO_SERVICIO_SISTEMA)
        }
        
        # Calcular EDAD si no existe
        if (!"EDAD" %in% names(datos) && "DOC_FEC_NAC" %in% names(datos)) {
          datos <- datos %>%
            dplyr::mutate(EDAD = 2024 - as.numeric(format(as.Date(DOC_FEC_NAC), "%Y")))
        }
        
        # Preparar KPIs
        personas_unicas <- datos %>% dplyr::distinct(MRUN) %>% nrow()
        registros_totales <- nrow(datos)
        
        # Calcular mediana de edad
        mediana_edad_val <- datos %>% 
          dplyr::distinct(MRUN, .keep_all = TRUE) %>% 
          dplyr::pull(EDAD) %>% 
          stats::median(na.rm = TRUE)
        
        # Calcular promedio años de servicio
        prom_servicio_val <- datos %>% 
          dplyr::distinct(MRUN, .keep_all = TRUE) %>% 
          dplyr::pull(ANOS_SERV) %>% 
          mean(na.rm = TRUE)
        
        resumen_kpis <- list(
          registros = registros_totales,
          personas = personas_unicas,
          promedio_rbd = if(personas_unicas > 0) registros_totales / personas_unicas else 0,
          mediana_edad = if(!is.na(mediana_edad_val)) mediana_edad_val else 0,
          prom_servicio = if(!is.na(prom_servicio_val)) prom_servicio_val else 0,
          pct_mujeres = if(personas_unicas > 0) {
            datos %>% dplyr::distinct(MRUN, .keep_all = TRUE) %>%
              dplyr::summarise(pct = sum(DOC_GENERO == 2, na.rm = TRUE) / dplyr::n() * 100) %>%
              dplyr::pull(pct)
          } else 0
        )
        
        # Resumen por especialidad - verificar que existan las columnas
        if ("Especialidad" %in% names(datos)) {
          resumen_especialidad <- datos %>%
            dplyr::group_by(Especialidad) %>%
            dplyr::summarise(
              Registros = dplyr::n(),
              Docentes = dplyr::n_distinct(MRUN),
              Pct_Mujeres = sum(DOC_GENERO == 2, na.rm = TRUE) / dplyr::n() * 100,
              .groups = 'drop'
            ) %>%
            dplyr::arrange(desc(Docentes))
          
          # Renombrar columna para evitar problemas con %
          names(resumen_especialidad)[4] <- "Porcentaje_Mujeres"
          
        } else {
          resumen_especialidad <- data.frame(
            Especialidad = "No disponible",
            Registros = nrow(datos),
            Docentes = personas_unicas,
            Porcentaje_Mujeres = 0
          )
        }
        
        # Filtros aplicados
        filtros <- list(
          Región = input$doc_f_region,
          Comuna = input$doc_f_comuna,
          Enseñanza = input$doc_f_poblacion,
          Especialidad = paste(input$doc_f_especialidad, collapse = ", "),
          Género = input$doc_f_genero,
          Dependencia = input$doc_f_dependencia,
          Ruralidad = input$doc_f_ruralidad
        )
        
        # Generar plots (versión estática para PDF)
        # Plot género general
        plot_genero <- NULL
        if (personas_unicas > 0 && "DOC_GENERO_label" %in% names(datos)) {
          datos_genero <- datos %>%
            dplyr::distinct(MRUN, .keep_all = TRUE) %>%
            dplyr::count(DOC_GENERO_label) %>%
            dplyr::mutate(pct = n / sum(n) * 100)
          
          plot_genero <- ggplot(datos_genero, aes(x = "", y = pct, fill = DOC_GENERO_label)) +
            geom_bar(stat = "identity", width = 1) +
            coord_polar("y") +
            labs(fill = "Género", title = "Distribución por Género") +
            theme_minimal() +
            theme(axis.text = element_blank(),
                  axis.title = element_blank())
        }
        
        # Plot género por especialidad
        plot_genero_esp <- NULL
        if (nrow(datos) > 0 && "Especialidad" %in% names(datos)) {
          datos_esp <- datos %>%
            dplyr::group_by(Especialidad) %>%
            dplyr::summarise(
              Total = dplyr::n(),
              Mujeres = sum(DOC_GENERO == 2, na.rm = TRUE),
              Pct_Mujeres = Mujeres / Total * 100,
              .groups = 'drop'
            ) %>%
            dplyr::arrange(desc(Total)) %>%
            head(15)
          
          plot_genero_esp <- ggplot(datos_esp, aes(x = reorder(Especialidad, Pct_Mujeres), y = Pct_Mujeres)) +
            geom_col(fill = "#E74C3C") +
            coord_flip() +
            labs(x = NULL, y = "% Mujeres", title = "Género por Especialidad (Top 15)") +
            theme_minimal()
        }
        
        # Renderizar el RMarkdown
        rmarkdown::render(
          input = "templates/reporte_docentes_completo.Rmd",
          output_file = basename(file),
          output_dir = dirname(file),
          params = list(
            datos = datos,
            resumen_kpis = resumen_kpis,
            filtros_aplicados = filtros,
            resumen_especialidad = resumen_especialidad,
            plot_genero = plot_genero,
            plot_genero_esp = plot_genero_esp,
            plot_genero_region = NULL,
            plot_dependencia = NULL,
            plot_ruralidad = NULL,
            plot_edad = NULL,
            plot_servicio = NULL,
            plot_tramo = NULL,
            muestra_datos = datos
          ),
          envir = new.env(parent = globalenv())
        )
        
        removeNotification(id = "pdf_progress")
        showNotification("¡Reporte PDF generado exitosamente!", type = "message", duration = 5)
        
      }, error = function(e) {
        removeNotification(id = "pdf_progress")
        showNotification(paste("Error al generar PDF:", e$message), type = "error", duration = 10)
      })
    }
  )
  
  # Glosario/ayuda para la pestaña docentes
  output$glosario_docentes <- renderUI({
    tagList(
      div(class = "alert-info", style = "margin-bottom: 15px;",
          tags$strong("¿Qué muestra esta tabla?"),
          p("La base contiene docentes por establecimiento (RBD) y especialidad. Cada docente puede impartir Formación General (SUBSECTOR1/SUBSECTOR2 entre 31001 y 39501) o Módulos de Especialidad (otros códigos). Aquí se muestran principalmente los docentes que imparten módulos de especialidad.")
      ),
      div(class = "alert-info", style = "margin-bottom: 15px;",
          tags$strong("Códigos relevantes:"),
          tags$ul(
            tags$li("SUBSECTOR1/SUBSECTOR2: Código de la asignatura o módulo que imparte el docente."),
            tags$li("31001-39501: Formación General en una especialidad."),
            tags$li("Otros códigos: Módulos de especialidad EMTP.")
          )
      )
    )
  })
  # --- Botón para reiniciar filtros en Mapa de Matrícula ---
  observeEvent(input$reset_filtros_mapa, {
    updateSelectInput(session, "rft", selected = "Todas")
    updateSelectInput(session, "region", selected = "Todas")
    updateSelectInput(session, "provincia", selected = "Todas")
    updateSelectInput(session, "comuna", selected = "Todas")
    updateSelectizeInput(session, "especialidad", selected = "")
    updateSelectInput(session, "dependencia", selected = "Todas")
    updateSelectInput(session, "sostenedor_mapa", selected = "Todos")
  })
  
  # --- Botón para reiniciar filtros en Visualizaciones ---
  observeEvent(input$reset_filtros_viz, {
    updateSelectizeInput(session, "filtro_especialidad", selected = "")
    updateSelectInput(session, "nivel", selected = "Ambos")
    updateSelectizeInput(session, "filtro_region", selected = "")
    updateSelectInput(session, "filtro_dependencia", selected = "Todas")
    # Si hay otros filtros personalizados, agregarlos aquí
    # Ejemplo: updateSelectInput(session, "grado", selected = "Todas")
  })
  # --- Botón para reiniciar filtros en Buscador de Establecimientos ---
  observeEvent(input$reset_filtros, {
    updateSelectInput(session, "rft_busqueda", selected = "Todas")
    updateSelectInput(session, "region_busqueda", selected = "Todas")
    updateSelectInput(session, "provincia_busqueda", selected = "Todas")
    updateSelectInput(session, "comuna_busqueda", selected = "Todas")
    updateSelectInput(session, "dependencia_busqueda", selected = "Todas")
    updateSelectInput(session, "sostenedor_busqueda", selected = "Todos")
    updateSelectizeInput(session, "especialidad_busqueda", selected = "")
    updateTextInput(session, "rbd_busqueda", value = "")
    updateTextInput(session, "nombre_busqueda", value = "")
  })
  
  # --- Habilitar/Deshabilitar botón de descarga según resultados ---
  observe({
    # Obtener la tabla de establecimientos filtrados
    tabla <- tryCatch({
      datos <- datos_visual()
      datos %>%
        group_by(rbd, nom_rbd, nom_reg_rbd_a, nom_com_rbd, nom_espe, cod_men) %>%
        summarise(Total = n(), .groups = "drop")
    }, error = function(e) NULL)
    
    habilitar <- !is.null(tabla) && nrow(tabla) > 0
    session$sendCustomMessage(type = "toggleDownloadBtn", message = list(enabled = habilitar))
  })
  # --- JS para habilitar/deshabilitar el botón de descarga ---
  shiny::addResourcePath("customjs", "www")
  tags$head(tags$script(src = "customjs/toggleDownload.js"))
  
  # Valores reactivos para el estado de la aplicación
  values <- reactiveValues(
    cargando = FALSE,
    mensaje_estado = "Listo"
  )
  
  # Función para mostrar mensajes de estado
  mostrar_estado <- function(mensaje) {
    values$mensaje_estado <- mensaje
    showNotification(mensaje, type = "message", duration = 3)
  }
  
  # Validación de datos al inicio
  observe({
    if(nrow(matricula_raw) == 0) {
      showNotification("Error: No se pudieron cargar los datos de matrícula", 
                       type = "error", duration = NULL)
    } else {
      mostrar_estado(paste("Datos cargados correctamente:", 
                           format(nrow(matricula_raw), big.mark = ","), 
                           "registros de matrícula"))
    }
  })
  
  observeEvent(input$rft, {
    if (input$rft == "Todas") {
      regiones <- sort(unique(comunas$nom_reg_rbd_a))
    } else {
      regiones <- comunas %>%
        filter(rft == input$rft) %>%
        pull(nom_reg_rbd_a) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "region",
                      choices = c("Todas", regiones),
                      selected = "Todas")
    
    # Actualiza provincias
    provincias <- if (input$rft == "Todas") {
      sort(unique(comunas$nom_deprov_rbd))
    } else {
      comunas %>%
        filter(rft == input$rft) %>%
        pull(nom_deprov_rbd) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "provincia",
                      choices = c("Todas", provincias),
                      selected = "Todas")
    
    # Actualiza comunas
    comunas_disp <- if (input$rft == "Todas") {
      sort(unique(comunas$nom_com_rbd))
    } else {
      comunas %>%
        filter(rft == input$rft) %>%
        pull(nom_com_rbd) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "comuna",
                      choices = c("Todas", comunas_disp),
                      selected = "Todas")
  })
  
  
  
  # Actualizar provincias según región seleccionada
  observeEvent(input$region, {
    if (input$region == "Todas") {
      provincias <- if (input$rft == "Todas") {
        sort(unique(comunas$nom_deprov_rbd))
      } else {
        comunas %>%
          filter(rft == input$rft) %>%
          pull(nom_deprov_rbd) %>%
          unique() %>%
          sort()
      }
    } else {
      provincias <- comunas %>%
        filter(nom_reg_rbd_a == input$region) %>%
        pull(nom_deprov_rbd) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "provincia",
                      choices = c("Todas", provincias),
                      selected = "Todas")
  })
  
  observeEvent(c(input$region, input$provincia), {
    if (input$provincia == "Todas" & input$region == "Todas") {
      comunas_disp <- if (input$rft == "Todas") {
        sort(unique(comunas$nom_com_rbd))
      } else {
        comunas %>%
          filter(rft == input$rft) %>%
          pull(nom_com_rbd) %>%
          unique() %>%
          sort()
      }
    } else if (input$provincia == "Todas" & input$region != "Todas") {
      comunas_disp <- comunas %>%
        filter(nom_reg_rbd_a == input$region) %>%
        pull(nom_com_rbd) %>%
        unique() %>%
        sort()
    } else {
      comunas_disp <- comunas %>%
        filter(nom_deprov_rbd == input$provincia) %>%
        pull(nom_com_rbd) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "comuna",
                      choices = c("Todas", comunas_disp),
                      selected = "Todas")
  })
  
  
  observeEvent(input$especialidad, {
    comunas_especialidad <- if ("Todas" %in% input$especialidad) {
      comunas
    } else {
      comunas %>% filter(nom_espe %in% input$especialidad)
    }
    
    rfts <- sort(unique(comunas_especialidad$rft))
    regiones <- sort(unique(comunas_especialidad$nom_reg_rbd_a))
    provincias <- sort(unique(comunas_especialidad$nom_deprov_rbd))
    comunas_disp <- sort(unique(comunas_especialidad$nom_com_rbd))
    
    updateSelectInput(session, "rft", choices = c("Todas", rfts), selected = "Todas")
    updateSelectInput(session, "region", choices = c("Todas", regiones), selected = "Todas")
    updateSelectInput(session, "provincia", choices = c("Todas", provincias), selected = "Todas")
    updateSelectInput(session, "comuna", choices = c("Todas", comunas_disp), selected = "Todas")
  })
  
  observeEvent(input$rft_busqueda, {
    regiones <- if (input$rft_busqueda == "Todas") {
      sort(unique(matricula_raw$nom_reg_rbd_a))
    } else {
      matricula_raw %>%
        filter(rft == input$rft_busqueda) %>%
        pull(nom_reg_rbd_a) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "region_busqueda", choices = c("Todas", regiones), selected = "Todas")
    
    provincias <- if (input$rft_busqueda == "Todas") {
      sort(unique(matricula_raw$nom_deprov_rbd))
    } else {
      matricula_raw %>%
        filter(rft == input$rft_busqueda) %>%
        pull(nom_deprov_rbd) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "provincia_busqueda", choices = c("Todas", provincias), selected = "Todas")
    
    comunas_disp <- if (input$rft_busqueda == "Todas") {
      sort(unique(matricula_raw$nom_com_rbd))
    } else {
      matricula_raw %>%
        filter(rft == input$rft_busqueda) %>%
        pull(nom_com_rbd) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "comuna_busqueda", choices = c("Todas", comunas_disp), selected = "Todas")
  })
  
  observeEvent(input$region_busqueda, {
    provincias <- if (input$region_busqueda == "Todas") {
      if (input$rft_busqueda == "Todas") {
        sort(unique(matricula_raw$nom_deprov_rbd))
      } else {
        matricula_raw %>%
          filter(rft == input$rft_busqueda) %>%
          pull(nom_deprov_rbd) %>%
          unique() %>%
          sort()
      }
    } else {
      matricula_raw %>%
        filter(nom_reg_rbd_a == input$region_busqueda) %>%
        pull(nom_deprov_rbd) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "provincia_busqueda", choices = c("Todas", provincias), selected = "Todas")
  })
  
  observeEvent(c(input$region_busqueda, input$provincia_busqueda), {
    comunas_disp <- if (input$provincia_busqueda == "Todas" & input$region_busqueda == "Todas") {
      if (input$rft_busqueda == "Todas") {
        sort(unique(matricula_raw$nom_com_rbd))
      } else {
        matricula_raw %>%
          filter(rft == input$rft_busqueda) %>%
          pull(nom_com_rbd) %>%
          unique() %>%
          sort()
      }
    } else if (input$provincia_busqueda == "Todas" & input$region_busqueda != "Todas") {
      matricula_raw %>%
        filter(nom_reg_rbd_a == input$region_busqueda) %>%
        pull(nom_com_rbd) %>%
        unique() %>%
        sort()
    } else {
      matricula_raw %>%
        filter(nom_deprov_rbd == input$provincia_busqueda) %>%
        pull(nom_com_rbd) %>%
        unique() %>%
        sort()
    }
    updateSelectInput(session, "comuna_busqueda", choices = c("Todas", comunas_disp), selected = "Todas")
  })
  
  observeEvent(input$especialidad_busqueda, {
    # Si no hay selección, usamos todas las especialidades
    comunas_especialidad <- if (is.null(input$especialidad_busqueda) || length(input$especialidad_busqueda) == 0) {
      comunas
    } else {
      comunas %>% filter(nom_espe %in% input$especialidad_busqueda)
    }
    
    # Actualizamos los demás select inputs según las especialidades seleccionadas
    rfts <- sort(unique(comunas_especialidad$rft))
    regiones <- sort(unique(comunas_especialidad$nom_reg_rbd_a))
    provincias <- sort(unique(comunas_especialidad$nom_deprov_rbd))
    comunas_disp <- sort(unique(comunas_especialidad$nom_com_rbd))
    
    updateSelectInput(session, "rft_busqueda", choices = c("Todas", rfts), selected = "Todas")
    updateSelectInput(session, "region_busqueda", choices = c("Todas", regiones), selected = "Todas")
    updateSelectInput(session, "provincia_busqueda", choices = c("Todas", provincias), selected = "Todas")
    updateSelectInput(session, "comuna_busqueda", choices = c("Todas", comunas_disp), selected = "Todas")
  })
  
  
  
  # --- Optimización: Crear índices para joins más rápidos ---
  # Después de cargar los datos, antes del UI
  matricula_raw <- matricula_raw %>%
    arrange(rbd, cod_com_rbd) # Ordenar para mejorar joins
  
  base_apoyo <- base_apoyo %>%
    arrange(rbd)
  
  # Cache de datos frecuentemente usados
  especialidades_unicas <- sort(unique(matricula_raw$nom_espe))
  regiones_unicas <- sort(unique(matricula_raw$nom_reg_rbd_a))
  comunas_unicas <- sort(unique(matricula_raw$nom_com_rbd))
  sostenedores_unicos <- sort(unique(matricula_raw$nombre_sost))
  
  # Mejorar datos_filtrados con debounce para evitar recálculos excesivos
  datos_filtrados <- debounce(reactive({
    values$cargando <- TRUE
    on.exit(values$cargando <- FALSE)
    
    comunas_f <- comunas
    matricula_f <- matricula_raw
    
    # Aplicar filtros de manera más eficiente
    filtros <- list(
      region = if(input$region != "Todas") input$region else NULL,
      provincia = if(input$provincia != "Todas") input$provincia else NULL,
      comuna = if(input$comuna != "Todas") input$comuna else NULL,
      rft = if(input$rft != "Todas") input$rft else NULL,
      dependencia = if(input$dependencia != "Todas") input$dependencia else NULL,
      sostenedor = if(input$sostenedor_mapa != "Todos") input$sostenedor_mapa else NULL
    )
    
    # Aplicar filtros solo si existen
    if(!is.null(filtros$region)) {
      comunas_f <- comunas_f %>% filter(nom_reg_rbd_a == filtros$region)
      matricula_f <- matricula_f %>% filter(nom_reg_rbd_a == filtros$region)
    }
    
    if(!is.null(filtros$provincia)) {
      comunas_f <- comunas_f %>% filter(nom_deprov_rbd == filtros$provincia)
      matricula_f <- matricula_f %>% filter(nom_deprov_rbd == filtros$provincia)
    }
    
    if(!is.null(filtros$comuna)) {
      comunas_f <- comunas_f %>% filter(nom_com_rbd == filtros$comuna)
      matricula_f <- matricula_f %>% filter(nom_com_rbd == filtros$comuna)
    }
    
    if(!is.null(filtros$rft)) {
      comunas_f <- comunas_f %>% filter(rft == filtros$rft)
      matricula_f <- matricula_f %>% filter(rft == filtros$rft)
    }
    
    if(!is.null(filtros$dependencia)) {
      matricula_f <- matricula_f %>% filter(cod_depe2 == filtros$dependencia)
    }
    
    if(!is.null(filtros$sostenedor)) {
      matricula_f <- matricula_f %>% filter(nombre_sost == filtros$sostenedor)
      comunas_f <- comunas_f %>% filter(cod_comuna %in% unique(matricula_f$cod_comuna))
    }
    
    # Filtro por especialidad
    if(!is.null(input$especialidad) && length(input$especialidad) > 0 && !"Todas" %in% input$especialidad) {
      comunas_f <- comunas_f %>% filter(nom_espe %in% input$especialidad)
      matricula_f <- matricula_f %>% filter(nom_espe %in% input$especialidad)
    }
    
    # Actualizar colores del mapa
    comunas_actual <- comunas %>%
      mutate(
        fill_color_final = ifelse(cod_comuna %in% comunas_f$cod_comuna, fill_color_final, "#BBBBBB"),
        fill_opacity = ifelse(cod_comuna %in% comunas_f$cod_comuna, fill_opacity, 0.2)
      )
    
    mostrar_estado(paste("Filtros aplicados:", format(nrow(matricula_f), big.mark = ","), "registros"))
    
    list(comunas = comunas_actual, matricula = matricula_f)
  }), 500) # Debounce de 500ms
  
  # ========================= KPIs Inicio (reubicados dentro del server) =========================
  output$kpi_total_matricula_inicio <- renderText({
    df <- tryCatch(datos_filtrados()$matricula, error = function(e) NULL)
    if (is.null(df)) return("-")
    format(nrow(df), big.mark = ".")
  })
  output$kpi_establecimientos_inicio <- renderText({
    df <- tryCatch(datos_filtrados()$matricula, error = function(e) NULL)
    if (is.null(df)) return("-")
    format(dplyr::n_distinct(df$rbd), big.mark = ".")
  })
  output$kpi_hombres_inicio <- renderText({
    df <- tryCatch(datos_filtrados()$matricula, error = function(e) NULL)
    if (is.null(df)) return("-")
    format(sum(df$gen_alu == 1, na.rm = TRUE), big.mark = ".")
  })
  output$kpi_mujeres_inicio <- renderText({
    df <- tryCatch(datos_filtrados()$matricula, error = function(e) NULL)
    if (is.null(df)) return("-")
    format(sum(df$gen_alu == 2, na.rm = TRUE), big.mark = ".")
  })
  
  # Filtro dinámico para grado según el nivel
  # UI dinámica para grado (no cambia)
  output$grado_ui <- renderUI({
    if (input$nivel == "Niños y Jóvenes") {
      selectInput("grado", "Grado:",
                  choices = c("Todos" = "Todos",
                              "3° medio" = "3",
                              "4° medio" = "4"),
                  selected = "Todos")
    } else if (input$nivel == "Adultos") {
      selectInput("grado", "Grado:",
                  choices = c("Todos" = "Todos",
                              "1° nivel (1° y 2° medio sólo adultos)" = "1"),
                  selected = "Todos")
    } else {
      selectInput("grado", "Grado:",
                  choices = c("Todos" = "Todos",
                              "1° nivel (1° y 2° medio sólo adultos)" = "1",
                              "3° medio" = "3",
                              "4° medio" = "4"),
                  selected = "Todos")
    }
  })
  
  # --- Datos filtrados con Región y Dependencia ---
  datos_visual <- reactive({
    datos <- matricula_raw
    
    # Filtro por especialidad
    if (!is.null(input$filtro_especialidad)) {
      if ("Todas" %in% input$filtro_especialidad) {
        # Si "Todas" está seleccionada, no filtramos
        datos <- datos
      } else {
        datos <- datos %>% filter(nom_espe %in% input$filtro_especialidad)
      }
    }
    
    # Filtro por nivel
    if (input$nivel == "Niños y Jóvenes") {
      datos <- datos %>% filter(cod_ense2 == 7)
    } else if (input$nivel == "Adultos") {
      datos <- datos %>% filter(cod_ense2 == 8)
    }
    
    # Filtro por grado
    if (!is.null(input$grado) && input$grado != "Todos") {
      datos <- datos %>% filter(cod_grado == as.numeric(input$grado))
    }
    
    if (!is.null(input$filtro_region)) {
      if ("Todas" %in% input$filtro_region) {
        # Si "Todas" está seleccionada, no filtramos
        datos <- datos
      } else {
        datos <- datos %>% filter(nom_reg_rbd_a %in% input$filtro_region)
      }
    }
    
    
    # Filtro por dependencia
    if (!is.null(input$filtro_dependencia) && input$filtro_dependencia != "Todas") {
      datos <- datos %>% filter(cod_depe2 == input$filtro_dependencia)
    }
    
    # Etiquetas para grado
    datos <- datos %>%
      mutate(grado_etiqueta = case_when(
        cod_grado == 1 ~ "1° nivel (1° y 2° medio sólo adultos)",
        cod_grado == 3 ~ "3° medio",
        cod_grado == 4 ~ "4° medio",
        TRUE ~ as.character(cod_grado)
      ))
    
    datos
  })
  
  # --- Resúmenes para las tarjetas ---
  output$total_matricula <- renderText({
    nrow(datos_visual())
  })
  
  output$total_matricula_filtrada <- renderText({
    format(nrow(datos_visual()), big.mark = ".")
  })
  
  output$total_hombres <- renderText({
    sum(datos_visual()$gen_alu == 1, na.rm = TRUE)
  })
  
  output$total_mujeres <- renderText({
    sum(datos_visual()$gen_alu == 2, na.rm = TRUE)
  })
  
  # Total establecimientos
  output$total_establecimientos <- renderText({
    n_distinct(datos_visual()$rbd)
  })
  
  output$tabla_dependencia <- renderDT({
    datos_dep <- datos_visual() %>%
      group_by(cod_depe2) %>%
      summarise(N = n_distinct(rbd), .groups = "drop") %>%
      mutate(Pct = round(N / sum(N) * 100, 1))
    
    datatable(
      datos_dep,
      colnames = c("Dependencia", "N", "%"),
      options = list(
        dom = 't',          # Solo la tabla sin filtros ni paginación
        paging = FALSE,
        ordering = FALSE,
        columnDefs = list(list(className = 'dt-center', targets = "_all"))
      ),
      rownames = FALSE
    )
  }, server = FALSE)
  
  # Porcentaje de Hombres
  output$pct_hombres <- renderText({
    total <- nrow(datos_visual())
    if (total == 0) return("0%")
    hombres <- sum(datos_visual()$gen_alu == 1, na.rm = TRUE)
    paste0(round(hombres / total * 100, 1), "%")
  })
  
  # Porcentaje de Mujeres
  output$pct_mujeres <- renderText({
    total <- nrow(datos_visual())
    if (total == 0) return("0%")
    mujeres <- sum(datos_visual()$gen_alu == 2, na.rm = TRUE)
    paste0(round(mujeres / total * 100, 1), "%")
  })
  
  # Número de especialidades distintas
  output$num_especialidades <- renderText({
    length(unique(datos_visual()$nom_espe))
  })
  
  # Número de establecimientos (RBD) distintos
  output$num_establecimientos <- renderText({
    length(unique(datos_visual()$rbd))
  })
  
  # --- Outputs para pestaña Inicio ---
  output$total_matricula_inicio <- renderText({
    format(nrow(matricula_raw), big.mark = ".")
  })
  
  output$total_establecimientos_inicio <- renderText({
    format(n_distinct(matricula_raw$rbd), big.mark = ".")
  })
  
  output$total_especialidades_inicio <- renderText({
    format(n_distinct(matricula_raw$nom_espe), big.mark = ".")
  })
  
  
  # Gráfico de barras: matrícula por especialidad con % Hombres y Mujeres
  output$grafico_barras <- renderPlotly({
    datos_barras <- datos_visual() %>%
      group_by(nom_espe, gen_alu) %>%
      summarise(Total = n(), .groups = "drop") %>%
      tidyr::pivot_wider(names_from = gen_alu, values_from = Total, values_fill = 0) %>%
      mutate(
        Hombres = `1`,
        Mujeres = `2`,
        Total = Hombres + Mujeres,
        pct_Hombres = Hombres / Total * 100,
        pct_Mujeres = Mujeres / Total * 100
      ) %>%
      arrange(pct_Mujeres) %>% 
      mutate(nom_espe = factor(nom_espe, levels = nom_espe))
    
    p <- plot_ly(
      datos_barras,
      x = ~nom_espe,
      y = ~pct_Hombres,
      type = 'bar',
      name = 'Hombres',
      marker = list(color = "#3B5268")
    ) %>%
      add_trace(y = ~pct_Mujeres, name = 'Mujeres', marker = list(color = "#A75F5D")) %>%
      layout(
        title = "Matrícula por Especialidad (% por Género)",
        barmode = 'stack',
        margin = list(b = 150),
        xaxis = list(title = "Especialidad", tickangle = -45),
        yaxis = list(title = "% de Estudiantes")
      )
    
    return(apply_plotly_theme(p))
  })
  
  # Gráfico de torta: proporción por género (total general)
  output$grafico_torta <- renderPlotly({
    datos_torta <- datos_visual() %>%
      mutate(Genero = case_when(
        gen_alu == 1 ~ "Hombres",
        gen_alu == 2 ~ "Mujeres",
        TRUE ~ "Desconocido"
      )) %>%
      group_by(Genero) %>%
      summarise(Total = n(), .groups = "drop")
    
    datos_torta <- datos_torta %>%
      mutate(color = dplyr::case_when(
        Genero == "Hombres" ~ "#3B5268",
        Genero == "Mujeres" ~ "#A75F5D",
        TRUE ~ "#C0C8D2"
      ))
    p <- plot_ly(
      datos_torta,
      labels = ~Genero,
      values = ~Total,
      type = "pie",
      marker = list(colors = datos_torta$color)
    ) %>%
      layout(title = "Distribución por Género")
    
    return(apply_plotly_theme(p))
  })
  
  # Gráfico de barras: matrícula por nivel y grado
  output$grafico_nivel_grado <- renderPlotly({
    datos <- datos_visual() %>%
      mutate(
        Nivel = case_when(cod_ense2 == 7 ~ "Niños y Jóvenes",
                          cod_ense2 == 8 ~ "Adultos"),
        Grado = case_when(cod_grado == 1 ~ "1° nivel",
                          cod_grado == 3 ~ "3° medio",
                          cod_grado == 4 ~ "4° medio")
      ) %>%
      group_by(Nivel, Grado, gen_alu) %>%
      summarise(Total = n(), .groups = "drop") %>%
      tidyr::pivot_wider(names_from = gen_alu, values_from = Total, values_fill = 0) %>%
      mutate(Hombres = `1`, Mujeres = `2`, Total_Grado = Hombres + Mujeres)
    
    fig <- plot_ly(
      datos,
      x = ~Grado,
      y = ~Hombres,
      type = 'bar',
      name = 'Hombres',
      color = I("#3B5268")
    ) %>%
      add_trace(y = ~Mujeres, name = 'Mujeres', color = I("#A75F5D")) %>%
      layout(
        title = "Matrícula por Grado",
        barmode = 'stack',
        xaxis = list(title = "Grado"),
        yaxis = list(title = "Número de Estudiantes")
      ) %>%
      add_text(
        x = ~Grado,
        y = ~Total_Grado,
        text = ~Total_Grado,
        textposition = "outside",
        showlegend = FALSE,
        textfont = list(color = "black", size = 14),
        inherit = FALSE  # <-- Esto es clave
      )
    
    return(apply_plotly_theme(fig))
  })
  
  # Gráfico por establecimientos y dependencia
  output$establecimientos_dependencia <- renderPlotly({
    datos_est <- datos_visual() %>%
      group_by(cod_depe2) %>%
      summarise(N = n_distinct(rbd), .groups = "drop")
    
    p <- plot_ly(
      datos_est,
      x = ~cod_depe2,
      y = ~N,
      type = 'bar',
      marker = list(color = "#34536A")
    ) %>%
      layout(
        title = "Establecimientos por Dependencia",
        xaxis = list(title = "Dependencia"),
        yaxis = list(title = "Número de Establecimientos")
      )
    
    return(apply_plotly_theme(p))
  })
  
  # Gráfico comparativo por región
  output$grafico_regional <- renderPlotly({
    datos_regional <- datos_visual() %>%
      group_by(nom_reg_rbd_a) %>%
      summarise(
        Matricula = n(),
        Establecimientos = n_distinct(rbd),
        Especialidades = n_distinct(nom_espe),
        .groups = "drop"
      ) %>%
      arrange(desc(Matricula)) %>%
      slice_head(n = 10)  # Top 10 regiones
    
    p <- plot_ly(
      datos_regional,
      x = ~reorder(nom_reg_rbd_a, Matricula),
      y = ~Matricula,
      type = 'bar',
      marker = list(color = "#5A6E79"),
      hovertemplate = paste(
        "<b>%{x}</b><br>",
        "Matrícula: %{y:,}<br>",
        "<extra></extra>"
      )
    ) %>%
      layout(
        title = "Top 10 Regiones por Matrícula EMTP",
        xaxis = list(title = "Región", tickangle = -45),
        yaxis = list(title = "Matrícula"),
        margin = list(b = 150)
      )
    
    return(apply_plotly_theme(p))
  })
  
  # Crear tabla de menciones
  menciones <- tibble(
    cod_men = c(41005001,41005002,41005003,
                51007001,51007002,51007003,51007004,
                52013001,52013002,52013003,52013004,
                56027001,56027002,56027003,
                61003001,61003002,61003003,
                64003001,64003002,64003003,
                72007001,72007002,72007003,72007004),
    Glosa_Mencion = c("Plan Común","Logística","Recursos Humanos",
                      "Plan Común","Edificación","Terminaciones de la Construcción","Obras Viales e Infraestructura",
                      "Plan Común","Mantenimiento Electromecánico","Máquinas-Herramientas","Matricería",
                      "Plan Común","Planta Química","Laboratorio Químico",
                      "Plan Común","Cocina","Pastelería y Repostería",
                      "Adultos Mayores","Enfermería","Plan Común",
                      "Plan Común","Agricultura","Pecuaria","Vitivinícola")
  )
  
  # Tabla interactiva agregada por RBD y especialidad
  output$tabla_matricula <- renderDT({
    datos_visual() %>%
      group_by(rbd, nom_rbd, nom_reg_rbd_a, nom_com_rbd, nom_espe, cod_men) %>%
      summarise(
        Total = n(),
        Total_Hombres = sum(gen_alu == 1, na.rm = TRUE),
        Total_Mujeres = sum(gen_alu == 2, na.rm = TRUE),
        .groups = "drop"
      ) %>%
      left_join(menciones, by = "cod_men") %>%
      mutate(
        Glosa_Mencion = ifelse(is.na(Glosa_Mencion), "Sin Mención", Glosa_Mencion)
      ) %>%
      select(rbd, nom_rbd, nom_reg_rbd_a, nom_com_rbd, nom_espe, Glosa_Mencion, 
             Total, Total_Hombres, Total_Mujeres)
  }, 
  options = list(pageLength = 10, scrollX = TRUE),  # opciones de visualización
  filter = "top",  # filtrado por columna
  rownames = FALSE)
  
  # Descargar datos filtrados en csv
  output$descargar_csv <- downloadHandler(
    filename = function() {
      paste0("lista_liceos_filtrada_", Sys.Date(), ".csv")
    },
    content = function(file) {
      datos_a_descargar <- datos_visual() %>%
        group_by(rbd, nom_rbd, nom_reg_rbd_a, nom_com_rbd, nom_espe, cod_men, cod_ense2, cod_grado) %>%
        summarise(
          Total = n(),
          Total_Hombres = sum(gen_alu == 1, na.rm = TRUE),
          Total_Mujeres = sum(gen_alu == 2, na.rm = TRUE),
          .groups = "drop"
        ) %>%
        left_join(menciones, by = "cod_men") %>%
        mutate(
          Glosa_Mencion = ifelse(is.na(Glosa_Mencion), "Sin Mención", Glosa_Mencion),
          Nivel = case_when(
            cod_ense2 == 7 ~ "Niños y Jóvenes",
            cod_ense2 == 8 ~ "Adultos",
            TRUE ~ "Desconocido"
          ),
          Grado = case_when(
            cod_grado == 1 ~ "1° nivel (1° y 2° medio sólo adultos)",
            cod_grado == 3 ~ "3° medio",
            cod_grado == 4 ~ "4° medio",
            TRUE ~ as.character(cod_grado)
          )
        ) %>%
        select(rbd, nom_rbd, nom_reg_rbd_a, nom_com_rbd, nom_espe, Glosa_Mencion,
               Nivel, Grado, Total, Total_Hombres, Total_Mujeres)
      
      write.csv2(datos_a_descargar, file, row.names = FALSE, fileEncoding = "UTF-8")
    }
  )
  
  # Descargar matrícula en CSV (sin columnas de equipamiento)
  output$descargar_matricula_csv <- downloadHandler(
    filename = function() {
      paste0("20240913_Matricula_unica_2024_TP_", Sys.Date(), ".csv")
    },
    content = function(file) {
      # Excluir columnas de equipamiento
      matricula_descarga <- matricula_raw %>%
        select(-any_of(c("EquipamientoRegular_TOTAL", "EquipamientoRegular_2020",
                         "EquipamientoRegular_2021", "EquipamientoRegular_2022",
                         "EquipamientoRegular_2023", "EquipamientoRegular_2024",
                         "EquipamientoRegular_Adjudica", "EquipamientoSLEP_2023",
                         "EquipamientoSLEP_2024", "EquipamientoSLEP_TOTAL")))
      
      write.csv2(matricula_descarga, file, row.names = FALSE, fileEncoding = "UTF-8")
    }
  )
  
  # Descargar base de apoyo en CSV
  output$descargar_base_apoyo_csv <- downloadHandler(
    filename = function() {
      paste0("Base_EE_EMTP_2024_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write.csv2(base_apoyo, file, row.names = FALSE, fileEncoding = "UTF-8")
    }
  )
  
  output$descargar_docentes_emtp_csv <- downloadHandler(
    filename = function() {
      paste0("Base_docentes_2025_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write.csv2(docentes_raw, file, row.names = FALSE, fileEncoding = "UTF-8")
    }
  )
  
  # Download handler para minuta territorial
  output$descargar_resumen_territorial <- downloadHandler(
    filename = function() {
      nombre <- input$comuna
      if (nombre == "Todas") nombre <- "Territorio"
      paste0("Resumen_", nombre, "_", Sys.Date(), ".docx")
    },
    content = function(file) {
      notif_id <- "res_terr_word"
      showNotification("Generando reporte Word... Por favor espere.", type = "message", duration = NULL, id = notif_id)
      on.exit({ removeNotification(id = notif_id) }, add = TRUE)
      incluir_val <- isTRUE(input$incluir)
      
      nombre <- if (input$comuna != "Todas") {
        input$comuna
      } else if (input$provincia != "Todas") {
        input$provincia
      } else if (input$region != "Todas") {
        input$region
      } else if (input$rft != "Todas") {
        input$rft
      } else {
        "Territorio_Nacional"
      }
      
      territorio_filtrado <- datos_filtrados()$matricula
      rbd_filtrados <- unique(territorio_filtrado$rbd)
      
      # 1. Definir cod_ens_tp
      cod_ens_tp <- 410:863
      
      # 2. Preprocesar docentes_tp para todos los RBD filtrados
      docentes_tp <- docentes_raw %>%
        filter(
          rbd %in% rbd_filtrados &
            ((COD_ENS_1 %in% cod_ens_tp & HORAS1 > 0) |
               (COD_ENS_2 %in% cod_ens_tp & HORAS2 > 0))
        ) %>%
        mutate(
          SUBSECTOR1_mapped = ifelse(
            COD_ENS_1 %in% cod_ens_tp & HORAS1 > 0,
            ifelse(startsWith(as.character(SUBSECTOR1), "3"), "Formación General", as.character(SUBSECTOR1)),
            NA_character_
          ),
          SUBSECTOR2_mapped = ifelse(
            COD_ENS_2 %in% cod_ens_tp & HORAS2 > 0,
            ifelse(startsWith(as.character(SUBSECTOR2), "3"), "Formación General", as.character(SUBSECTOR2)),
            NA_character_
          )
        ) %>%
        tidyr::pivot_longer(
          cols = c(SUBSECTOR1_mapped, SUBSECTOR2_mapped),
          names_to = "Subsector_num",
          values_to = "Especialidad"
        ) %>%
        filter(!is.na(Especialidad))
      
      # Si queda vacío, crear tibble vacío para que el RMD no falle
      if(nrow(docentes_tp) == 0) docentes_tp <- tibble(Especialidad = character())
      
      # Filtrar base_apoyo solo con esos RBD
      base_apoyo_filtrada <- base_apoyo %>%
        filter(rbd %in% rbd_filtrados)
      
      suppressWarnings(rmarkdown::render(
        input = "templates/resumen_territorio.Rmd",
        output_file = file,
        quiet = TRUE,
        params = list(
          nombre_territorio = nombre,
          territorio_filtrado = territorio_filtrado,
          resumen_matricula = resumen_matricula(),
          detalle_especialidades = NULL,
          resumen_etnias = NULL,
          extranjeros = NULL,
          origen_extranjeros = NULL,
          rural_dependencia = NULL,
          base_apoyo = base_apoyo_filtrada,
          docentes_emtp = docentes_tp,
          resumen_subsector = docentes_tp,
          incluir_tabla = incluir_val
        ),
        envir = new.env(parent = globalenv())
      ))
    }
  )
  
  # Download handler para minuta territorial en PDF
  output$descargar_resumen_territorial_pdf <- downloadHandler(
    filename = function() {
      nombre <- input$comuna
      if (nombre == "Todas") nombre <- "Territorio"
      paste0("Resumen_", nombre, "_", Sys.Date(), ".pdf")
    },
    content = function(file) {
      notif_id <- "res_terr_pdf"
      showNotification("Generando reporte PDF... Por favor espere.", type = "message", duration = NULL, id = notif_id)
      on.exit({ removeNotification(id = notif_id) }, add = TRUE)
      incluir_val <- isTRUE(input$incluir)
      
      nombre <- if (input$comuna != "Todas") {
        input$comuna
      } else if (input$provincia != "Todas") {
        input$provincia
      } else if (input$region != "Todas") {
        input$region
      } else if (input$rft != "Todas") {
        input$rft
      } else {
        "Territorio_Nacional"
      }
      
      territorio_filtrado <- datos_filtrados()$matricula
      rbd_filtrados <- unique(territorio_filtrado$rbd)
      
      # Preprocesamiento docentes similar al DOCX
      cod_ens_tp <- 410:863
      docentes_tp <- docentes_raw %>%
        dplyr::filter(
          rbd %in% rbd_filtrados &
            ((COD_ENS_1 %in% cod_ens_tp & HORAS1 > 0) |
               (COD_ENS_2 %in% cod_ens_tp & HORAS2 > 0))
        ) %>%
        dplyr::mutate(
          SUBSECTOR1_mapped = dplyr::if_else(
            COD_ENS_1 %in% cod_ens_tp & HORAS1 > 0,
            dplyr::if_else(startsWith(as.character(SUBSECTOR1), "3"), "Formación General", as.character(SUBSECTOR1)),
            NA_character_
          ),
          SUBSECTOR2_mapped = dplyr::if_else(
            COD_ENS_2 %in% cod_ens_tp & HORAS2 > 0,
            dplyr::if_else(startsWith(as.character(SUBSECTOR2), "3"), "Formación General", as.character(SUBSECTOR2)),
            NA_character_
          )
        ) %>%
        tidyr::pivot_longer(
          cols = c(SUBSECTOR1_mapped, SUBSECTOR2_mapped),
          names_to = "Subsector_num",
          values_to = "Especialidad"
        ) %>%
        dplyr::filter(!is.na(Especialidad))
      if(nrow(docentes_tp) == 0) docentes_tp <- tibble::tibble(Especialidad = character())
      
      base_apoyo_filtrada <- base_apoyo %>% dplyr::filter(rbd %in% rbd_filtrados)
      
      # Renderizar a PDF cambiando el output_format (usar xelatex por soporte Unicode)
      suppressWarnings(rmarkdown::render(
        input = "templates/resumen_territorio.Rmd",
        output_file = file,
        output_format = rmarkdown::pdf_document(latex_engine = "xelatex"),
        quiet = TRUE,
        params = list(
          nombre_territorio = nombre,
          territorio_filtrado = territorio_filtrado,
          resumen_matricula = resumen_matricula(),
          detalle_especialidades = NULL,
          resumen_etnias = NULL,
          extranjeros = NULL,
          origen_extranjeros = NULL,
          rural_dependencia = NULL,
          base_apoyo = base_apoyo_filtrada,
          docentes_emtp = docentes_tp,
          resumen_subsector = docentes_tp,
          incluir_tabla = incluir_val
        ),
        envir = new.env(parent = globalenv())
      ))
    }
  )
  
  # Download handler para minutas por RBD
  output$descargar_minuta <- downloadHandler(
    filename = function() {
      paste0("minutas_establecimientos_", Sys.Date(), ".zip")
    },
    content = function(file) {
      notif_id <- "minuta_word"
      showNotification("Generando minutas Word... Por favor espere.", type = "message", duration = NULL, id = notif_id)
      on.exit({ removeNotification(id = notif_id) }, add = TRUE)
      resultados <- resultado_busqueda()
      if (nrow(resultados) == 0) {
        stop("No se encontró ningún RBD para generar minutas.")
      }
      rbd_lista <- rbd_seleccionados()
      if (length(rbd_lista) == 0) {
        stop("Seleccione al menos un establecimiento antes de descargar.")
      }
      
      # Pre-filtramos todos los datos necesarios una vez
      matricula_rbd_lista <- matricula_raw %>%
        filter(rbd %in% rbd_lista) %>%
        group_split(rbd) %>%
        setNames(map_chr(., ~ as.character(unique(.x$rbd))))
      
      # --- (Más adelante en tu código)
      # Supongamos que ya tienes creado el objeto `datos_establecimiento`
      # y ahora quieres agregar la información de equipamiento:
      datos_establecimiento <- matricula_raw
      
      temp_dir <- tempdir()
      archivos_generados <- c()
      
      for (rbd_seleccionado in rbd_lista) {
        
        matricula_actual <- matricula_rbd_lista[[as.character(rbd_seleccionado)]]
        
        datos_generales <- matricula_raw %>%
          filter(rbd == rbd_seleccionado) %>%
          select(rbd, nom_rbd, cod_depe2, rft, nom_reg_rbd_a, nom_deprov_rbd, nombre_sost, nom_com_rbd, RuralidadRBD) %>%
          distinct()
        
        datos_generales1 <- matricula_raw %>%
          filter(rbd == rbd_seleccionado) %>%
          select(rbd, nom_rbd, cod_depe2, rft, nom_reg_rbd_a, nom_deprov_rbd, nombre_sost, nom_com_rbd, RuralidadRBD, categoria_asis_anual)
        
        resumen_matricula <- matricula_actual %>%
          filter(rbd == rbd_seleccionado) %>%
          summarise(
            total = n(),
            hombres = sum(gen_alu == 1, na.rm = TRUE),
            mujeres = sum(gen_alu == 2, na.rm = TRUE),
            matricula_jovenes = sum(cod_ense2 == 7 & cod_grado %in% c(3, 4), na.rm = TRUE),
            matricula_adultos = sum(cod_ense2 == 8, na.rm = TRUE),
            matricula_adultos_1nivel = sum(cod_ense2 == 8 & cod_grado %in% c(1, 2), na.rm = TRUE),
            matricula_3medio = sum(cod_grado == 3, na.rm = TRUE),
            matricula_4medio = sum(cod_grado == 4, na.rm = TRUE)
          ) %>% as.list()
        
        detalle_por_nivel <- matricula_actual %>%
          filter(rbd == rbd_seleccionado) %>%
          group_by(cod_ense2, cod_grado) %>%
          summarise(
            total = n(),
            hombres = sum(gen_alu == 1, na.rm = TRUE),
            mujeres = sum(gen_alu == 2, na.rm = TRUE),
            .groups = "drop"
          ) %>%
          mutate(
            nivel = case_when(
              cod_ense2 == 7 ~ "Jóvenes",
              cod_ense2 == 8 ~ "Adultos",
              TRUE ~ "Otro"
            ),
            grado = cod_grado
          )
        
        detalle_especialidades <- matricula_actual %>%
          filter(rbd == rbd_seleccionado, !is.na(nom_espe)) %>%
          group_by(nom_espe) %>%
          summarise(
            Total = n(),
            Hombres = sum(gen_alu == 1, na.rm = TRUE),
            Mujeres = sum(gen_alu == 2, na.rm = TRUE),
            .groups = "drop"
          ) %>%
          mutate(
            `% Hombres` = round(100 * Hombres / Total, 1),
            `% Mujeres` = round(100 * Mujeres / Total, 1)
          ) %>%
          rename(`Especialidad` = nom_espe)       
        
        total_matricula_rbd <- resumen_matricula$total
        
        resumen_etnias <- matricula_actual %>%
          filter(rbd == rbd_seleccionado, !is.na(cod_etnia_alu)) %>%
          group_by(Etnia = cod_etnia_alu) %>%
          summarise(
            Total = n(),
            Porcentaje = round(100 * Total / total_matricula_rbd, 1),
            .groups = "drop"
          )
        
        extranjeros <- matricula_actual %>%
          filter(rbd == rbd_seleccionado) %>%
          group_by(Nacionalidad = case_when(
            cod_nac_alu == "E" ~ "Extranjero",
            cod_nac_alu == "N" ~ "Nacionalizado",
            cod_nac_alu == "C" ~ "Chileno",
            TRUE ~ "Desconocido"
          )) %>%
          summarise(
            Total = n(),
            Porcentaje = round(100 * Total / total_matricula_rbd, 1),
            .groups = "drop"
          )
        
        total_extranjeros <- matricula_actual %>%
          filter(rbd == rbd_seleccionado, cod_nac_alu == "E") %>%
          nrow()
        
        origen_extranjeros <- matricula_actual %>%
          filter(rbd == rbd_seleccionado, cod_nac_alu == "E") %>%
          mutate(pais_origen_alu = ifelse(pais_origen_alu == "Chile" | is.na(pais_origen_alu), "Desconocido", pais_origen_alu)) %>%
          group_by(País = pais_origen_alu) %>%
          summarise(Total = n(), .groups = "drop") %>%
          mutate(
            Porcentaje_extranjeros = round(100 * Total / sum(Total), 1),
            Porcentaje_total = round(100 * Total / total_matricula_rbd, 1)
          ) %>%
          arrange(desc(Total))
        
        embarazo <- matricula_actual %>%
          filter(rbd == rbd_seleccionado, gen_alu == 2) %>%  # SOLO MUJERES
          group_by(Embarazo = case_when(
            emb_alu == 1 ~ "Sí",
            emb_alu == 0 ~ "No",
            TRUE ~ "Desconocido"
          )) %>%
          summarise(
            Total = n(),
            .groups = "drop"
          ) %>%
          mutate(
            Porcentaje = ifelse(sum(Total) > 0,
                                round(100 * Total / sum(Total), 1),
                                NA_real_)
          )
        
        # Obtener nombre del establecimiento y limpiar caracteres especiales
        nombre_establecimiento <- datos_generales$nom_rbd[1] %>%
          stringr::str_replace_all("[^[:alnum:][:space:]]", "") %>%   # Quita caracteres raros
          stringr::str_replace_all("\\s+", "_") %>%                   # Reemplaza espacios por _
          stringr::str_sub(1, 40)                                     # Limita largo para evitar errores en archivos
        
        nombre_archivo <- file.path(temp_dir, paste0("minuta_", rbd_seleccionado, "_", nombre_establecimiento, "_", Sys.Date(), ".docx"))
        
        # Obtener los datos del establecimiento (incluye datos del concurso)
        # Obtener los datos del establecimiento (incluye datos del concurso Regular y SLEP)
        datos_establecimiento <- base_apoyo %>%
          filter(rbd == rbd_seleccionado)
        
        # Limpia los valores SLEP para evitar problemas de coerción a NA
        datos_establecimiento <- datos_establecimiento %>%
          mutate(
            EquipamientoSLEP_2023 = as.numeric(gsub("[^0-9]", "", EquipamientoSLEP_2023)),
            EquipamientoSLEP_2024 = as.numeric(gsub("[^0-9]", "", EquipamientoSLEP_2024)),
            EquipamientoSLEP_TOTAL = as.numeric(gsub("[^0-9]", "", EquipamientoSLEP_TOTAL))
          )
        
        if (nrow(datos_establecimiento) == 0) {
          warning(paste("No se encontraron datos para RBD:", rbd_seleccionado))
          next
        }
        
        datos_establecimiento_original <- datos_establecimiento
        
        datos_equipamiento <- datos_establecimiento %>%
          select(rbd, cod_depe2,
                 EquipamientoRegular_2020, EquipamientoRegular_2021,
                 EquipamientoRegular_2022, EquipamientoRegular_2023,
                 EquipamientoRegular_2024, EquipamientoRegular_TOTAL,
                 EquipamientoRegular_Adjudica,
                 EquipamientoSLEP_2023, EquipamientoSLEP_2024, EquipamientoSLEP_TOTAL)
        
        # Resumen de docentes por RBD
        datos_docentes <- docentes_raw %>%
          filter(rbd == rbd_seleccionado) %>%
          summarise(
            rbd = first(rbd),   # conserva la columna rbd
            Docentes_Total   = n(),
            Docentes_Hombres = sum(DOC_GENERO == 1, na.rm = TRUE),
            Docentes_Mujeres = sum(DOC_GENERO == 2, na.rm = TRUE)
          )
        
        # --- Paso 1: Preprocesar docentes para desagregación por especialidad ---
        cod_ens_tp <- 410:863
        map_subsector <- function(x) {
          if (is.na(x)) return(NA_character_)
          x_char <- as.character(x)
          if (startsWith(x_char, "3")) return("Formación General")
          return(x_char)
        }
        
        docentes_tp <- docentes_raw %>%
          filter(
            rbd == rbd_seleccionado &
              ((COD_ENS_1 %in% cod_ens_tp & HORAS1 > 0) |
                 (COD_ENS_2 %in% cod_ens_tp & HORAS2 > 0))
          ) %>%
          mutate(
            SUBSECTOR1_mapped = ifelse(
              COD_ENS_1 %in% cod_ens_tp & HORAS1 > 0,
              ifelse(startsWith(as.character(SUBSECTOR1), "3"), "Formación General", as.character(SUBSECTOR1)),
              NA_character_
            ),
            SUBSECTOR2_mapped = ifelse(
              COD_ENS_2 %in% cod_ens_tp & HORAS2 > 0,
              ifelse(startsWith(as.character(SUBSECTOR2), "3"), "Formación General", as.character(SUBSECTOR2)),
              NA_character_
            )
          ) %>%
          tidyr::pivot_longer(
            cols = c(SUBSECTOR1_mapped, SUBSECTOR2_mapped),
            names_to = "Subsector_num",
            values_to = "Especialidad"
          ) %>%
          filter(!is.na(Especialidad))
        
        # Luego lo agregas al establecimiento
        datos_establecimiento_docentes <- base_apoyo %>%
          filter(rbd == rbd_seleccionado) %>%
          left_join(datos_docentes, by = "rbd")
        
        # Luego pásalo como parámetro
        suppressWarnings(rmarkdown::render(
          input = "templates/minuta_establecimiento.Rmd",
          output_file = nombre_archivo,
          output_format = rmarkdown::word_document(reference_docx = "templates/plantilla_minuta.docx"),
          clean = TRUE,
          intermediates_dir = getwd(),
          quiet = TRUE,
          params = list(
            datos_generales = datos_generales,
            datos_generales1 = datos_generales1,
            resumen_matricula = resumen_matricula,
            detalle_especialidades = detalle_especialidades,
            resumen_etnias = resumen_etnias,
            extranjeros = extranjeros,
            embarazo = embarazo,
            origen_extranjeros = origen_extranjeros,
            datos_establecimiento = datos_establecimiento_docentes,
            datos_equipamiento = datos_equipamiento,
            detalle_por_nivel = detalle_por_nivel,
            datos_docentes       = datos_docentes,
            resumen_subsector = docentes_tp
          ),
          envir = new.env(parent = globalenv())
        ))
        
        archivos_generados <- c(archivos_generados, nombre_archivo)
      }
      
      # Crear ZIP
      zipfile <- file.path(temp_dir, paste0("minutas_", Sys.Date(), ".zip"))
      suppressWarnings(zip::zip(zipfile, files = archivos_generados, mode = "cherry-pick"))
      file.copy(zipfile, file)
    }
  )
  
  # Download handler para minutas por RBD en PDF (ZIP)
  output$descargar_minuta_pdf <- downloadHandler(
    filename = function() {
      paste0("minutas_establecimientos_pdf_", Sys.Date(), ".zip")
    },
    content = function(file) {
      notif_id <- "minuta_pdf"
      showNotification("Generando minutas PDF... Por favor espere.", type = "message", duration = NULL, id = notif_id)
      on.exit({ removeNotification(id = notif_id) }, add = TRUE)
      resultados <- resultado_busqueda()
      if (nrow(resultados) == 0) {
        stop("No se encontró ningún RBD para generar minutas.")
      }
      rbd_lista <- rbd_seleccionados()
      if (length(rbd_lista) == 0) {
        stop("Seleccione al menos un establecimiento antes de descargar.")
      }
      
      temp_dir <- tempdir()
      archivos_generados <- c()
      
      matricula_rbd_lista <- matricula_raw %>%
        dplyr::filter(rbd %in% rbd_lista) %>%
        dplyr::group_split(rbd) %>%
        setNames(purrr::map_chr(., ~ as.character(unique(.x$rbd))))
      
      for (rbd_seleccionado in rbd_lista) {
        matricula_actual <- matricula_rbd_lista[[as.character(rbd_seleccionado)]]
        
        datos_generales <- matricula_raw %>%
          dplyr::filter(rbd == rbd_seleccionado) %>%
          dplyr::select(rbd, nom_rbd, cod_depe2, rft, nom_reg_rbd_a, nom_deprov_rbd, nombre_sost, nom_com_rbd, RuralidadRBD) %>%
          dplyr::distinct()
        
        datos_generales1 <- matricula_raw %>%
          dplyr::filter(rbd == rbd_seleccionado) %>%
          dplyr::select(rbd, nom_rbd, cod_depe2, rft, nom_reg_rbd_a, nom_deprov_rbd, nombre_sost, nom_com_rbd, RuralidadRBD, categoria_asis_anual)
        
        resumen_matricula <- matricula_actual %>%
          dplyr::filter(rbd == rbd_seleccionado) %>%
          dplyr::summarise(
            total = dplyr::n(),
            hombres = sum(gen_alu == 1, na.rm = TRUE),
            mujeres = sum(gen_alu == 2, na.rm = TRUE),
            matricula_jovenes = sum(cod_ense2 == 7 & cod_grado %in% c(3, 4), na.rm = TRUE),
            matricula_adultos = sum(cod_ense2 == 8, na.rm = TRUE),
            matricula_adultos_1nivel = sum(cod_ense2 == 8 & cod_grado %in% c(1, 2), na.rm = TRUE),
            matricula_3medio = sum(cod_grado == 3, na.rm = TRUE),
            matricula_4medio = sum(cod_grado == 4, na.rm = TRUE)
          ) %>% as.list()
        
        detalle_por_nivel <- matricula_actual %>%
          dplyr::filter(rbd == rbd_seleccionado) %>%
          dplyr::group_by(cod_ense2, cod_grado) %>%
          dplyr::summarise(
            total = dplyr::n(),
            hombres = sum(gen_alu == 1, na.rm = TRUE),
            mujeres = sum(gen_alu == 2, na.rm = TRUE),
            .groups = "drop"
          ) %>%
          dplyr::mutate(
            nivel = dplyr::case_when(
              cod_ense2 == 7 ~ "Jóvenes",
              cod_ense2 == 8 ~ "Adultos",
              TRUE ~ "Otro"
            ),
            grado = cod_grado
          )
        
        detalle_especialidades <- matricula_actual %>%
          dplyr::filter(rbd == rbd_seleccionado, !is.na(nom_espe)) %>%
          dplyr::group_by(nom_espe) %>%
          dplyr::summarise(
            Total = dplyr::n(),
            Hombres = sum(gen_alu == 1, na.rm = TRUE),
            Mujeres = sum(gen_alu == 2, na.rm = TRUE),
            .groups = "drop"
          ) %>%
          dplyr::mutate(
            `% Hombres` = round(100 * Hombres / Total, 1),
            `% Mujeres` = round(100 * Mujeres / Total, 1)
          ) %>%
          dplyr::rename(`Especialidad` = nom_espe)
        
        total_matricula_rbd <- resumen_matricula$total
        
        resumen_etnias <- matricula_actual %>%
          dplyr::filter(rbd == rbd_seleccionado, !is.na(cod_etnia_alu)) %>%
          dplyr::group_by(Etnia = cod_etnia_alu) %>%
          dplyr::summarise(
            Total = dplyr::n(),
            Porcentaje = round(100 * Total / total_matricula_rbd, 1),
            .groups = "drop"
          )
        
        extranjeros <- matricula_actual %>%
          dplyr::filter(rbd == rbd_seleccionado) %>%
          dplyr::group_by(Nacionalidad = dplyr::case_when(
            cod_nac_alu == "E" ~ "Extranjero",
            cod_nac_alu == "N" ~ "Nacionalizado",
            cod_nac_alu == "C" ~ "Chileno",
            TRUE ~ "Desconocido"
          )) %>%
          dplyr::summarise(
            Total = dplyr::n(),
            .groups = "drop"
          ) %>%
          dplyr::mutate(
            Porcentaje = round(100 * Total / sum(Total), 1)
          )
        
        total_extranjeros <- matricula_actual %>%
          dplyr::filter(rbd == rbd_seleccionado, cod_nac_alu == "E") %>%
          nrow()
        
        origen_extranjeros <- matricula_actual %>%
          dplyr::filter(rbd == rbd_seleccionado, cod_nac_alu == "E") %>%
          dplyr::mutate(pais_origen_alu = ifelse(pais_origen_alu == "Chile" | is.na(pais_origen_alu), "Desconocido", pais_origen_alu)) %>%
          dplyr::group_by(País = pais_origen_alu) %>%
          dplyr::summarise(Total = dplyr::n(), .groups = "drop") %>%
          dplyr::mutate(
            Porcentaje_extranjeros = round(100 * Total / sum(Total), 1),
            Porcentaje_total = round(100 * Total / total_matricula_rbd, 1)
          ) %>%
          dplyr::arrange(dplyr::desc(Total))
        
        embarazo <- matricula_actual %>%
          dplyr::filter(rbd == rbd_seleccionado, gen_alu == 2) %>%
          dplyr::group_by(Embarazo = dplyr::case_when(
            emb_alu == 1 ~ "Sí",
            emb_alu == 0 ~ "No",
            TRUE ~ "Desconocido"
          )) %>%
          dplyr::summarise(
            Total = dplyr::n(),
            .groups = "drop"
          ) %>%
          dplyr::mutate(
            Porcentaje = ifelse(sum(Total) > 0,
                                round(100 * Total / sum(Total), 1),
                                NA_real_)
          )
        
        # Datos establecimiento y equipamiento
        datos_establecimiento <- base_apoyo %>% dplyr::filter(rbd == rbd_seleccionado)
        datos_establecimiento <- datos_establecimiento %>% dplyr::mutate(
          EquipamientoSLEP_2023 = as.numeric(gsub("[^0-9]", "", EquipamientoSLEP_2023)),
          EquipamientoSLEP_2024 = as.numeric(gsub("[^0-9]", "", EquipamientoSLEP_2024)),
          EquipamientoSLEP_TOTAL = as.numeric(gsub("[^0-9]", "", EquipamientoSLEP_TOTAL))
        )
        datos_equipamiento <- datos_establecimiento %>%
          dplyr::select(rbd, cod_depe2,
                        EquipamientoRegular_2020, EquipamientoRegular_2021,
                        EquipamientoRegular_2022, EquipamientoRegular_2023,
                        EquipamientoRegular_2024, EquipamientoRegular_TOTAL,
                        EquipamientoRegular_Adjudica,
                        EquipamientoSLEP_2023, EquipamientoSLEP_2024, EquipamientoSLEP_TOTAL)
        
        datos_docentes <- docentes_raw %>%
          dplyr::filter(rbd == rbd_seleccionado) %>%
          dplyr::summarise(
            rbd = dplyr::first(rbd),
            Docentes_Total   = dplyr::n(),
            Docentes_Hombres = sum(DOC_GENERO == 1, na.rm = TRUE),
            Docentes_Mujeres = sum(DOC_GENERO == 2, na.rm = TRUE)
          )
        
        # Construir resumen_subsector (docentes_tp) con columna "Especialidad" como en la versión DOCX
        cod_ens_tp <- 410:863
        docentes_tp <- docentes_raw %>%
          dplyr::filter(
            rbd == rbd_seleccionado &
              ((COD_ENS_1 %in% cod_ens_tp & HORAS1 > 0) |
                 (COD_ENS_2 %in% cod_ens_tp & HORAS2 > 0))
          ) %>%
          dplyr::mutate(
            SUBSECTOR1_mapped = dplyr::if_else(
              COD_ENS_1 %in% cod_ens_tp & HORAS1 > 0,
              dplyr::if_else(startsWith(as.character(SUBSECTOR1), "3"), "Formación General", as.character(SUBSECTOR1)),
              NA_character_
            ),
            SUBSECTOR2_mapped = dplyr::if_else(
              COD_ENS_2 %in% cod_ens_tp & HORAS2 > 0,
              dplyr::if_else(startsWith(as.character(SUBSECTOR2), "3"), "Formación General", as.character(SUBSECTOR2)),
              NA_character_
            )
          ) %>%
          tidyr::pivot_longer(
            cols = c(SUBSECTOR1_mapped, SUBSECTOR2_mapped),
            names_to = "Subsector_num",
            values_to = "Especialidad"
          ) %>%
          dplyr::filter(!is.na(Especialidad))
        
        # Render a PDF usando el Rmd existente cambiando el formato
        nombre_archivo_pdf <- file.path(temp_dir, paste0("minuta_", rbd_seleccionado, "_", stringr::str_sub(gsub("[^[:alnum:][:space:]]", "", datos_generales$nom_rbd[1]) %>% stringr::str_replace_all("\\s+", "_"), 1, 40), "_", Sys.Date(), ".pdf"))
        
        suppressWarnings(rmarkdown::render(
          input = "templates/minuta_establecimiento.Rmd",
          output_file = nombre_archivo_pdf,
          output_format = rmarkdown::pdf_document(latex_engine = "xelatex"),
          clean = TRUE,
          intermediates_dir = getwd(),
          params = list(
            datos_generales = datos_generales,
            datos_generales1 = datos_generales1,
            resumen_matricula = resumen_matricula,
            detalle_especialidades = detalle_especialidades,
            resumen_etnias = resumen_etnias,
            extranjeros = extranjeros,
            embarazo = embarazo,
            origen_extranjeros = origen_extranjeros,
            datos_establecimiento = datos_establecimiento,
            datos_equipamiento = datos_equipamiento,
            detalle_por_nivel = detalle_por_nivel,
            datos_docentes = datos_docentes,
            resumen_subsector = if (nrow(docentes_tp) > 0) docentes_tp else tibble::tibble(Especialidad = character())
          ),
          envir = new.env(parent = globalenv()),
          quiet = TRUE
        ))
        
        archivos_generados <- c(archivos_generados, nombre_archivo_pdf)
      }
      
      # Crear ZIP
      zipfile <- file.path(temp_dir, paste0("minutas_pdf_", Sys.Date(), ".zip"))
      suppressWarnings(zip::zip(zipfile, files = archivos_generados, mode = "cherry-pick"))
      file.copy(zipfile, file)
    }
  )
  
  resumen_matricula <- reactive({
    datos <- datos_filtrados()$matricula
    
    total <- nrow(datos)
    hombres <- sum(datos$gen_alu == 1, na.rm = TRUE)
    mujeres <- sum(datos$gen_alu == 2, na.rm = TRUE)
    
    # Por tipo de enseñanza
    jovenes_3_4 <- datos %>% filter(cod_ense2 == 7, cod_grado %in% c(3, 4)) %>% nrow()
    jovenes_1_2 <- datos %>% filter(cod_ense2 == 7, cod_grado %in% c(1, 2)) %>% nrow()
    adultos_total <- datos %>% filter(cod_ense2 == 8) %>% nrow()
    adultos_1nivel <- datos %>% filter(cod_ense2 == 8, cod_grado %in% c(1, 2)) %>% nrow()
    adultos_3_4 <- datos %>% filter(cod_ense2 == 8, cod_grado %in% c(3, 4)) %>% nrow()
    
    # Desglose detallado por tipo, grado y género
    # Jóvenes por grado y género
    jovenes_h_1_2 <- datos %>% filter(cod_ense2 == 7, cod_grado %in% c(1, 2), gen_alu == 1) %>% nrow()
    jovenes_m_1_2 <- datos %>% filter(cod_ense2 == 7, cod_grado %in% c(1, 2), gen_alu == 2) %>% nrow()
    jovenes_h_3 <- datos %>% filter(cod_ense2 == 7, cod_grado == 3, gen_alu == 1) %>% nrow()
    jovenes_m_3 <- datos %>% filter(cod_ense2 == 7, cod_grado == 3, gen_alu == 2) %>% nrow()
    jovenes_h_4 <- datos %>% filter(cod_ense2 == 7, cod_grado == 4, gen_alu == 1) %>% nrow()
    jovenes_m_4 <- datos %>% filter(cod_ense2 == 7, cod_grado == 4, gen_alu == 2) %>% nrow()
    
    # Adultos por grado y género
    adultos_h_1_2 <- datos %>% filter(cod_ense2 == 8, cod_grado %in% c(1, 2), gen_alu == 1) %>% nrow()
    adultos_m_1_2 <- datos %>% filter(cod_ense2 == 8, cod_grado %in% c(1, 2), gen_alu == 2) %>% nrow()
    adultos_h_3 <- datos %>% filter(cod_ense2 == 8, cod_grado == 3, gen_alu == 1) %>% nrow()
    adultos_m_3 <- datos %>% filter(cod_ense2 == 8, cod_grado == 3, gen_alu == 2) %>% nrow()
    adultos_h_4 <- datos %>% filter(cod_ense2 == 8, cod_grado == 4, gen_alu == 1) %>% nrow()
    adultos_m_4 <- datos %>% filter(cod_ense2 == 8, cod_grado == 4, gen_alu == 2) %>% nrow()
    
    # Por grados (totales)
    tercero_medio <- datos %>% filter(cod_grado == 3) %>% nrow()
    cuarto_medio <- datos %>% filter(cod_grado == 4) %>% nrow()
    primer_nivel <- datos %>% filter(cod_grado %in% c(1, 2)) %>% nrow()
    
    data.frame(
      Categoría = c(
        "🎯 RESUMEN GENERAL",
        "Total Matrícula",
        "Matrícula Hombres", 
        "Matrícula Mujeres",
        "",
        "👥 POR TIPO DE ENSEÑANZA",
        "Jóvenes - 1° y 2° Nivel",
        "Jóvenes - 3° y 4° Medio", 
        "Adultos - Total",
        "Adultos - 1° Nivel",
        "Adultos - 3° y 4° Medio",
        "",
        "📚 DESGLOSE DETALLADO POR GRADO Y GÉNERO",
        "--- JÓVENES ---",
        "Jóvenes Hombres - 1° y 2° Nivel",
        "Jóvenes Mujeres - 1° y 2° Nivel",
        "Jóvenes Hombres - 3° Medio",
        "Jóvenes Mujeres - 3° Medio",
        "Jóvenes Hombres - 4° Medio",
        "Jóvenes Mujeres - 4° Medio",
        "",
        "--- ADULTOS ---",
        "Adultos Hombres - 1° Nivel",
        "Adultos Mujeres - 1° Nivel",
        "Adultos Hombres - 3° Medio",
        "Adultos Mujeres - 3° Medio",
        "Adultos Hombres - 4° Medio",
        "Adultos Mujeres - 4° Medio",
        "",
        "📊 TOTALES POR GRADO",
        "Total 1° Nivel",
        "Total 3° Medio",
        "Total 4° Medio"
      ),
      Valor = c(
        "",
        format(total, big.mark = "."),
        format(hombres, big.mark = "."),
        format(mujeres, big.mark = "."),
        "",
        "",
        format(jovenes_1_2, big.mark = "."),
        format(jovenes_3_4, big.mark = "."),
        format(adultos_total, big.mark = "."),
        format(adultos_1nivel, big.mark = "."),
        format(adultos_3_4, big.mark = "."),
        "",
        "",
        "",
        format(jovenes_h_1_2, big.mark = "."),
        format(jovenes_m_1_2, big.mark = "."),
        format(jovenes_h_3, big.mark = "."),
        format(jovenes_m_3, big.mark = "."),
        format(jovenes_h_4, big.mark = "."),
        format(jovenes_m_4, big.mark = "."),
        "",
        "",
        format(adultos_h_1_2, big.mark = "."),
        format(adultos_m_1_2, big.mark = "."),
        format(adultos_h_3, big.mark = "."),
        format(adultos_m_3, big.mark = "."),
        format(adultos_h_4, big.mark = "."),
        format(adultos_m_4, big.mark = "."),
        "",
        "",
        format(primer_nivel, big.mark = "."),
        format(tercero_medio, big.mark = "."),
        format(cuarto_medio, big.mark = ".")
      ),
      check.names = FALSE
    )
  })
  
  # --- Renderiza la tabla resumen con mejor formato y diseño mejorado
  output$resumen_matricula <- renderUI({
    tabla <- resumen_matricula()
    
    # Dividir la tabla en secciones para mejor presentación
    secciones <- split(tabla, cumsum(startsWith(tabla$Categoría, "🎯") | 
                                       startsWith(tabla$Categoría, "👥") | 
                                       startsWith(tabla$Categoría, "📚") | 
                                       startsWith(tabla$Categoría, "📊")))
    
    # Función para crear cada sección
    crear_seccion <- function(seccion_data) {
      if(nrow(seccion_data) == 0) return(NULL)
      
      # Título de la sección (primera fila)
      titulo <- seccion_data[1, ]
      contenido <- seccion_data[-1, ]
      
      # Crear contenido de la sección con lógica especial para jóvenes/adultos
      filas_contenido <- lapply(1:nrow(contenido), function(i) {
        fila <- contenido[i, ]
        if(fila$Categoría == "") {
          return(NULL)
        }
        
        # Detectar separadores de jóvenes/adultos
        if(startsWith(fila$Categoría, "--- JÓVENES ---")) {
          return(tags$div(
            style = "background: linear-gradient(135deg, #2ECC71, #27AE60); color: white; padding: 10px 15px; margin: 10px 0; border-radius: 6px; font-weight: bold; text-align: center; font-size: 14px;",
            tags$i(class = "fas fa-graduation-cap", style = "margin-right: 8px;"),
            "EDUCACIÓN DE JÓVENES"
          ))
        }
        
        if(startsWith(fila$Categoría, "--- ADULTOS ---")) {
          return(tags$div(
            style = "background: linear-gradient(135deg, #E67E22, #D35400); color: white; padding: 10px 15px; margin: 10px 0; border-radius: 6px; font-weight: bold; text-align: center; font-size: 14px;",
            tags$i(class = "fas fa-user-graduate", style = "margin-right: 8px;"),
            "EDUCACIÓN DE ADULTOS"
          ))
        }
        
        # Filas normales de datos
        tags$div(
          style = "display: flex; justify-content: space-between; padding: 8px 12px; border-bottom: 1px solid #e9ecef; transition: background-color 0.2s;",
          `onmouseover` = "this.style.backgroundColor='#f8f9fa'",
          `onmouseout` = "this.style.backgroundColor='white'",
          tags$span(fila$Categoría, style = "font-weight: 500; color: #495057;"),
          tags$span(fila$Valor, style = "font-weight: bold; color: #2C3E50;")
        )
      })
      
      # Eliminar elementos NULL
      filas_contenido <- filas_contenido[!sapply(filas_contenido, is.null)]
      
      if(length(filas_contenido) == 0) return(NULL)
      
      # Retornar la sección completa
      tags$div(
        style = "margin-bottom: 25px; background: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); overflow: hidden;",
        
        # Encabezado de la sección
        tags$div(
          style = "background: linear-gradient(135deg, #34536A, #2A4255); color: white; padding: 12px 15px; font-weight: bold; font-size: 16px;",
          titulo$Categoría
        ),
        
        # Contenido de la sección
        tags$div(
          style = "border: 1px solid #dee2e6;",
          filas_contenido
        )
      )
    }
    
    # Crear todas las secciones
    secciones_ui <- lapply(secciones, crear_seccion)
    secciones_ui <- secciones_ui[!sapply(secciones_ui, is.null)]
    
    # Organizar en columnas para aprovechar el espacio horizontal
    if(length(secciones_ui) >= 2) {
      primera_mitad <- secciones_ui[1:ceiling(length(secciones_ui)/2)]
      segunda_mitad <- secciones_ui[(ceiling(length(secciones_ui)/2)+1):length(secciones_ui)]
      
      tags$div(
        style = "width: 100%;",
        fluidRow(
          column(6, primera_mitad),
          column(6, segunda_mitad)
        )
      )
    } else {
      tags$div(
        style = "width: 100%; max-width: 800px; margin: 0 auto;",
        secciones_ui
      )
    }
  })
  
  # Mejorar el renderLeaflet
  output$mapa_matricula <- renderLeaflet({
    datos <- datos_filtrados()
    
    # Crear popups más informativos con iconos
    popups <- paste0(
      "<div style='font-family: Roboto; font-size: 13px; min-width: 200px;'>",
      "<h4 style='margin: 0 0 10px 0; color: #2C3E50;'>📍 ", datos$comunas$Comuna, "</h4>",
      "<hr style='margin: 5px 0;'>",
      "<p><strong>🗺️ Región:</strong> ", datos$comunas$Region, "</p>",
      "<p><strong>👥 Matrícula Total:</strong> ", 
      format(ifelse(is.na(datos$comunas$matricula), 0, datos$comunas$matricula), big.mark = "."), "</p>",
      "<p><strong>👨‍🎓 Hombres:</strong> ", 
      format(ifelse(is.na(datos$comunas$matricula_hombres), 0, datos$comunas$matricula_hombres), big.mark = "."), "</p>",
      "<p><strong>👩‍🎓 Mujeres:</strong> ", 
      format(ifelse(is.na(datos$comunas$matricula_mujeres), 0, datos$comunas$matricula_mujeres), big.mark = "."), "</p>",
      "<p><strong>🏫 Establecimientos:</strong> ", 
      format(ifelse(is.na(datos$comunas$n_establecimientos), 0, datos$comunas$n_establecimientos), big.mark = "."), "</p>",
      "</div>"
    )
    
    # Crear el mapa base
    mapa <- leaflet() %>%
      addTiles() %>%
      addPolygons(
        data = datos$comunas,
        fillColor = ~fill_color_final,
        fillOpacity = ~fill_opacity,
        color = "white",
        weight = 1,
        popup = popups,
        highlight = highlightOptions(
          weight = 3,
          color = "#2C3E50",
          fillOpacity = 0.8,
          bringToFront = TRUE
        )
      ) %>%
      addLegend(
        position = "bottomright",
        title = "Matrícula EMTP por Comuna",
        labels = c("Sin datos", "Con datos"),
        colors = c("#BBBBBB", "#34536A"),
        opacity = 0.8
      )
    
    # Aplicar zoom automático a las comunas con datos filtrados
    comunas_con_datos <- datos$comunas %>% filter(!is.na(matricula) & matricula > 0)
    
    if (nrow(comunas_con_datos) > 0) {
      # Verificar que hay geometría válida
      if (!is.null(comunas_con_datos$geometry) && any(!st_is_empty(comunas_con_datos))) {
        # Calcular el bounding box de las comunas con datos
        bbox <- st_bbox(comunas_con_datos)
        
        # Agregar fitBounds para hacer zoom automático con un margen
        mapa <- mapa %>%
          fitBounds(
            lng1 = bbox[["xmin"]] - 0.1, lat1 = bbox[["ymin"]] - 0.1,
            lng2 = bbox[["xmax"]] + 0.1, lat2 = bbox[["ymax"]] + 0.1
          )
      }
    }
    
    mapa
  })
  
  # ---------------------------------------------------------------------------
  # Tabla seleccionable de establecimientos (Buscador)
  # ---------------------------------------------------------------------------
  output$tabla_establecimientos <- DT::renderDataTable({
    req(input$buscar)
    resultado_busqueda()
  }, selection = list(mode = 'multiple', target = 'row'), options = list(
    pageLength = 15,
    scrollX = TRUE,
    language = list(
      search = "Buscar:",
      lengthMenu = "Mostrar _MENU_ registros por página",
      zeroRecords = "No se encontraron registros",
      info = "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty = "Mostrando 0 a 0 de 0 registros",
      infoFiltered = "(filtrado de _MAX_ registros totales)",
      paginate = list(
        first = "Primero",
        previous = "Anterior",
        `next` = "Siguiente",
        last = "Último"
      )
    )
  ))
  
  proxy_tabla_est <- DT::dataTableProxy("tabla_establecimientos")
  
  # Seleccionar todas las filas tras nueva búsqueda
  observeEvent(resultado_busqueda(), {
    dat <- resultado_busqueda()
    if (nrow(dat) > 0) {
      DT::selectRows(proxy_tabla_est, 1:nrow(dat))
    }
  })
  
  observeEvent(input$seleccionar_todos_est, {
    dat <- resultado_busqueda()
    if (nrow(dat) > 0) DT::selectRows(proxy_tabla_est, 1:nrow(dat))
  })
  observeEvent(input$deseleccionar_todos_est, {
    DT::selectRows(proxy_tabla_est, NULL)
  })
  
  `%||%` <- function(a, b) if (is.null(a)) b else a
  output$contador_seleccion <- renderText({
    total <- tryCatch(nrow(resultado_busqueda()), error = function(e) 0)
    sel <- length(input$tabla_establecimientos_rows_selected %||% integer())
    if (total == 0) return("0 seleccionados")
    paste0(sel, " seleccionados de ", total)
  })
  
  rbd_seleccionados <- reactive({
    dat <- resultado_busqueda()
    idx <- input$tabla_establecimientos_rows_selected
    if (is.null(idx) || length(idx) == 0) return(dat$rbd) # fallback a todos
    dat$rbd[idx]
  })
  
  resultado_busqueda <- eventReactive(input$buscar, {
    datos <- matricula_raw
    
    # Aplicar filtros (ya están bien)
    if (input$rft_busqueda != "Todas") {
      datos <- datos %>% filter(rft == input$rft_busqueda)
    }
    if (input$region_busqueda != "Todas") {
      datos <- datos %>% filter(nom_reg_rbd_a == input$region_busqueda)
    }
    if (input$provincia_busqueda != "Todas") {
      datos <- datos %>% filter(nom_deprov_rbd == input$provincia_busqueda)
    }
    if (input$comuna_busqueda != "Todas") {
      datos <- datos %>% filter(nom_com_rbd == input$comuna_busqueda)
    }
    
    # Filtro por especialidad in los datos
    if (!is.null(input$especialidad_busqueda) && length(input$especialidad_busqueda) > 0) {
      datos <- datos %>% filter(nom_espe %in% input$especialidad_busqueda)
    }
    
    if (input$rbd_busqueda != "") {
      rbd_input <- str_split(input$rbd_busqueda, ",")[[1]] %>%
        str_trim() %>%
        discard(~ .x == "") %>%
        as.character()
      datos <- datos %>% filter(rbd %in% rbd_input)
    }
    if (input$nombre_busqueda != "") {
      datos <- datos %>% filter(str_detect(str_to_lower(nom_rbd), str_to_lower(input$nombre_busqueda)))
    }
    if (input$dependencia_busqueda != "Todas") {
      datos <- datos %>% filter(cod_depe2 == input$dependencia_busqueda)
    }
    if (input$sostenedor_busqueda != "Todos") {
      datos <- datos %>% filter(nombre_sost == input$sostenedor_busqueda)
    }
    
    # Agrupar y mantener rbd
    datos %>%
      group_by(rbd, nom_rbd, nom_com_rbd, nom_deprov_rbd, nom_reg_rbd_a, cod_depe2) %>%
      summarise(
        especialidades = str_c(unique(na.omit(nom_espe)), collapse = ", "),
        .groups = "drop"
      ) %>%
      arrange(nom_rbd)
  })
  
  # ===========================================================================
  # OUTPUTS PARA BUSCADOR AVANZADO
  # ===========================================================================
  
  # (Eliminado output$tabla_establecimientos_dt redundante)
  
  # ===========================================================================
  # OUTPUTS PARA ANÁLISIS VISUAL
  # ===========================================================================
  
  # Métricas del análisis visual
  output$total_matricula <- renderText({
    format(nrow(datos_visual()), big.mark = ".")
  })
  
  output$total_hombres <- renderText({
    format(sum(datos_visual()$gen_alu == 1, na.rm = TRUE), big.mark = ".")
  })
  
  output$total_mujeres <- renderText({
    format(sum(datos_visual()$gen_alu == 2, na.rm = TRUE), big.mark = ".")
  })
  
  output$pct_hombres <- renderText({
    total <- nrow(datos_visual())
    if (total == 0) return("0%")
    hombres <- sum(datos_visual()$gen_alu == 1, na.rm = TRUE)
    paste0(round(hombres / total * 100, 1), "%")
  })
  
  output$pct_mujeres <- renderText({
    total <- nrow(datos_visual())
    if (total == 0) return("0%")
    mujeres <- sum(datos_visual()$gen_alu == 2, na.rm = TRUE)
    paste0(round(mujeres / total * 100, 1), "%")
  })
  
  output$total_establecimientos <- renderText({
    format(n_distinct(datos_visual()$rbd), big.mark = ".")
  })
  
  # Gráfico principal del análisis visual
  output$grafico_principal <- renderPlotly({
    datos <- datos_visual()
    
    if (nrow(datos) == 0) {
      p <- plot_ly() %>%
        add_text(x = 0.5, y = 0.5, text = "No hay datos para mostrar", textsize = 16) %>%
        layout(
          title = "Sin datos disponibles",
          xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
          yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE)
        )
      return(p)
    }
    
    if (input$tipo_grafico == "barras_especialidad") {
      # Gráfico de barras por especialidad
      datos_barras <- datos %>%
        group_by(nom_espe, gen_alu) %>%
        summarise(Total = n(), .groups = "drop") %>%
        pivot_wider(names_from = gen_alu, values_from = Total, values_fill = 0) %>%
        mutate(
          Hombres = `1`,
          Mujeres = `2`,
          Total_est = Hombres + Mujeres,
          pct_Hombres = ifelse(Total_est > 0, Hombres / Total_est * 100, 0),
          pct_Mujeres = ifelse(Total_est > 0, Mujeres / Total_est * 100, 0)
        ) %>%
        arrange(pct_Mujeres) %>% 
        mutate(nom_espe = factor(nom_espe, levels = nom_espe))
      
      p <- plot_ly(
        datos_barras,
        x = ~nom_espe,
        y = ~pct_Hombres,
        type = 'bar',
        name = 'Hombres',
        marker = list(color = "#3B5268"),
        hovertemplate = paste(
          "<b>%{x}</b><br>",
          "Hombres: %{y:.1f}%<br>",
          "<extra></extra>"
        )
      ) %>%
        add_trace(
          y = ~pct_Mujeres, 
          name = 'Mujeres', 
          marker = list(color = "#A75F5D"),
          hovertemplate = paste(
            "<b>%{x}</b><br>",
            "Mujeres: %{y:.1f}%<br>",
            "<extra></extra>"
          )
        ) %>%
        layout(
          title = "Distribución por Género en Especialidades EMTP",
          barmode = 'stack',
          margin = list(b = 150),
          xaxis = list(title = "Especialidad", tickangle = -45),
          yaxis = list(title = "Porcentaje de Estudiantes")
        )
      
    } else if (input$tipo_grafico == "distribucion_genero") {
      # Gráfico circular de distribución por género
      datos_genero <- datos %>%
        group_by(gen_alu) %>%
        summarise(Total = n(), .groups = "drop") %>%
        mutate(
          Género = case_when(
            gen_alu == 1 ~ "Hombres",
            gen_alu == 2 ~ "Mujeres",
            TRUE ~ "No especificado"
          ),
          Porcentaje = round(Total / sum(Total) * 100, 1)
        )
      
      datos_genero <- datos_genero %>%
        mutate(color = dplyr::case_when(
          Género == "Hombres" ~ "#3B5268",
          Género == "Mujeres" ~ "#A75F5D",
          TRUE ~ "#7F8C8D"
        ))
      p <- plot_ly(
        datos_genero,
        labels = ~Género,
        values = ~Total,
        type = 'pie',
        textposition = 'inside',
        textinfo = 'label+percent',
        marker = list(colors = datos_genero$color),
        hovertemplate = paste(
          "<b>%{label}</b><br>",
          "Total: %{value:,}<br>",
          "Porcentaje: %{percent}<br>",
          "<extra></extra>"
        )
      ) %>%
        layout(title = "Distribución de Matrícula por Género")
      
    } else if (input$tipo_grafico == "matricula_region") {
      # Gráfico de barras por región
      datos_region <- datos %>%
        group_by(nom_reg_rbd_a) %>%
        summarise(Total = n(), .groups = "drop") %>%
        arrange(desc(Total)) %>%
        slice_head(n = 15)  # Top 15 regiones
      
      p <- plot_ly(
        datos_region,
        x = ~reorder(nom_reg_rbd_a, Total),
        y = ~Total,
        type = 'bar',
        marker = list(color = "#5A6E79"),
        hovertemplate = paste(
          "<b>%{x}</b><br>",
          "Matrícula: %{y:,}<br>",
          "<extra></extra>"
        )
      ) %>%
        layout(
          title = "Matrícula EMTP por Región (Top 15)",
          xaxis = list(title = "Región"),
          yaxis = list(title = "Número de Estudiantes"),
          margin = list(b = 100)
        )
      
    } else if (input$tipo_grafico == "dependencia_matricula") {
      # Gráfico de barras por dependencia
      datos_dep <- datos %>%
        group_by(cod_depe2) %>%
        summarise(Total = n(), .groups = "drop") %>%
        arrange(desc(Total))
      
      p <- plot_ly(
        datos_dep,
        x = ~reorder(cod_depe2, Total),
        y = ~Total,
        type = 'bar',
        marker = list(color = "#6E5F80"),
        hovertemplate = paste(
          "<b>%{x}</b><br>",
          "Matrícula: %{y:,}<br>",
          "<extra></extra>"
        )
      ) %>%
        layout(
          title = "Matrícula EMTP por Dependencia",
          xaxis = list(title = "Dependencia"),
          yaxis = list(title = "Número de Estudiantes")
        )
    }
    
    return(p)
  })
}

# Iniciar la aplicación
shinyApp(ui = ui, server = server)

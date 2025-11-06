"""
Script para generar datos comunales simulados a partir de datos regionales.
Distribuye la matrícula regional entre las comunas usando el shapefile oficial.
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).parent.parent
SHAPEFILE_PATH = BASE_DIR / "Comunas" / "comunas.shp"
REGIONAL_DATA_PATH = BASE_DIR / "data" / "processed" / "matricula_simulada.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "matricula_comunal_simulada.csv"

# Semilla para reproducibilidad
np.random.seed(42)

def load_comunas_data():
    """Cargar datos del shapefile de comunas"""
    print("📍 Cargando shapefile de comunas...")
    gdf = gpd.read_file(SHAPEFILE_PATH)
    
    # Filtrar "Zona sin demarcar" (codregion = 0)
    gdf = gdf[gdf['codregion'] != 0].copy()
    
    # Renombrar para consistencia
    comunas_df = gdf[['codregion', 'Region', 'cod_comuna', 'Comuna']].copy()
    comunas_df.columns = ['codregion', 'region', 'cod_comuna', 'comuna']
    
    print(f"   ✓ {len(comunas_df)} comunas en {comunas_df['codregion'].nunique()} regiones")
    return comunas_df

def load_regional_data():
    """Cargar datos regionales existentes"""
    print("📊 Cargando datos regionales...")
    df = pd.read_csv(REGIONAL_DATA_PATH)
    print(f"   ✓ {len(df)} registros regionales")
    return df

def create_comunal_data(regional_df, comunas_df):
    """
    Generar datos comunales distribuyendo la matrícula regional entre comunas.
    
    Estrategia:
    - Cada región tiene N comunas
    - La matrícula regional se distribuye entre comunas usando pesos aleatorios
    - Las comunas grandes reciben más matrícula
    - Se mantiene la suma regional
    """
    print("🔄 Generando datos comunales...")
    
    # Mapeo de nombres de región (datos vs shapefile)
    region_mapping = {
        'Arica y Parinacota': 'Región de Arica y Parinacota',
        'Tarapacá': 'Región de Tarapacá',
        'Antofagasta': 'Región de Antofagasta',
        'Atacama': 'Región de Atacama',
        'Coquimbo': 'Región de Coquimbo',
        'Valparaíso': 'Región de Valparaíso',
        "O'Higgins": "Región del Libertador Bernardo O'Higgins",
        'Maule': 'Región del Maule',
        'Biobío': 'Región del Bío-Bío',
        'Araucanía': 'Región de La Araucanía',
        'La Araucanía': 'Región de La Araucanía',  # Variante del nombre
        'Los Lagos': 'Región de Los Lagos',
        'Aysén': "Región de Aysén del Gral.Ibañez del Campo",
        'Magallanes': 'Región de Magallanes y Antártica Chilena',
        'Metropolitana': 'Región Metropolitana de Santiago',
        'Los Ríos': 'Región de Los Ríos',
        'Ñuble': 'Región de Ñuble'
    }
    
    # Invertir el mapeo (shapefile -> datos)
    inverse_mapping = {v: k for k, v in region_mapping.items()}
    
    # Agregar columna con nombre estandarizado a comunas
    comunas_df['region_original'] = comunas_df['region']
    comunas_df['region'] = comunas_df['region'].map(inverse_mapping)
    
    # Verificar que todas las regiones tienen mapeo
    missing = comunas_df[comunas_df['region'].isna()]
    if len(missing) > 0:
        print(f"⚠️  Regiones sin mapeo: {missing['region_original'].unique()}")
    
    all_comunal_data = []
    
    # Por cada combinación de año, región, especialidad, dependencia
    grouped = regional_df.groupby(['año', 'region', 'especialidad', 'dependencia'])
    
    for (año, region, especialidad, dependencia), group in grouped:
        # Obtener comunas de esta región
        region_comunas = comunas_df[comunas_df['region'] == region].copy()
        
        if len(region_comunas) == 0:
            print(f"⚠️  Sin comunas para región: {region}")
            continue
        
        n_comunas = len(region_comunas)
        
        # Datos regionales
        matricula_total = group['matricula_total'].iloc[0]
        matricula_hombres = group['matricula_hombres'].iloc[0]
        matricula_mujeres = group['matricula_mujeres'].iloc[0]
        tasa_retencion = group['tasa_retencion'].iloc[0]
        
        # Generar pesos aleatorios para distribución (más realista)
        # Algunas comunas son más grandes que otras
        weights = np.random.lognormal(mean=0, sigma=0.8, size=n_comunas)
        weights = weights / weights.sum()  # Normalizar
        
        # Distribuir matrícula entre comunas
        matriculas_comunales = np.round(matricula_total * weights).astype(int)
        
        # Ajustar para que la suma sea exacta
        diff = matricula_total - matriculas_comunales.sum()
        if diff != 0:
            # Ajustar en la comuna más grande
            idx_max = np.argmax(matriculas_comunales)
            matriculas_comunales[idx_max] += diff
        
        # Distribuir por género (proporcional)
        prop_hombres = matricula_hombres / matricula_total if matricula_total > 0 else 0.5
        matriculas_hombres = np.round(matriculas_comunales * prop_hombres).astype(int)
        matriculas_mujeres = matriculas_comunales - matriculas_hombres
        
        # Variación en tasa de retención por comuna (±5%)
        tasas_retencion = np.clip(
            tasa_retencion + np.random.normal(0, 0.05, n_comunas),
            0.5, 1.0
        )
        
        # Crear registros comunales
        for i, (_, comuna_row) in enumerate(region_comunas.iterrows()):
            comunal_record = {
                'año': año,
                'region': region,
                'comuna': comuna_row['comuna'],
                'cod_comuna': comuna_row['cod_comuna'],
                'especialidad': especialidad,
                'dependencia': dependencia,
                'matricula_total': int(matriculas_comunales[i]),
                'matricula_hombres': int(matriculas_hombres[i]),
                'matricula_mujeres': int(matriculas_mujeres[i]),
                'tasa_retencion': round(tasas_retencion[i], 4)
            }
            all_comunal_data.append(comunal_record)
    
    # Crear DataFrame
    comunal_df = pd.DataFrame(all_comunal_data)
    
    # Filtrar registros con matrícula 0 (por la distribución pueden quedar algunos)
    comunal_df = comunal_df[comunal_df['matricula_total'] > 0].copy()
    
    print(f"   ✓ {len(comunal_df)} registros comunales generados")
    
    return comunal_df

def validate_data(regional_df, comunal_df):
    """Validar que los datos comunales suman correctamente a nivel regional"""
    print("✓ Validando consistencia de datos...")
    
    # Agrupar datos comunales por región
    comunal_agg = comunal_df.groupby(['año', 'region', 'especialidad', 'dependencia']).agg({
        'matricula_total': 'sum',
        'matricula_hombres': 'sum',
        'matricula_mujeres': 'sum'
    }).reset_index()
    
    # Merge con datos regionales
    comparison = regional_df.merge(
        comunal_agg,
        on=['año', 'region', 'especialidad', 'dependencia'],
        suffixes=('_regional', '_comunal')
    )
    
    # Calcular diferencias
    comparison['diff_total'] = comparison['matricula_total_regional'] - comparison['matricula_total_comunal']
    comparison['diff_hombres'] = comparison['matricula_hombres_regional'] - comparison['matricula_hombres_comunal']
    comparison['diff_mujeres'] = comparison['matricula_mujeres_regional'] - comparison['matricula_mujeres_comunal']
    
    max_diff = comparison['diff_total'].abs().max()
    print(f"   Diferencia máxima en matrícula total: {max_diff}")
    
    if max_diff > 5:  # Tolerancia de ±5 estudiantes por redondeo
        print("   ⚠️  Hay diferencias significativas en algunos grupos")
        problematic = comparison[comparison['diff_total'].abs() > 5]
        print(f"   Registros problemáticos: {len(problematic)}")
    else:
        print("   ✅ Datos consistentes (diferencias menores a ±5)")
    
    return comparison

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🏫 GENERADOR DE DATOS COMUNALES SIMULADOS")
    print("="*70 + "\n")
    
    # 1. Cargar comunas del shapefile
    comunas_df = load_comunas_data()
    
    # 2. Cargar datos regionales
    regional_df = load_regional_data()
    
    # 3. Generar datos comunales
    comunal_df = create_comunal_data(regional_df, comunas_df)
    
    # 4. Validar consistencia
    validation = validate_data(regional_df, comunal_df)
    
    # 5. Guardar resultados
    print(f"\n💾 Guardando datos en: {OUTPUT_PATH}")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    comunal_df.to_csv(OUTPUT_PATH, index=False)
    
    # 6. Mostrar estadísticas
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS FINALES")
    print("="*70)
    print(f"Total registros:        {len(comunal_df):,}")
    print(f"Años:                   {comunal_df['año'].min()} - {comunal_df['año'].max()}")
    print(f"Regiones:               {comunal_df['region'].nunique()}")
    print(f"Comunas:                {comunal_df['comuna'].nunique()}")
    print(f"Especialidades:         {comunal_df['especialidad'].nunique()}")
    print(f"Tipos de dependencia:   {comunal_df['dependencia'].nunique()}")
    print(f"Matrícula total:        {comunal_df['matricula_total'].sum():,}")
    print("\nTop 10 comunas por matrícula:")
    top_comunas = comunal_df.groupby('comuna')['matricula_total'].sum().sort_values(ascending=False).head(10)
    for comuna, matricula in top_comunas.items():
        print(f"  • {comuna}: {matricula:,}")
    
    print("\n✅ Proceso completado exitosamente!\n")

if __name__ == "__main__":
    main()

"""
============================================================================
GENERADOR DE DATOS SIMULADOS PARA EMTP
============================================================================
Genera datos realistas basados en estadísticas reales del sistema EMTP chileno
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple


class EMTPDataGenerator:
    """Generador de datos simulados para el sistema EMTP"""
    
    def __init__(self, seed=42):
        """Inicializa el generador con una semilla para reproducibilidad"""
        np.random.seed(seed)
        random.seed(seed)
        
        # Datos base del sistema EMTP chileno
        self.regiones = [
            "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama",
            "Coquimbo", "Valparaíso", "Metropolitana", "O'Higgins", 
            "Maule", "Ñuble", "Biobío", "La Araucanía", "Los Ríos", 
            "Los Lagos", "Aysén", "Magallanes"
        ]
        
        self.especialidades = [
            "Administración", "Electricidad", "Mecánica Industrial", 
            "Construcción", "Gastronomía", "Contabilidad", "Enfermería",
            "Programación", "Telecomunicaciones", "Soldadura", 
            "Turismo", "Párvulos", "Agropecuaria", "Forestal",
            "Acuicultura", "Minería", "Química Industrial"
        ]
        
        self.dependencias = ["Municipal", "Particular Subvencionado", "Particular"]
        self.generos = ["Masculino", "Femenino"]
        self.años = list(range(2015, 2025))
        
        # Distribuciones realistas basadas en datos del MINEDUC
        self.dist_matricula_region = {
            "Metropolitana": 0.284, "Biobío": 0.098, "Valparaíso": 0.087,
            "La Araucanía": 0.064, "Maule": 0.058, "O'Higgins": 0.055,
            "Los Lagos": 0.052, "Antofagasta": 0.048, "Coquimbo": 0.045,
            "Tarapacá": 0.042, "Atacama": 0.038, "Ñuble": 0.035,
            "Los Ríos": 0.032, "Arica y Parinacota": 0.028,
            "Aysén": 0.019, "Magallanes": 0.015
        }
        
        self.dist_especialidad = {
            "Administración": 0.185, "Electricidad": 0.142, "Mecánica Industrial": 0.098,
            "Construcción": 0.087, "Gastronomía": 0.076, "Contabilidad": 0.065,
            "Enfermería": 0.058, "Programación": 0.052, "Telecomunicaciones": 0.045,
            "Soldadura": 0.038, "Turismo": 0.035, "Párvulos": 0.032,
            "Agropecuaria": 0.028, "Forestal": 0.025, "Acuicultura": 0.022,
            "Minería": 0.018, "Química Industrial": 0.015
        }

    def generate_matricula_data(self, years: List[int] = None) -> pd.DataFrame:
        """Genera datos de matrícula por año, región, especialidad"""
        if years is None:
            years = self.años
            
        data = []
        base_matricula = 78000
        
        for year in years:
            # Crecimiento anual variable
            crecimiento = np.random.normal(0.025, 0.008)  # 2.5% ± 0.8%
            matricula_año = int(base_matricula * (1 + crecimiento) ** (year - 2015))
            
            for region in self.regiones:
                matricula_region = int(matricula_año * self.dist_matricula_region[region])
                
                for especialidad in self.especialidades:
                    matricula_esp = int(matricula_region * self.dist_especialidad[especialidad])
                    
                    if matricula_esp > 0:  # Solo incluir si hay matrícula
                        # Distribución por género (varía por especialidad)
                        if especialidad in ["Enfermería", "Párvulos", "Gastronomía"]:
                            pct_mujeres = np.random.uniform(0.65, 0.85)
                        elif especialidad in ["Electricidad", "Mecánica Industrial", "Construcción", "Minería"]:
                            pct_mujeres = np.random.uniform(0.05, 0.25)
                        else:
                            pct_mujeres = np.random.uniform(0.35, 0.65)
                        
                        mujeres = int(matricula_esp * pct_mujeres)
                        hombres = matricula_esp - mujeres
                        
                        # Distribución por dependencia
                        for dependencia in self.dependencias:
                            if dependencia == "Municipal":
                                pct_dep = np.random.uniform(0.40, 0.50)
                            elif dependencia == "Particular Subvencionado":
                                pct_dep = np.random.uniform(0.45, 0.55)
                            else:  # Particular
                                pct_dep = np.random.uniform(0.02, 0.08)
                            
                            matricula_dep = int(matricula_esp * pct_dep)
                            
                            if matricula_dep > 0:
                                data.append({
                                    'año': year,
                                    'region': region,
                                    'especialidad': especialidad,
                                    'dependencia': dependencia,
                                    'matricula_total': matricula_dep,
                                    'matricula_hombres': int(matricula_dep * (1 - pct_mujeres)),
                                    'matricula_mujeres': int(matricula_dep * pct_mujeres),
                                    'tasa_retencion': np.random.uniform(0.82, 0.95)
                                })
            
            base_matricula = matricula_año
        
        return pd.DataFrame(data)

    def generate_egresados_data(self, years: List[int] = None) -> pd.DataFrame:
        """Genera datos de egresados y transición a ESUP"""
        if years is None:
            years = self.años
            
        data = []
        
        for year in years:
            for region in self.regiones:
                for especialidad in self.especialidades:
                    # Egresados basado en matrícula de hace 4 años
                    if year >= 2019:  # Solo si tenemos datos de 4 años atrás
                        egresados_base = int(np.random.uniform(50, 500))
                        
                        # Tasa de transición varía por especialidad
                        if especialidad in ["Enfermería", "Programación", "Contabilidad"]:
                            tasa_transicion = np.random.uniform(0.70, 0.85)
                        elif especialidad in ["Construcción", "Soldadura", "Minería"]:
                            tasa_transicion = np.random.uniform(0.45, 0.65)
                        else:
                            tasa_transicion = np.random.uniform(0.60, 0.75)
                        
                        transicion_esup = int(egresados_base * tasa_transicion)
                        
                        # Distribución entre universidades e institutos
                        pct_universidades = np.random.uniform(0.25, 0.45)
                        a_universidades = int(transicion_esup * pct_universidades)
                        a_institutos = transicion_esup - a_universidades
                        
                        data.append({
                            'año': year,
                            'region': region,
                            'especialidad': especialidad,
                            'egresados_total': egresados_base,
                            'transicion_esup': transicion_esup,
                            'tasa_transicion': tasa_transicion,
                            'a_universidades': a_universidades,
                            'a_institutos': a_institutos,
                            'continuidad_directa': np.random.choice([True, False], p=[0.78, 0.22])
                        })
        
        return pd.DataFrame(data)

    def generate_titulacion_data(self, years: List[int] = None) -> pd.DataFrame:
        """Genera datos de titulación"""
        if years is None:
            years = self.años
            
        data = []
        
        for year in years:
            for region in self.regiones:
                for especialidad in self.especialidades:
                    # Cohorte que debería titularse (ingresó hace 4-5 años)
                    cohorte_ingreso = year - 4
                    
                    if cohorte_ingreso >= 2015:
                        titulados_potenciales = int(np.random.uniform(30, 400))
                        
                        # Tasa de titulación varía por especialidad y región
                        if especialidad in ["Administración", "Contabilidad", "Programación"]:
                            tasa_titulacion = np.random.uniform(0.88, 0.96)
                        elif especialidad in ["Construcción", "Minería", "Soldadura"]:
                            tasa_titulacion = np.random.uniform(0.78, 0.88)
                        else:
                            tasa_titulacion = np.random.uniform(0.83, 0.93)
                        
                        titulados = int(titulados_potenciales * tasa_titulacion)
                        
                        # Tiempo de titulación (en meses desde egreso)
                        tiempo_promedio = np.random.uniform(12, 24)
                        
                        data.append({
                            'año': year,
                            'cohorte_ingreso': cohorte_ingreso,
                            'region': region,
                            'especialidad': especialidad,
                            'titulados': titulados,
                            'tasa_titulacion': tasa_titulacion,
                            'tiempo_titulacion_meses': tiempo_promedio,
                            'titulacion_oportuna': tiempo_promedio <= 18
                        })
        
        return pd.DataFrame(data)

    def generate_establecimientos_data(self) -> pd.DataFrame:
        """Genera datos de establecimientos"""
        data = []
        
        for region in self.regiones:
            # Número de establecimientos por región (proporcional a población)
            if region == "Metropolitana":
                n_establecimientos = np.random.randint(180, 220)
            elif region in ["Biobío", "Valparaíso"]:
                n_establecimientos = np.random.randint(60, 80)
            elif region in ["La Araucanía", "Maule", "O'Higgins"]:
                n_establecimientos = np.random.randint(40, 60)
            else:
                n_establecimientos = np.random.randint(15, 40)
            
            for i in range(n_establecimientos):
                # Especialidades por establecimiento
                n_especialidades = np.random.randint(2, 8)
                especialidades_est = random.sample(self.especialidades, n_especialidades)
                
                dependencia = np.random.choice(
                    ["Municipal", "Particular Subvencionado", "Particular"],
                    p=[0.45, 0.52, 0.03]
                )
                
                for esp in especialidades_est:
                    data.append({
                        'region': region,
                        'establecimiento_id': f"{region[:3].upper()}-{i+1:03d}",
                        'nombre_establecimiento': f"Liceo Técnico {region} {i+1}",
                        'dependencia': dependencia,
                        'especialidad': esp,
                        'año_creacion': np.random.randint(1980, 2020),
                        'zona': np.random.choice(["Urbana", "Rural"], p=[0.85, 0.15]),
                        'matricula_especialidad': np.random.randint(20, 120)
                    })
        
        return pd.DataFrame(data)

    def generate_docentes_data(self) -> pd.DataFrame:
        """Genera datos de docentes"""
        data = []
        
        for region in self.regiones:
            for especialidad in self.especialidades:
                # Número de docentes por especialidad y región
                n_docentes = int(np.random.uniform(5, 150))
                
                for i in range(n_docentes):
                    edad = np.random.randint(25, 65)
                    experiencia = min(np.random.randint(1, 25), edad - 23)
                    
                    # Distribución de género por especialidad
                    if especialidad in ["Enfermería", "Párvulos"]:
                        genero = np.random.choice(["Femenino", "Masculino"], p=[0.85, 0.15])
                    elif especialidad in ["Electricidad", "Mecánica Industrial", "Construcción"]:
                        genero = np.random.choice(["Femenino", "Masculino"], p=[0.15, 0.85])
                    else:
                        genero = np.random.choice(["Femenino", "Masculino"], p=[0.45, 0.55])
                    
                    data.append({
                        'region': region,
                        'especialidad': especialidad,
                        'docente_id': f"DOC-{region[:3]}-{especialidad[:3]}-{i+1:04d}",
                        'edad': edad,
                        'genero': genero,
                        'experiencia_años': experiencia,
                        'titulo_pedagogico': np.random.choice([True, False], p=[0.78, 0.22]),
                        'postgrado': np.random.choice([True, False], p=[0.35, 0.65]),
                        'tipo_contrato': np.random.choice(
                            ["Indefinido", "Plazo fijo", "Honorarios"], 
                            p=[0.67, 0.28, 0.05]
                        ),
                        'jornada': np.random.choice(
                            ["Completa", "Media", "Parcial"], 
                            p=[0.42, 0.35, 0.23]
                        ),
                        'establecimiento_dependencia': np.random.choice(
                            ["Municipal", "Particular Subvencionado", "Particular"],
                            p=[0.45, 0.52, 0.03]
                        )
                    })
        
        return pd.DataFrame(data)

    def generate_proyectos_data(self, years: List[int] = None) -> pd.DataFrame:
        """Genera datos de proyectos SEEMTP"""
        if years is None:
            years = list(range(2017, 2025))  # SEEMTP empezó en 2017
            
        data = []
        
        tipos_proyecto = [
            "Equipamiento", "Infraestructura", "Capacitación Docente", 
            "Innovación Curricular", "Vinculación Empresa"
        ]
        
        for year in years:
            for region in self.regiones:
                n_proyectos = np.random.randint(8, 35)
                
                for i in range(n_proyectos):
                    tipo = np.random.choice(tipos_proyecto)
                    
                    # Monto por tipo de proyecto
                    if tipo == "Infraestructura":
                        monto = np.random.uniform(50, 500) * 1_000_000  # 50M - 500M
                    elif tipo == "Equipamiento":
                        monto = np.random.uniform(10, 150) * 1_000_000  # 10M - 150M
                    else:
                        monto = np.random.uniform(5, 50) * 1_000_000   # 5M - 50M
                    
                    data.append({
                        'año': year,
                        'region': region,
                        'proyecto_id': f"SEEMTP-{year}-{region[:3]}-{i+1:03d}",
                        'tipo_proyecto': tipo,
                        'monto_asignado': monto,
                        'monto_ejecutado': monto * np.random.uniform(0.70, 0.98),
                        'pct_ejecucion': np.random.uniform(0.70, 0.98),
                        'establecimientos_beneficiados': np.random.randint(1, 8),
                        'estudiantes_impactados': np.random.randint(50, 800),
                        'estado': np.random.choice(
                            ["En ejecución", "Finalizado", "En licitación"], 
                            p=[0.60, 0.35, 0.05]
                        )
                    })
        
        return pd.DataFrame(data)

    def save_all_datasets(self, output_dir: str = "data/processed"):
        """Genera y guarda todos los datasets"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("🔄 Generando datos de matrícula...")
        matricula_df = self.generate_matricula_data()
        matricula_df.to_csv(f"{output_dir}/matricula_simulada.csv", index=False)
        
        print("🔄 Generando datos de egresados...")
        egresados_df = self.generate_egresados_data()
        egresados_df.to_csv(f"{output_dir}/egresados_simulados.csv", index=False)
        
        print("🔄 Generando datos de titulación...")
        titulacion_df = self.generate_titulacion_data()
        titulacion_df.to_csv(f"{output_dir}/titulacion_simulada.csv", index=False)
        
        print("🔄 Generando datos de establecimientos...")
        establecimientos_df = self.generate_establecimientos_data()
        establecimientos_df.to_csv(f"{output_dir}/establecimientos_simulados.csv", index=False)
        
        print("🔄 Generando datos de docentes...")
        docentes_df = self.generate_docentes_data()
        docentes_df.to_csv(f"{output_dir}/docentes_simulados.csv", index=False)
        
        print("🔄 Generando datos de proyectos...")
        proyectos_df = self.generate_proyectos_data()
        proyectos_df.to_csv(f"{output_dir}/proyectos_simulados.csv", index=False)
        
        print("✅ Todos los datasets generados exitosamente!")
        
        return {
            'matricula': matricula_df,
            'egresados': egresados_df,
            'titulacion': titulacion_df,
            'establecimientos': establecimientos_df,
            'docentes': docentes_df,
            'proyectos': proyectos_df
        }


if __name__ == "__main__":
    # Generar todos los datos
    generator = EMTPDataGenerator(seed=42)
    datasets = generator.save_all_datasets()
    
    # Mostrar resumen
    for nombre, df in datasets.items():
        print(f"\n📊 {nombre.upper()}: {len(df):,} registros")
        if 'año' in df.columns:
            print(f"   📅 Años: {df['año'].min()} - {df['año'].max()}")
        if 'region' in df.columns:
            print(f"   🗺️  Regiones: {df['region'].nunique()}")
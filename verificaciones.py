"""
VERIFICACIONES AUTOMATICAS - BENCHMARK 3D SEMANA 1 MCOC
========================================================
Verifica todas las condiciones de aceptacion del modelo
"""

import json
import sys
from pathlib import Path

def cargar_datos(ruta_datos):
    with open(ruta_datos, 'r') as f:
        return json.load(f)

def verificar_geometria(datos):
    print("\n=== VERIFICACION DE GEOMETRIA ===")
    
    geo = datos['geometria']
    losa = datos['losa']
    
    assert abs(geo['LX'] - 10.0) < 1e-10, f"Error: LX = {geo['LX']}, esperado 10.0"
    assert abs(geo['LY'] - 8.9) < 1e-10, f"Error: LY = {geo['LY']}, esperado 8.9"
    assert abs(geo['H'] - 3.96) < 1e-10, f"Error: H = {geo['H']}, esperado 3.96"
    
    area_esperada = 2 * geo['ancho_pano'] * geo['largo_pano']
    assert abs(losa['area_total'] - area_esperada) < 1e-10, \
        f"Error: Area total = {losa['area_total']}, esperado {area_esperada}"
    
    print(f"[OK] Dimensiones correctas: {geo['LX']} x {geo['LY']} x {geo['H']} m")
    print(f"[OK] Area de losas: {losa['area_total']:.2f} m2 (esperado: {area_esperada:.2f} m2)")
    
    return True

def verificar_secciones(datos):
    print("\n=== VERIFICACION DE SECCIONES (colaboracion monolitica) ===")
    
    secciones = datos['secciones']
    col = secciones['columna']
    sec_T = secciones['viga_T_interior']
    sec_L89 = secciones['viga_L_borde_890']
    sec_L5 = secciones['viga_L_borde_500']
    
    tolerancia = 1e-6
    
    # Verificar columna sin cambios
    assert abs(col['A'] - 0.49) < tolerancia, f"Error: Area columna = {col['A']}"
    assert abs(col['b'] - 0.70) < tolerancia
    assert abs(col['h'] - 0.70) < tolerancia
    print(f"[OK] Columna P70x70 sin cambios: A={col['A']:.4f} m2")
    
    # Verificar dimensiones comunes
    for nombre, sec in [('T', sec_T), ('L89', sec_L89), ('L5', sec_L5)]:
        assert abs(sec['bw'] - 0.60) < tolerancia, f"Error: bw={sec['bw']} en {nombre}"
        assert abs(sec['h'] - 0.80) < tolerancia, f"Error: h={sec['h']} en {nombre}"
        assert abs(sec['hf'] - 0.15) < tolerancia, f"Error: hf={sec['hf']} en {nombre}"
        assert abs(sec['hw'] - 0.65) < tolerancia, f"Error: hw={sec['hw']} en {nombre}"
    print("[OK] bw=0.60, h=0.80, hf=0.15, hw=0.65 verificado para todas las vigas")
    
    # Verificar que secciones son diferentes a la rectangular original
    assert abs(sec_T['A'] - 0.48) > 0.01, "Error: A_T igual a rectangular original"
    assert abs(sec_L89['A'] - 0.48) > 0.01, "Error: A_L89 igual a rectangular original"
    assert abs(sec_L5['A'] - 0.48) > 0.01, "Error: A_L5 igual a rectangular original"
    print("[OK] Las secciones T y L difieren de la rectangular original 0.60x0.80")
    
    # Verificar que T tiene mayor area que L
    assert sec_T['A'] > sec_L89['A'], "Error: A_T debe ser > A_L89"
    print(f"[OK] A_T ({sec_T['A']:.4f}) > A_L89 ({sec_L89['A']:.4f})")
    
    # Tabla resumen
    print("\n  Tabla de propiedades de secciones vigas:")
    print(f"  {'Seccion':20s} {'Tipo':5s} {'A(m2)':8s} {'y_bar(m)':9s} {'Iy(m4)':10s} {'Iz(m4)':10s} {'J(m4)':10s}  Elementos")
    print(f"  {'-'*100}")
    print(f"  {'T_INTERIOR_8.90':20s} {'T':5s} {sec_T['A']:8.4f} {sec_T['y_centroide']:9.4f} {sec_T['Iy']:10.6f} {sec_T['Iz']:10.6f} {sec_T['J']:10.6f}  10 (B-E)")
    print(f"  {'L_BORDE_8.90':20s} {'L':5s} {sec_L89['A']:8.4f} {sec_L89['y_centroide']:9.4f} {sec_L89['Iy']:10.6f} {sec_L89['Iz']:10.6f} {sec_L89['J']:10.6f}  9,11 (A-D, C-F)")
    print(f"  {'L_BORDE_5.00':20s} {'L':5s} {sec_L5['A']:8.4f} {sec_L5['y_centroide']:9.4f} {sec_L5['Iy']:10.6f} {sec_L5['Iz']:10.6f} {sec_L5['J']:10.6f}  5,6,7,8 (A-B,B-C,D-E,E-F)")
    
    # Documentar aproximacion
    print("\n  Aproximacion para secciones L en elasticBeamColumn:")
    print("  - Iyz = 0 (seccion simetrica respecto del eje vertical del alma)")
    print("  - Los ejes centroidales coinciden con los ejes principales de inercia")
    print("  - elasticBeamColumn usa Iy e Iz centroidales directamente")
    
    return True

def verificar_areas_tributarias(datos):
    print("\n=== VERIFICACION DE AREAS TRIBUTARIAS ===")
    
    areas = datos['areas_tributarias']
    
    area_pano = areas['por_pano']['triangular'] * 2 + areas['por_pano']['trapezoidal'] * 2
    assert abs(area_pano - 44.50) < 1e-10, \
        f"Error: Area por pano = {area_pano}, esperado 44.50"
    
    area_total = sum([v['area'] for v in areas['por_viga'].values()])
    assert abs(area_total - 89.00) < 1e-10, \
        f"Error: Area total tributaria = {area_total}, esperado 89.00"
    
    print(f"[OK] Area por pano: {area_pano:.2f} m2 (esperado: 44.50 m2)")
    print(f"[OK] Area total tributaria: {area_total:.2f} m2 (esperado: 89.00 m2)")
    
    return True

def verificar_cargas(datos):
    print("\n=== VERIFICACION DE CARGAS ===")
    
    cargas = datos['cargas_distribuidas']
    
    carga_5m = cargas['viga_5m']['integral'] * 4
    carga_8m_ext = cargas['viga_8m_exterior']['integral'] * 2
    carga_8m_cent = cargas['viga_8m_central']['integral'] * 1
    carga_vigas = carga_5m + carga_8m_ext + carga_8m_cent
    
    assert abs(carga_vigas - 445.00) < 1e-10, \
        f"Error: Carga total en vigas = {carga_vigas}, esperado 445.00"
    
    print(f"[OK] Vigas 5m (x4): {carga_5m:.2f} kN")
    print(f"[OK] Vigas 8.9m ext (x2): {carga_8m_ext:.2f} kN")
    print(f"[OK] Viga 8.9m cent (x1): {carga_8m_cent:.2f} kN")
    print(f"[OK] Carga total en vigas: {carga_vigas:.2f} kN (esperado: 445.00 kN)")
    
    return True

def verificar_reacciones(resultados, tolerancia=1e-6):
    print("\n=== VERIFICACION DE REACCIONES ===")
    
    suma_RZ = 0.0
    suma_RX = 0.0
    suma_RY = 0.0
    for nombre, reac in resultados['reacciones'].items():
        suma_RZ += reac['RZ']
        suma_RX += reac['RX']
        suma_RY += reac['RY']
    
    error_RZ = abs(suma_RZ - 445.00)
    assert error_RZ < tolerancia, \
        f"Error: Suma RZ = {suma_RZ:.6f}, esperado 445.00, error = {error_RZ:.6f}"
    
    error_RX = abs(suma_RX)
    assert error_RX < tolerancia, \
        f"Error: Suma RX = {suma_RX:.6f}, esperado 0.00, error = {error_RX:.6f}"
    
    error_RY = abs(suma_RY)
    assert error_RY < tolerancia, \
        f"Error: Suma RY = {suma_RY:.6f}, esperado 0.00, error = {error_RY:.6f}"
    
    print(f"[OK] Suma RZ = {suma_RZ:.6f} kN (esperado: 445.00 kN)")
    print(f"[OK] Suma RX = {suma_RX:.6f} kN (esperado: 0.00 kN)")
    print(f"[OK] Suma RY = {suma_RY:.6f} kN (esperado: 0.00 kN)")
    print(f"[OK] Error RZ absoluto: {error_RZ:.6f} kN")
    print(f"[OK] Error RZ relativo: {error_RZ/445.00*100:.10f}%")
    
    for nombre, reac in resultados['reacciones'].items():
        print(f"  {nombre}: RX={reac['RX']:+.4f} RY={reac['RY']:+.4f} RZ={reac['RZ']:+.4f} kN")
    
    return True

def verificar_desplazamientos(datos, resultados):
    print("\n=== VERIFICACION DE DESPLAZAMIENTOS ===")
    
    nodos_base = ['base_A', 'base_C', 'base_D', 'base_F']
    for nombre in nodos_base:
        desp = resultados['desplazamientos'][nombre]
        assert abs(desp['UZ']) < 1e-10, \
            f"Error: Nodo {nombre} tiene UZ = {desp['UZ']}"
    
    print("[OK] Nodos de base no se desplazan (empotrados)")
    
    nodos_superior = ['sup_A', 'sup_B', 'sup_C', 'sup_D', 'sup_E', 'sup_F']
    for nombre in nodos_superior:
        desp = resultados['desplazamientos'][nombre]
        assert desp['UZ'] <= 0, \
            f"Error: Nodo {nombre} tiene UZ = {desp['UZ']} (debe ser <= 0)"
    
    print("[OK] Nodos superiores se desplazan hacia abajo (UZ <= 0)")
    
    for nombre in nodos_superior:
        desp = resultados['desplazamientos'][nombre]
        print(f"  {nombre}: UZ = {desp['UZ']:.8f} m")
    
    return True

def verificar_fuerzas_elementos(resultados):
    print("\n=== VERIFICACION DE FUERZAS DE ELEMENTOS (locales) ===")
    
    locales = resultados['fuerzas_locales_elementos']
    
    for elem, fuerzas in locales.items():
        assert abs(fuerzas['N_i']) < 1000, \
            f"Error: Elemento {elem} tiene N_i = {fuerzas['N_i']}"
    
    print("[OK] Fuerzas de elementos en rangos razonables")
    
    elem_info = {
        'elem_1': 'Col A', 'elem_2': 'Col C', 'elem_3': 'Col D', 'elem_4': 'Col F',
        'elem_5': 'Vig A-B', 'elem_6': 'Vig B-C', 'elem_7': 'Vig D-E', 'elem_8': 'Vig E-F',
        'elem_9': 'Vig A-D', 'elem_10': 'Vig B-E', 'elem_11': 'Vig C-F'
    }
    
    for elem, fuerzas in locales.items():
        nombre = elem_info.get(elem, elem)
        print(f"  {nombre:10s}: N_i={fuerzas['N_i']:+10.4f} Vz_i={fuerzas['Vz_i']:+10.4f} "
              f"My_i={fuerzas['My_i']:+10.4f} Mz_i={fuerzas['Mz_i']:+10.4f}")
    
    return True

def verificar_columna_A(resultados):
    print("\n=== VERIFICACION COLUMNA A (axial ~ 111.25 kN) ===")
    
    locales = resultados['fuerzas_locales_elementos']
    col_A = locales['elem_1']
    
    N_col = abs(col_A['N_i'])
    assert abs(N_col - 111.25) < 0.1, \
        f"Error: Columna A N_i = {N_col:.4f}, esperado ~111.25"
    
    print(f"[OK] Columna A: N_local = {col_A['N_i']:+.4f} kN (|N| = {N_col:.4f} ~ 111.25)")
    
    return True

def verificar_cortantes_vigas(resultados):
    print("\n=== VERIFICACION DE CORTANTES EN VIGAS ===")
    
    locales = resultados['fuerzas_locales_elementos']
    
    # Viga A-B (elem 5): carga triangular = 31.25 kN
    fl_5 = locales['elem_5']
    Vz_5_total = fl_5['Vz_i'] + fl_5['Vz_j']
    assert abs(Vz_5_total - 31.25) < 0.1, \
        f"Error: Vig A-B Vz_total = {Vz_5_total:.4f}, esperado 31.25"
    print(f"[OK] Vig A-B (elem 5): Vz_i+Vz_j = {Vz_5_total:+.4f} kN (esperado: 31.25)")
    
    # Viga A-D (elem 9): carga trapezoidal = 80 kN
    fl_9 = locales['elem_9']
    Vz_9_total = fl_9['Vz_i'] + fl_9['Vz_j']
    assert abs(Vz_9_total - 80.0) < 0.1, \
        f"Error: Vig A-D Vz_total = {Vz_9_total:.4f}, esperado 80.0"
    print(f"[OK] Vig A-D (elem 9): Vz_i+Vz_j = {Vz_9_total:+.4f} kN (esperado: 80.00)")
    
    # Viga B-E (elem 10): carga trapezoidal x2 = 160 kN
    fl_10 = locales['elem_10']
    Vz_10_total = fl_10['Vz_i'] + fl_10['Vz_j']
    assert abs(Vz_10_total - 160.0) < 0.1, \
        f"Error: Vig B-E Vz_total = {Vz_10_total:.4f}, esperado 160.0"
    print(f"[OK] Vig B-E (elem 10): Vz_i+Vz_j = {Vz_10_total:+.4f} kN (esperado: 160.00)")
    
    return True

def verificar_equilibrio_cargas(datos, resultados):
    print("\n=== VERIFICACION DE EQUILIBRIO DE CARGAS ===")
    
    cargas = datos['cargas_distribuidas']
    
    carga_5m = cargas['viga_5m']['integral'] * 4
    carga_8m_ext = cargas['viga_8m_exterior']['integral'] * 2
    carga_8m_cent = cargas['viga_8m_central']['integral'] * 1
    carga_total_modelo = carga_5m + carga_8m_ext + carga_8m_cent
    
    # Verificar con suma de reacciones
    suma_RZ = sum(r['RZ'] for r in resultados['reacciones'].values())
    
    print(f"  Carga total (datos):  {carga_total_modelo:.2f} kN")
    print(f"  Suma RZ (modelo):     {suma_RZ:+.6f} kN")
    print(f"  Diferencia:           {abs(suma_RZ - carga_total_modelo):.6f} kN")
    
    assert abs(suma_RZ - carga_total_modelo) < 0.01, \
        f"Error: RZ={suma_RZ:.6f} != carga={carga_total_modelo:.2f}"
    
    print(f"[OK] Equilibrio carga-reacciones verificado")
    
    return True

def verificar_BE_empotrado_empotrado(resultados):
    print("\n=== VERIFICACION VIGA B-E EMPOTRADO-EMPOTRADO ===")
    
    locales = resultados['fuerzas_locales_elementos']
    fl_BE = locales['elem_10']
    
    Vz_i = fl_BE['Vz_i']
    Vz_j = fl_BE['Vz_j']
    My_i = fl_BE['My_i']
    My_j = fl_BE['My_j']
    
    V_total = Vz_i + Vz_j
    print(f"  Vz_i = {Vz_i:+.4f} kN (esperado: ~80.00)")
    print(f"  Vz_j = {Vz_j:+.4f} kN (esperado: ~80.00)")
    print(f"  My_i = {My_i:+.4f} kN*m (esperado: ~-142.64)")
    print(f"  My_j = {My_j:+.4f} kN*m (esperado: ~-142.64)")
    
    # Cortantes
    assert abs(Vz_i - 80.0) < 1.0, \
        f"Error: Vz_i = {Vz_i:.4f}, esperado ~80.00"
    assert abs(Vz_j - 80.0) < 1.0, \
        f"Error: Vz_j = {Vz_j:.4f}, esperado ~80.00"
    assert abs(V_total - 160.0) < 0.1, \
        f"Error: V_total = {V_total:.4f}, esperado 160.00"
    print(f"[OK] Cortantes Vz_i={Vz_i:+.4f}, Vz_j={Vz_j:+.4f}, total={V_total:+.4f} kN")
    
    # Momentos de empotramiento
    assert abs(abs(My_i) - 142.64) < 2.0, \
        f"Error: |My_i| = {abs(My_i):.4f}, esperado ~142.64"
    assert abs(abs(My_j) - 142.64) < 2.0, \
        f"Error: |My_j| = {abs(My_j):.4f}, esperado ~142.64"
    print(f"[OK] Momentos empotramiento My_i={My_i:+.4f}, My_j={My_j:+.4f} kN*m (~-142.64)")
    
    # Momento a media luz via diagrama (si disponible)
    diag = resultados.get('diagrama_momento_BE', {})
    M_50 = diag.get('M_numerico_50', None)
    if M_50 is not None:
        print(f"  M_media_luz = {M_50:+.4f} kN*m (esperado: ~+78.85)")
        assert abs(M_50 - 78.85) < 2.0, \
            f"Error: M_media_luz = {M_50:.4f}, esperado ~+78.85"
        print(f"[OK] Momento a media luz verificado")
    
    return True

def generar_reporte(resultados, ruta_reporte):
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write("REPORTE DE VERIFICACION - BENCHMARK 3D SEMANA 1 MCOC\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("1. DESPLAZAMIENTOS\n")
        f.write("-" * 60 + "\n")
        for nombre, desp in resultados['desplazamientos'].items():
            f.write(f"  {nombre:12s}: UX={desp['UX']:+.8e} UY={desp['UY']:+.8e} UZ={desp['UZ']:+.8e} m\n")
        
        f.write("\n2. REACCIONES\n")
        f.write("-" * 60 + "\n")
        suma_RZ = 0
        suma_RX = 0
        for nombre, reac in resultados['reacciones'].items():
            f.write(f"  {nombre:12s}: RX={reac['RX']:+.4f} RY={reac['RY']:+.4f} RZ={reac['RZ']:+.4f} kN\n")
            suma_RZ += reac['RZ']
            suma_RX += reac['RX']
        f.write(f"\n  Suma RX = {suma_RX:+.6f} kN (esperado: 0.00)\n")
        f.write(f"  Suma RZ = {suma_RZ:+.6f} kN (esperado: 445.00)\n")
        f.write(f"  Error RZ = {abs(suma_RZ - 445.00):.6f} kN\n")
        
        f.write("\n3. FUERZAS GLOBALES (extremo i)\n")
        f.write("-" * 60 + "\n")
        globales = resultados.get('fuerzas_globales_elementos', {})
        for elem, fuerzas in globales.items():
            nombre = fuerzas.get('nombre', elem)
            f.write(f"  {nombre:12s}: FX={fuerzas['FX_i']:+.4f} FY={fuerzas['FY_i']:+.4f} FZ={fuerzas['FZ_i']:+.4f} "
                    f"MX={fuerzas['MX_i']:+.4f} MY={fuerzas['MY_i']:+.4f} MZ={fuerzas['MZ_i']:+.4f}\n")
        
        f.write("\n4. FUERZAS LOCALES (extremo i)\n")
        f.write("-" * 60 + "\n")
        f.write("  Convencion: [N_i, Vy_i, Vz_i, T_i, My_i, Mz_i]\n\n")
        
        locales = resultados.get('fuerzas_locales_elementos', {})
        for elem, fuerzas in locales.items():
            nombre = fuerzas.get('nombre', elem)
            f.write(f"  {nombre:12s}: N={fuerzas['N_i']:+.4f} Vy={fuerzas['Vy_i']:+.4f} Vz={fuerzas['Vz_i']:+.4f} "
                    f"T={fuerzas['T_i']:+.4f} My={fuerzas['My_i']:+.4f} Mz={fuerzas['Mz_i']:+.4f}\n")
        
        f.write("\n5. CARGAS APLICADAS\n")
        f.write("-" * 60 + "\n")
        cargas = resultados.get('cargas_elementos', {})
        for nombre, info in cargas.items():
            f.write(f"  {nombre}: tipo={info['tipo']}, L={info['L']} m, integral={info['integral']:.2f} kN\n")
        
        f.write("\n6. VERIFICACIONES\n")
        f.write("-" * 60 + "\n")
        verif = resultados.get('verificaciones', {})
        f.write(f"  Carga total:  {verif.get('carga_total_kN', 'N/A')} kN\n")
        f.write(f"  Suma RZ:      {verif.get('suma_RZ_kN', 'N/A'):.6f} kN\n")
        f.write(f"  Equilibrio:   {'SI' if verif.get('equilibrio') else 'NO'}\n")
    
    print(f"\nReporte generado en: {ruta_reporte}")

def main():
    print("=" * 60)
    print("VERIFICACIONES AUTOMATICAS - BENCHMARK 3D SEMANA 1 MCOC")
    print("=" * 60)
    
    ruta_datos = Path(__file__).parent / 'datos_entrada.json'
    ruta_resultados = Path(__file__).parent / 'resultados' / 'resultados.json'
    ruta_reporte = Path(__file__).parent / 'resultados' / 'reporte_verificacion.txt'
    
    datos = cargar_datos(ruta_datos)
    
    with open(ruta_resultados, 'r') as f:
        resultados = json.load(f)
    
    try:
        verificar_geometria(datos)
        verificar_secciones(datos)
        verificar_areas_tributarias(datos)
        verificar_cargas(datos)
        verificar_reacciones(resultados)
        verificar_desplazamientos(datos, resultados)
        verificar_fuerzas_elementos(resultados)
        verificar_columna_A(resultados)
        verificar_cortantes_vigas(resultados)
        verificar_equilibrio_cargas(datos, resultados)
        verificar_BE_empotrado_empotrado(resultados)
        
        print("\n" + "=" * 60)
        print("[OK] TODAS LAS VERIFICACIONES PASARON")
        print("=" * 60)
        
        generar_reporte(resultados, ruta_reporte)
        
        return 0
        
    except AssertionError as e:
        print(f"\n[FAIL] VERIFICACION FALLIDA: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

"""
MODELO OPENSEESPY - BENCHMARK 3D RECTANGULAR SEMANA 1 MCOC
============================================================
Version rectangular: vigas 0.60 x 0.80 m (sin colaboracion T/L)
Marco espacial elastico lineal 3D
10 nodos, 11 elementos, 4 columnas, 7 vigas
Cargas distribuidas via eleLoad (point loads por region)
Fuerzas globales y locales separadas
"""

import json
import sys
from pathlib import Path

import numpy as np
from openseespy.opensees import *

# =============================================================================
# 1. CARGA DE DATOS DE ENTRADA
# =============================================================================

def cargar_datos(ruta_datos):
    with open(ruta_datos, 'r') as f:
        return json.load(f)

# =============================================================================
# 2. DEFINICION DE NODOS
# =============================================================================

def crear_nodos(datos):
    nodos = datos['nodos']

    base_tags = {'A': 1, 'C': 3, 'D': 4, 'F': 6}
    for nombre, tag in base_tags.items():
        coord = nodos['base'][nombre]
        node(tag, coord[0], coord[1], coord[2])

    sup_tags = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    for nombre, tag in sup_tags.items():
        coord = nodos['superior'][nombre]
        node(tag, coord[0], coord[1], coord[2])

    print("Nodos creados: 10")
    print("  Base   (Z=0):   A=1, C=3, D=4, F=6")
    print("  Sup. (Z=3.96): A=10, B=11, C=12, D=13, E=14, F=15")

    return base_tags, sup_tags

# =============================================================================
# 3. DEFINICION DE MATERIAL
# =============================================================================

def crear_material(datos):
    mat = datos['materiales']['concreto']
    E = mat['E']
    nu = mat['nu']
    G = E / (2 * (1 + nu))

    uniaxialMaterial('Elastic', 1, E)

    print(f"\nMaterial (supuesto): E={E/1e6:.1f} GPa, nu={nu}, G={G/1e6:.2f} GPa")
    return E, G

# =============================================================================
# 4. DEFINICION DE SECCIONES
# =============================================================================

def crear_secciones(E, G, datos):
    col = datos['secciones']['columna']
    sec_T = datos['secciones']['viga_T_interior']
    sec_L89 = datos['secciones']['viga_L_borde_890']
    sec_L5 = datos['secciones']['viga_L_borde_500']

    section('Elastic', 1, E, col['A'], col['Iz'], col['Iy'], G, col['J'])
    section('Elastic', 2, E, sec_T['A'], sec_T['Iz'], sec_T['Iy'], G, sec_T['J'])
    section('Elastic', 3, E, sec_L89['A'], sec_L89['Iz'], sec_L89['Iy'], G, sec_L89['J'])
    section('Elastic', 4, E, sec_L5['A'], sec_L5['Iz'], sec_L5['Iy'], G, sec_L5['J'])

    print("\n=== SECCIONES (VERSION RECTANGULAR - sin colaboracion T/L) ===")
    print(f"  [1] Columna P70x70      : A={col['A']:.4f} m2, Iy={col['Iy']:.6f}, Iz={col['Iz']:.6f}, J={col['J']:.6f}")
    print(f"  [2] RECT Interior 8.90  : A={sec_T['A']:.4f} m2, Iy={sec_T['Iy']:.6f}, Iz={sec_T['Iz']:.6f}, J={sec_T['J']:.6f}")
    print(f"  [3] RECT Borde 8.90     : A={sec_L89['A']:.4f} m2, Iy={sec_L89['Iy']:.6f}, Iz={sec_L89['Iz']:.6f}, J={sec_L89['J']:.6f}")
    print(f"  [4] RECT Borde 5.00     : A={sec_L5['A']:.4f} m2, Iy={sec_L5['Iy']:.6f}, Iz={sec_L5['Iz']:.6f}, J={sec_L5['J']:.6f}")

# =============================================================================
# 5. TRANSFORMACIONES GEOMETRICAS
# =============================================================================

def crear_transformaciones():
    geomTransf('Linear', 1, 0.0, 1.0, 0.0)
    geomTransf('Linear', 2, 0.0, 0.0, 1.0)
    geomTransf('Linear', 3, 0.0, 0.0, 1.0)

    print("\nTransformaciones geometricas:")
    print("  Tag 1: Columnas -- vecz=(0,1,0)")
    print("  Tag 2: Vigas X  -- vecz=(0,0,1)")
    print("  Tag 3: Vigas Y  -- vecz=(0,0,1)")

# =============================================================================
# 6. CREACION DE ELEMENTOS
# =============================================================================

def crear_elementos():
    columnas = [
        (1, 1, 10), (2, 3, 12), (3, 4, 13), (4, 6, 15),
    ]
    for tag, ni, nj in columnas:
        element('elasticBeamColumn', tag, ni, nj, 1, 1)

    vigas_x = [
        (5, 10, 11), (6, 11, 12), (7, 13, 14), (8, 14, 15),
    ]
    for tag, ni, nj in vigas_x:
        element('elasticBeamColumn', tag, ni, nj, 4, 2)

    vigas_y_borde = [(9, 10, 13), (11, 12, 15)]
    for tag, ni, nj in vigas_y_borde:
        element('elasticBeamColumn', tag, ni, nj, 3, 3)

    element('elasticBeamColumn', 10, 11, 14, 2, 3)

    print("\nElementos creados: 11")
    print("  Columnas P70x70      (sec 1): 1(A), 2(C), 3(D), 4(F)")
    print("  Vigas RECT 5.00m     (sec 4): 5(A-B), 6(B-C), 7(D-E), 8(E-F)")
    print("  Vigas RECT 8.90m ext (sec 3): 9(A-D), 11(C-F)")
    print("  Viga  RECT 8.90m cent(sec 2): 10(B-E)")

# =============================================================================
# 7. APOYOS EMPOTRADOS
# =============================================================================

def aplicar_apoyos():
    for tag in [1, 3, 4, 6]:
        fix(tag, 1, 1, 1, 1, 1, 1)
    print("\nApoyos: 4 empotrados en bases (nodos 1, 3, 4, 6)")

def aplicar_restricciones_RX():
    fix(11, 0, 0, 0, 1, 0, 0)
    fix(14, 0, 0, 0, 1, 0, 0)
    print("\nRestriccion RX_B=RX_E=0: viga B-E empotrado-empotrado")
    print("  Nodos 11,14: solo RX fijada, traslaciones y demas rotaciones libres")

# =============================================================================
# 8. CARGAS (eleLoad con point loads por region)
# =============================================================================

def crear_cargas():
    timeSeries('Linear', 1)
    pattern('Plain', 1, 1)

    # Triangular for 5m beams
    L5 = 5.0
    n_reg5 = 4
    dx5 = L5 / n_reg5
    xL_5 = []
    P_5 = []
    for k in range(n_reg5):
        x_mid = (k + 0.5) * dx5
        xL_5.append(x_mid / L5)
        if x_mid <= 2.5:
            w_mid = 12.5 * (x_mid / 2.5)
        else:
            w_mid = 12.5 * ((L5 - x_mid) / 2.5)
        P_5.append(w_mid * dx5)

    total_5 = sum(P_5)
    assert abs(total_5 - 31.25) < 1e-10, f"Error: carga triangular 5m = {total_5}"

    M_5 = sum(P_5[k] * (xL_5[k] * L5) for k in range(len(P_5)))
    M_5_esperado = total_5 * (L5 / 2.0)
    assert abs(M_5 - M_5_esperado) < 1e-10, f"Error: momento triangular 5m = {M_5}"

    for tag in [5, 6, 7, 8]:
        for xi, Pi in zip(xL_5, P_5):
            eleLoad('-ele', tag, '-type', '-beamPoint', 0.0, -Pi, xi, 0.0)

    # Trapezoidal for 8.9m beams
    L89 = 8.9
    a_rampa = 2.5
    b_const = 6.4

    # Region 1: Ramp left [0, 2.5m]
    n_reg1 = 4
    dx1 = a_rampa / n_reg1
    xL_r1 = []
    P_r1 = []
    for k in range(n_reg1):
        x_mid = (k + 0.5) * dx1
        xL_r1.append(x_mid / L89)
        w_mid = 12.5 * (x_mid / a_rampa)
        P_r1.append(w_mid * dx1)

    total_r1 = sum(P_r1)
    assert abs(total_r1 - 15.625) < 1e-10, f"Error: rampa izq = {total_r1}"

    # Region 2: Uniform [2.5m, 6.4m]
    n_reg2 = 6
    dx2 = (b_const - a_rampa) / n_reg2
    xL_r2 = []
    P_r2 = []
    for k in range(n_reg2):
        x_mid = a_rampa + (k + 0.5) * dx2
        xL_r2.append(x_mid / L89)
        P_r2.append(12.5 * dx2)

    total_r2 = sum(P_r2)
    assert abs(total_r2 - 48.75) < 1e-10, f"Error: uniforme = {total_r2}"

    # Region 3: Ramp right [6.4m, 8.9m]
    n_reg3 = 4
    dx3 = (L89 - b_const) / n_reg3
    xL_r3 = []
    P_r3 = []
    for k in range(n_reg3):
        x_mid = b_const + (k + 0.5) * dx3
        xL_r3.append(x_mid / L89)
        w_mid = 12.5 * ((L89 - x_mid) / (L89 - b_const))
        P_r3.append(w_mid * dx3)

    total_r3 = sum(P_r3)
    assert abs(total_r3 - 15.625) < 1e-10, f"Error: rampa der = {total_r3}"

    # Combine all regions
    xL_89 = xL_r1 + xL_r2 + xL_r3
    P_89 = P_r1 + P_r2 + P_r3
    total_89 = sum(P_89)
    assert abs(total_89 - 80.0) < 1e-10, f"Error: carga trapezoidal 8.9m = {total_89}"

    M_89 = sum(P_89[k] * (xL_89[k] * L89) for k in range(len(P_89)))
    M_89_esperado = total_89 * (L89 / 2.0)
    assert abs(M_89 - M_89_esperado) < 1e-10, f"Error: momento trapezoidal 8.9m = {M_89}"

    for tag in [9, 11]:
        for xi, Pi in zip(xL_89, P_89):
            eleLoad('-ele', tag, '-type', '-beamPoint', 0.0, -Pi, xi, 0.0)

    for xi, Pi in zip(xL_89, P_89):
        eleLoad('-ele', 10, '-type', '-beamPoint', 0.0, -2.0 * Pi, xi, 0.0)

    total_BE = sum(2.0 * Pi for Pi in P_89)
    assert abs(total_BE - 160.0) < 1e-10, f"Error: carga B-E = {total_BE}"

    P_total = 4 * total_5 + 2 * total_89 + total_BE

    print("\n=== CARGAS (eleLoad point loads) ===")
    print(f"\n  Vigas 5m (triangular, 4 puntos c/u):")
    print(f"  {'Elem':5s} {'x/L':>7s} {'P (kN)':>10s}")
    for xi, Pi in zip(xL_5, P_5):
        print(f"  {'':5s} {xi:7.4f} {Pi:10.5f}")
    print(f"  {'':5s} {'Total':>7s} {total_5:10.5f} kN (esperado: 31.25)")

    print(f"\n  Vigas 8.9m (trapezoidal, 14 puntos c/u):")
    print(f"  Region 1 [0, 2.5m]: {n_reg1} puntos, integral = {total_r1:.5f} kN")
    print(f"  Region 2 [2.5, 6.4m]: {n_reg2} puntos, integral = {total_r2:.5f} kN")
    print(f"  Region 3 [6.4, 8.9m]: {n_reg3} puntos, integral = {total_r3:.5f} kN")
    print(f"  Total por viga: {total_89:.5f} kN (esperado: 80.00)")

    print(f"\n  Viga B-E (x2 magnitud): {total_BE:.5f} kN (esperado: 160.00)")

    print(f"\n  Carga vertical total: {P_total:.2f} kN (esperado: 445.00)")
    print(f"  Momento total 5m:   {M_5:.5f} kN*m (esperado: {M_5_esperado:.5f})")
    print(f"  Momento total 8.9m: {M_89:.5f} kN*m (esperado: {M_89_esperado:.5f})")

    if abs(P_total - 445.00) > 1e-10:
        print("  ERROR: La carga total no coincide!")
        sys.exit(1)
    print("  OK: Carga total y momentos verificados.")

    return {
        'cargas_vigas': {
            'viga_5m': {
                'tipo': 'triangular', 'L': L5, 'w_max': 12.5,
                'num_puntos': n_reg5, 'integral': total_5,
                'momento_i': M_5,
                'puntos': [{'x/L': xi, 'P': Pi} for xi, Pi in zip(xL_5, P_5)]
            },
            'viga_8m_ext': {
                'tipo': 'trapezoidal', 'L': L89, 'w_max': 12.5,
                'num_puntos': len(xL_89), 'integral': total_89,
                'momento_i': M_89,
                'regiones': {
                    'rampa_izq': {'n': n_reg1, 'integral': total_r1},
                    'uniforme': {'n': n_reg2, 'integral': total_r2},
                    'rampa_der': {'n': n_reg3, 'integral': total_r3}
                },
                'puntos': [{'x/L': xi, 'P': Pi} for xi, Pi in zip(xL_89, P_89)]
            },
            'viga_8m_cent': {
                'tipo': 'trapezoidal_x2', 'L': L89, 'w_max': 25.0,
                'num_puntos': len(xL_89), 'integral': total_BE,
                'momento_i': 2.0 * M_89,
                'puntos': [{'x/L': xi, 'P': 2.0 * Pi} for xi, Pi in zip(xL_89, P_89)]
            }
        },
        'carga_total': P_total
    }

# =============================================================================
# 8b. MOMENTO INTERNO A LO LARGO DEL ELEMENTO
# =============================================================================

def momento_interno(x, My_i, Fz_i, L, puntos_carga):
    M = My_i + Fz_i * x
    for pc in puntos_carga:
        s = pc['x/L'] * L
        if s < x - 1e-12:
            M -= pc['P'] * (x - s)
    return M

def cortante_interno(x, Fz_i, L, puntos_carga):
    V = Fz_i
    for pc in puntos_carga:
        s = pc['x/L'] * L
        if s <= x + 1e-12:
            V -= pc['P']
    return V

def momento_interno_analitico_ss(x, L, w_max, a_rampa, b_const):
    a = a_rampa
    b = b_const
    c = L - b
    R = w_max * (L + b - a) / 4.0
    M = R * x

    if x <= a:
        M -= (w_max / (6.0 * a)) * x ** 3
    elif x <= b:
        M -= (w_max * a / 6.0) * (3.0 * x - 2.0 * a)
        M -= w_max * (x - a) ** 2 / 2.0
    else:
        M -= (w_max * a / 6.0) * (3.0 * x - 2.0 * a)
        M -= w_max * (b - a) * (x - (a + b) / 2.0)
        d = x - b
        M -= w_max * d ** 2 * (3.0 * c - d) / (6.0 * c)
    return M

def _w_trapezoidal(s, L, w_max, a_rampa, b_const):
    if s <= a_rampa:
        return w_max * s / a_rampa if a_rampa > 0 else 0.0
    elif s <= b_const:
        return w_max
    elif s <= L:
        return w_max * (L - s) / (L - b_const) if (L - b_const) > 0 else 0.0
    return 0.0

def calcular_fijos_analitico(L, w_max, a_rampa, b_const, n_quad=1000):
    s_vals = np.linspace(0, L, n_quad + 1)
    w_vals = np.array([_w_trapezoidal(s, L, w_max, a_rampa, b_const) for s in s_vals])
    h = L / n_quad

    integrand_B = w_vals * s_vals * (L - s_vals)**2
    integrand_E = w_vals * s_vals**2 * (L - s_vals)
    integrand_R = w_vals * s_vals

    I_B = np.sum(integrand_B[0::2]) * 2 + np.sum(integrand_B[1::2]) * 4
    I_B = (I_B - integrand_B[0] - integrand_B[-1]) * h / 3.0

    I_E = np.sum(integrand_E[0::2]) * 2 + np.sum(integrand_E[1::2]) * 4
    I_E = (I_E - integrand_E[0] - integrand_E[-1]) * h / 3.0

    I_R = np.sum(integrand_R[0::2]) * 2 + np.sum(integrand_R[1::2]) * 4
    I_R = (I_R - integrand_R[0] - integrand_R[-1]) * h / 3.0

    M_B = -I_B / L**2
    M_E = I_E / L**2
    R = I_R / L
    return M_B, M_E, R

def momento_ff_analitico(x, L, M_B, R, w_max, a_rampa, b_const):
    return M_B + momento_interno_analitico_ss(x, L, w_max, a_rampa, b_const)

def calcular_diagrama_BE(info_cargas, resultados):
    L_BE = 8.9
    n_pts = 100
    fl_BE = resultados['fuerzas_locales_elementos']['elem_10']
    My_i = fl_BE['My_i']
    Fz_i = fl_BE['Vz_i']
    puntos_carga = info_cargas['cargas_vigas']['viga_8m_cent']['puntos']

    xL_vals = np.linspace(0.0, 1.0, n_pts + 1)
    M_numerico = np.array([
        momento_interno(xL * L_BE, My_i, Fz_i, L_BE, puntos_carga) for xL in xL_vals
    ])

    M_ss = np.array([
        momento_interno_analitico_ss(xL * L_BE, L_BE, 25.0, 2.5, 6.4)
        for xL in xL_vals
    ])
    M_ff_B, M_ff_E, R_ff = calcular_fijos_analitico(L_BE, 25.0, 2.5, 6.4)
    M_ff = np.array([
        momento_ff_analitico(xL * L_BE, L_BE, M_ff_B, R_ff, 25.0, 2.5, 6.4)
        for xL in xL_vals
    ])

    M_50 = momento_interno(0.5 * L_BE, My_i, Fz_i, L_BE, puntos_carga)
    M_ss_50 = momento_interno_analitico_ss(0.5 * L_BE, L_BE, 25.0, 2.5, 6.4)
    M_ff_50 = momento_ff_analitico(0.5 * L_BE, L_BE, M_ff_B, R_ff, 25.0, 2.5, 6.4)

    print("\n=== MOMENTO INTERNO VIGA B-E (elem 10) - RECTANGULAR ===")
    print(f"  Metodo: M(x) = My_i + Fz_i*x - sum(P_k*(x-s_k))")
    print(f"  My_i = {My_i:+.4f} kN*m, Fz_i = {Fz_i:+.4f} kN")
    print(f"  L = {L_BE} m, {len(puntos_carga)} cargas puntuales")

    print(f"\n  Comparacion con soluciones de referencia:")
    print(f"    Empotrado-empotrado analitico (Simpson):")
    print(f"      M_B (FEM) = {M_ff_B:+.4f} kN*m")
    print(f"      M_E (FEM) = {M_ff_E:+.4f} kN*m")
    print(f"      R         = {R_ff:+.4f} kN")
    print(f"      M_centro  = {M_ff_50:+.4f} kN*m")
    print(f"    FEM (OpenSees):")
    print(f"      My_i      = {My_i:+.4f} kN*m")
    print(f"      My_j      = {fl_BE['My_j']:+.4f} kN*m")
    print(f"      Vz_i      = {Fz_i:+.4f} kN")
    print(f"      Vz_j      = {fl_BE['Vz_j']:+.4f} kN")

    print(f"\n  Valores en puntos clave:")
    for xL in [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]:
        M_n = momento_interno(xL * L_BE, My_i, Fz_i, L_BE, puntos_carga)
        M_a = momento_ff_analitico(xL * L_BE, L_BE, M_ff_B, R_ff, 25.0, 2.5, 6.4)
        print(f"    x/L={xL:.3f}  M_OpenSees={M_n:+8.3f}  M_analitico={M_a:+8.3f}")

    print(f"\n  Momento a media luz (x/L=0.500):")
    print(f"    OpenSees (My_i+Fz_i*x+loads): {M_50:+.4f} kN*m")
    print(f"    Analitico ff:                  {M_ff_50:+.4f} kN*m")
    print(f"    Referencia esperada:           ~+78.85 kN*m")
    diff_ff = abs(M_50 - M_ff_50)
    diff_ref = abs(M_50 - 78.85)
    if diff_ff < 2.0:
        print(f"    Diferencia OpenSees vs analitico: {diff_ff:+.4f} kN*m [OK]")
    else:
        print(f"    Diferencia OpenSees vs analitico: {diff_ff:+.4f} kN*m [REVISAR]")
    if diff_ref < 2.0:
        print(f"    Diferencia vs referencia:         {diff_ref:+.4f} kN*m [OK]")
    else:
        print(f"    Diferencia vs referencia:         {diff_ref:+.4f} kN*m [REVISAR]")

    print(f"\n  Condiciones de borde:")
    print(f"    M(0) = {M_numerico[0]:+.4f} kN*m (esperado: {My_i:+.4f})")
    print(f"    M(L) = {M_numerico[-1]:+.4f} kN*m (esperado: {fl_BE['My_j']:+.4f})")

    M_max = np.max(M_numerico)
    xL_max = xL_vals[np.argmax(M_numerico)]
    M_min = np.min(M_numerico)
    xL_min = xL_vals[np.argmin(M_numerico)]
    print(f"    M_max   = {M_max:+.4f} kN*m en x/L = {xL_max:.4f}")
    print(f"    M_min   = {M_min:+.4f} kN*m en x/L = {xL_min:.4f}")

    return {
        'xL': xL_vals.tolist(),
        'M_OpenSees': M_numerico.tolist(),
        'M_ff_analitico': M_ff.tolist(),
        'M_ss': M_ss.tolist(),
        'M_OpenSees_50': float(M_50),
        'M_ss_50': float(M_ss_50),
        'M_ff_analitico_50': float(M_ff_50),
        'M_ff_FEM_B': float(M_ff_B),
        'M_ff_FEM_E': float(M_ff_E),
        'R_ff': float(R_ff),
        'M_max': float(M_max),
        'xL_max': float(xL_max),
        'M_min': float(M_min),
        'xL_min': float(xL_min),
        'My_i': float(My_i),
        'My_j': float(fl_BE['My_j']),
        'Fz_i': float(Fz_i),
        'L': L_BE,
        'n_puntos_carga': len(puntos_carga)
    }

# =============================================================================
# 8b. DIAGRAMAS DE FUERZAS INTERNAS - TODAS LAS VIGAS
# =============================================================================

def calcular_diagramas_vigas(info_cargas, resultados):
    n_pts = 100
    xL_vals = np.linspace(0.0, 1.0, n_pts + 1)

    vigas_info = {
        5:  {'nombre': 'A-B',  'L': 5.0,  'grupo': 'viga_5m'},
        6:  {'nombre': 'B-C',  'L': 5.0,  'grupo': 'viga_5m'},
        7:  {'nombre': 'D-E',  'L': 5.0,  'grupo': 'viga_5m'},
        8:  {'nombre': 'E-F',  'L': 5.0,  'grupo': 'viga_5m'},
        9:  {'nombre': 'A-D',  'L': 8.9,  'grupo': 'viga_8m_ext'},
        10: {'nombre': 'B-E',  'L': 8.9,  'grupo': 'viga_8m_cent'},
        11: {'nombre': 'C-F',  'L': 8.9,  'grupo': 'viga_8m_ext'},
    }

    diagramas = {}
    print("\n=== DIAGRAMAS DE FUERZAS INTERNAS (7 VIGAS) - RECTANGULAR ===")
    print(f"  {'Viga':6s} {'L(m)':5s} {'Carga(kN)':10s} "
          f"{'V_i(kN)':9s} {'V_j(kN)':9s} {'M_i(kN*m)':10s} {'M_j(kN*m)':10s} "
          f"{'M_max(kN*m)':12s} {'x/L_max':8s}")
    print("  " + "-" * 95)

    for tag, info in vigas_info.items():
        nombre = info['nombre']
        L = info['L']
        fl = resultados['fuerzas_locales_elementos'][f'elem_{tag}']
        puntos = info_cargas['cargas_vigas'][info['grupo']]['puntos']

        My_i = fl['My_i']
        Fz_i = fl['Vz_i']

        V_vals = np.array([cortante_interno(xL * L, Fz_i, L, puntos) for xL in xL_vals])
        M_vals = np.array([momento_interno(xL * L, My_i, Fz_i, L, puntos) for xL in xL_vals])

        carga_total = info_cargas['cargas_vigas'][info['grupo']]['integral']

        M_max = float(np.max(M_vals))
        xL_max = float(xL_vals[np.argmax(M_vals)])

        print(f"  {nombre:6s} {L:5.1f} {carga_total:10.2f} "
              f"{V_vals[0]:+9.3f} {V_vals[-1]:+9.3f} "
              f"{M_vals[0]:+10.3f} {M_vals[-1]:+10.3f} "
              f"{M_max:+12.3f} {xL_max:8.4f}")

        diagramas[f'elem_{tag}'] = {
            'tag': tag, 'nombre': nombre, 'L': L,
            'xL': xL_vals.tolist(),
            'V': V_vals.tolist(),
            'M': M_vals.tolist(),
            'carga_total': float(carga_total),
        }

    return diagramas

# =============================================================================
# 8c. VERIFICACION DE EJES LOCALES
# =============================================================================

def verificar_ejes_locales():
    print("\n=== EJES LOCALES (verificacion programatica) ===")
    ejes = {}
    for tag, nombre in [(1, 'Columna A'), (5, 'Vig A-B'), (9, 'Vig A-D')]:
        xax = np.array(eleResponse(tag, 'xaxis'))
        yax = np.array(eleResponse(tag, 'yaxis'))
        zax = np.array(eleResponse(tag, 'zaxis'))
        ejes[tag] = {'xaxis': xax, 'yaxis': yax, 'zaxis': zax}
        print(f"  Elem {tag:2d} ({nombre:12s}):")
        print(f"    local_x = ({xax[0]:+.4f}, {xax[1]:+.4f}, {xax[2]:+.4f})")
        print(f"    local_y = ({yax[0]:+.4f}, {yax[1]:+.4f}, {yax[2]:+.4f})")
        print(f"    local_z = ({zax[0]:+.4f}, {zax[1]:+.4f}, {zax[2]:+.4f})")

    print("\n  Verificacion de carga gravitacional:")
    for tag, nombre in [(5, 'Vig X'), (9, 'Vig Y')]:
        zax = ejes[tag]['zaxis']
        dot = np.dot(zax, np.array([0, 0, 1]))
        if abs(dot - 1.0) < 1e-6:
            print(f"    Elem {tag} ({nombre}): local_z = +Z global -> Pz<0 aplica carga gravedad [OK]")
        elif abs(dot + 1.0) < 1e-6:
            print(f"    Elem {tag} ({nombre}): local_z = -Z global -> Pz>0 aplica carga gravedad")
        else:
            print(f"    Elem {tag} ({nombre}): local_z no es paralelo a Z global, dot={dot:.6f}")

    return ejes

# =============================================================================
# 9. ANALISIS
# =============================================================================

def ejecutar_analisis():
    system('BandGeneral')
    numberer('RCM')
    constraints('Plain')
    integrator('LoadControl', 1.0)
    algorithm('Linear')
    analysis('Static')

    ok = analyze(1)

    if ok == 0:
        print("\nAnalisis completado exitosamente.")
    else:
        print("\nERROR: El analisis fallo.")
        sys.exit(1)

    reactions()
    return ok

# =============================================================================
# 10. EXTRACCION DE RESULTADOS (globales y locales)
# =============================================================================

def extraer_resultados(ejes_locales):
    nodo_tags = {
        'base_A': 1, 'base_C': 3, 'base_D': 4, 'base_F': 6,
        'sup_A': 10, 'sup_B': 11, 'sup_C': 12,
        'sup_D': 13, 'sup_E': 14, 'sup_F': 15
    }

    elem_info = {
        1: 'Col A', 2: 'Col C', 3: 'Col D', 4: 'Col F',
        5: 'Vig A-B L5', 6: 'Vig B-C L5', 7: 'Vig D-E L5', 8: 'Vig E-F L5',
        9: 'Vig A-D L89', 10: 'Vig B-E Rect', 11: 'Vig C-F L89'
    }

    resultados = {
        'desplazamientos': {},
        'reacciones': {},
        'fuerzas_globales_elementos': {},
        'fuerzas_locales_elementos': {},
    }

    print("\n=== DESPLAZAMIENTOS (globales) ===")
    for nombre, tag in nodo_tags.items():
        d = nodeDisp(tag)
        resultados['desplazamientos'][nombre] = {
            'tag': tag, 'UX': d[0], 'UY': d[1], 'UZ': d[2],
            'RX': d[3], 'RY': d[4], 'RZ': d[5]
        }
        print(f"  Nodo {nombre:8s} (tag={tag:2d}): UZ = {d[2]:+.8f} m")

    print("\n=== REACCIONES (en apoyos) ===")
    suma_RZ = 0.0
    for nombre in ['base_A', 'base_C', 'base_D', 'base_F']:
        tag = nodo_tags[nombre]
        r = nodeReaction(tag)
        resultados['reacciones'][nombre] = {
            'tag': tag, 'RX': r[0], 'RY': r[1], 'RZ': r[2],
            'MX': r[3], 'MY': r[4], 'MZ': r[5]
        }
        suma_RZ += r[2]
        print(f"  Nodo {nombre:8s}: RX={r[0]:+.4f}  RY={r[1]:+.4f}  RZ={r[2]:+.4f}  "
              f"MX={r[3]:+.4f}  MY={r[4]:+.4f}  MZ={r[5]:+.4f}")

    print(f"\n  Suma RZ = {suma_RZ:+.6f} kN (esperado: +445.00)")
    print(f"  Error   = {abs(suma_RZ - 445.0):.6f} kN")

    print("\n=== FUERZAS DE ELEMENTOS ===")

    for tag in range(1, 12):
        f_global = np.array(eleForce(tag))

        xax = np.array(eleResponse(tag, 'xaxis'))
        yax = np.array(eleResponse(tag, 'yaxis'))
        zax = np.array(eleResponse(tag, 'zaxis'))
        R = np.array([xax, yax, zax])

        Fg_i = f_global[0:3]
        Mg_i = f_global[3:6]
        Fg_j = f_global[6:9]
        Mg_j = f_global[9:12]

        Fl_i = R @ Fg_i
        Ml_i = R @ Mg_i
        Fl_j = R @ Fg_j
        Ml_j = R @ Mg_j

        resultados['fuerzas_globales_elementos'][f'elem_{tag}'] = {
            'tag': tag, 'nombre': elem_info[tag],
            'FX_i': float(f_global[0]), 'FY_i': float(f_global[1]), 'FZ_i': float(f_global[2]),
            'MX_i': float(f_global[3]), 'MY_i': float(f_global[4]), 'MZ_i': float(f_global[5]),
            'FX_j': float(f_global[6]), 'FY_j': float(f_global[7]), 'FZ_j': float(f_global[8]),
            'MX_j': float(f_global[9]), 'MY_j': float(f_global[10]), 'MZ_j': float(f_global[11])
        }

        resultados['fuerzas_locales_elementos'][f'elem_{tag}'] = {
            'tag': tag, 'nombre': elem_info[tag],
            'N_i': float(Fl_i[0]), 'Vy_i': float(Fl_i[1]), 'Vz_i': float(Fl_i[2]),
            'T_i': float(Ml_i[0]), 'My_i': float(Ml_i[1]), 'Mz_i': float(Ml_i[2]),
            'N_j': float(Fl_j[0]), 'Vy_j': float(Fl_j[1]), 'Vz_j': float(Fl_j[2]),
            'T_j': float(Ml_j[0]), 'My_j': float(Ml_j[1]), 'Mz_j': float(Ml_j[2])
        }

    print("\n  Fuerzas GLOBALES (extremo i):")
    print(f"  {'Elem':5s} {'Nombre':12s} {'FX':>10s} {'FY':>10s} {'FZ':>10s} "
          f"{'MX':>10s} {'MY':>10s} {'MZ':>10s}")
    print("  " + "-" * 88)
    for tag in range(1, 12):
        fg = resultados['fuerzas_globales_elementos'][f'elem_{tag}']
        print(f"  {tag:5d} {fg['nombre']:12s} "
              f"{fg['FX_i']:+10.4f} {fg['FY_i']:+10.4f} {fg['FZ_i']:+10.4f} "
              f"{fg['MX_i']:+10.4f} {fg['MY_i']:+10.4f} {fg['MZ_i']:+10.4f}")

    print("\n  Fuerzas LOCALES (extremo i):")
    print(f"  {'Elem':5s} {'Nombre':12s} {'N':>10s} {'Vy':>10s} {'Vz':>10s} "
          f"{'T':>10s} {'My':>10s} {'Mz':>10s}")
    print("  " + "-" * 78)
    for tag in range(1, 12):
        fl = resultados['fuerzas_locales_elementos'][f'elem_{tag}']
        print(f"  {tag:5d} {fl['nombre']:12s} "
              f"{fl['N_i']:+10.4f} {fl['Vy_i']:+10.4f} {fl['Vz_i']:+10.4f} "
              f"{fl['T_i']:+10.4f} {fl['My_i']:+10.4f} {fl['Mz_i']:+10.4f}")

    return resultados

# =============================================================================
# 11. DIAGNOSTICO FINAL
# =============================================================================

def imprimir_diagnostico(resultados, info_cargas, diagrama_BE):
    print("\n" + "=" * 65)
    print("  DIAGNOSTICO DE VERIFICACION - VERSION RECTANGULAR")
    print("=" * 65)

    fl_A = resultados['fuerzas_locales_elementos']['elem_1']
    fg_A = resultados['fuerzas_globales_elementos']['elem_1']
    print(f"\n  COLUMNA A (elem 1):")
    print(f"    Axial local  N_i = {fl_A['N_i']:+.4f} kN")
    print(f"    Global:  FX={fg_A['FX_i']:+.4f}  FY={fg_A['FY_i']:+.4f}  FZ={fg_A['FZ_i']:+.4f}")

    if abs(abs(fl_A['N_i']) - 111.25) < 1.0:
        print(f"    |N_local| = {abs(fl_A['N_i']):.4f} ~ 111.25 kN [OK]")
    else:
        print(f"    |N_local| = {abs(fl_A['N_i']):.4f} NO ~ 111.25 kN [PROBLEMA]")

    fl_BE = resultados['fuerzas_locales_elementos']['elem_10']
    fg_BE = resultados['fuerzas_globales_elementos']['elem_10']
    print(f"\n  VIGA B-E (elem 10) - EMPOTRADO-EMPOTRADO (RECTANGULAR):")
    print(f"    Carga total: 160.00 kN")
    print(f"    Local:  N_i={fl_BE['N_i']:+.4f}  Vy_i={fl_BE['Vy_i']:+.4f}  Vz_i={fl_BE['Vz_i']:+.4f}")
    print(f"            My_i={fl_BE['My_i']:+.4f}  Mz_i={fl_BE['Mz_i']:+.4f}")
    print(f"            N_j={fl_BE['N_j']:+.4f}  Vy_j={fl_BE['Vy_j']:+.4f}  Vz_j={fl_BE['Vz_j']:+.4f}")
    print(f"            My_j={fl_BE['My_j']:+.4f}  Mz_j={fl_BE['Mz_j']:+.4f}")

    VzBE_total = fl_BE['Vz_i'] + fl_BE['Vz_j']
    print(f"\n    Cortante total Vz_i+Vz_j = {VzBE_total:+.4f} kN (esperado: 160.00)")
    if abs(VzBE_total - 160.0) < 0.01:
        print(f"    Cortantes verificados [OK]")
    else:
        print(f"    ERROR en cortantes")

    print(f"\n    Momentos de empotramiento:")
    print(f"      My_i = {fl_BE['My_i']:+.4f} kN*m (ref: -142.64)")
    print(f"      My_j = {fl_BE['My_j']:+.4f} kN*m (ref: +142.64)")
    if abs(abs(fl_BE['My_i']) - 142.64) < 2.0:
        print(f"      Magnitudes OK [OK]")
    else:
        print(f"      Magnitudes NO coinciden [REVISAR]")

    print(f"\n    MOMENTO A MEDIA LUZ (x/L=0.500):")
    print(f"      FEM (My_i+Fz_i*x+loads):   {diagrama_BE['M_OpenSees_50']:+.4f} kN*m")
    print(f"      Analitico ff (referencia):  {diagrama_BE['M_ff_analitico_50']:+.4f} kN*m")
    print(f"      Referencia esperada:        ~+78.85 kN*m")
    diff_ref = abs(diagrama_BE['M_OpenSees_50'] - 78.85)
    if diff_ref < 2.0:
        print(f"      Diferencia vs ref:          {diff_ref:+.4f} kN*m [OK]")
    else:
        print(f"      Diferencia vs ref:          {diff_ref:+.4f} kN*m [REVISAR]")

    desp_B = resultados['desplazamientos']['sup_B']
    desp_E = resultados['desplazamientos']['sup_E']
    print(f"\n    Desplazamientos: UZ_B = {desp_B['UZ']:+.8f} m")
    print(f"                     UZ_E = {desp_E['UZ']:+.8f} m")
    print(f"    Rotaciones:      RX_B = {desp_B['RX']:+.8f} rad (esperado: 0)")
    print(f"                     RX_E = {desp_E['RX']:+.8f} rad (esperado: 0)")

    suma_RZ = sum(r['RZ'] for r in resultados['reacciones'].values())
    print(f"\n  EQUILIBRIO GLOBAL:")
    print(f"    Carga total:     {info_cargas['carga_total']:.2f} kN")
    print(f"    Suma RZ:         {suma_RZ:+.6f} kN")
    print(f"    Residual:        {abs(suma_RZ - info_cargas['carga_total']):.6f} kN")

# =============================================================================
# 12. GUARDAR RESULTADOS
# =============================================================================

def guardar_resultados(resultados, info_cargas, diagrama_BE, diagramas_vigas):
    resultados['cargas_elementos'] = info_cargas['cargas_vigas']
    resultados['diagrama_momento_BE'] = diagrama_BE
    resultados['diagramas_vigas'] = diagramas_vigas
    resultados['verificaciones'] = {
        'carga_total_kN': info_cargas['carga_total'],
        'suma_RZ_kN': sum(r['RZ'] for r in resultados['reacciones'].values()),
        'equilibrio': abs(sum(r['RZ'] for r in resultados['reacciones'].values()) - 445.0) < 0.01,
        'Vz_BE_total': resultados['fuerzas_locales_elementos']['elem_10']['Vz_i']
                       + resultados['fuerzas_locales_elementos']['elem_10']['Vz_j'],
        'My_i_BE': resultados['fuerzas_locales_elementos']['elem_10']['My_i'],
        'My_j_BE': resultados['fuerzas_locales_elementos']['elem_10']['My_j'],
        'M_medialuz_FEM': diagrama_BE['M_OpenSees_50'],
        'M_medialuz_ff_ref': diagrama_BE['M_ff_analitico_50'],
        'M_medialuz_referencia': 78.85,
    }

    ruta = Path(__file__).parent / 'resultados_rectangular' / 'resultados.json'
    with open(ruta, 'w') as f:
        json.dump(resultados, f, indent=2)
    print(f"\nResultados guardados en: {ruta}")

# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def main():
    wipe()

    print("=" * 65)
    print("  MODELO OPENSEESPY - BENCHMARK 3D RECTANGULAR SEMANA 1 MCOC")
    print("=" * 65)

    ruta_datos = Path(__file__).parent / 'datos_entrada.json'
    datos = cargar_datos(ruta_datos)

    model('basic', '-ndm', 3, '-ndf', 6)

    crear_nodos(datos)
    E, G = crear_material(datos)
    crear_secciones(E, G, datos)
    crear_transformaciones()
    crear_elementos()
    aplicar_apoyos()
    aplicar_restricciones_RX()
    info_cargas = crear_cargas()
    ejes = verificar_ejes_locales()
    ejecutar_analisis()

    resultados = extraer_resultados(ejes)
    diagrama_BE = calcular_diagrama_BE(info_cargas, resultados)
    diagramas_vigas = calcular_diagramas_vigas(info_cargas, resultados)
    imprimir_diagnostico(resultados, info_cargas, diagrama_BE)
    guardar_resultados(resultados, info_cargas, diagrama_BE, diagramas_vigas)

    print("\n" + "=" * 65)
    print("  ANALISIS RECTANGULAR COMPLETADO")
    print("=" * 65)

    return 0

if __name__ == "__main__":
    main()

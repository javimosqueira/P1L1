"""
VISUALIZACION - BENCHMARK RECTANGULAR 3D SEMANA 1 MCOC
=====================================================
Visualizacion de geometria, ejes locales y cargas
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pathlib import Path

def cargar_datos(ruta_datos):
    with open(ruta_datos, 'r') as f:
        return json.load(f)

def visualizar_modelo(datos):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    nodos_base = datos['nodos']['base']
    nodos_sup = datos['nodos']['superior']
    
    for nombre, coord in nodos_base.items():
        ax.scatter(coord[0], coord[1], coord[2], c='red', s=100, marker='o')
        ax.text(coord[0], coord[1], coord[2]-0.3, f'Base {nombre}', fontsize=8)
    
    for nombre, coord in nodos_sup.items():
        ax.scatter(coord[0], coord[1], coord[2], c='blue', s=100, marker='o')
        ax.text(coord[0], coord[1], coord[2]+0.2, f'Sup {nombre}', fontsize=8)
    
    for nombre in ['A', 'C', 'D', 'F']:
        base = nodos_base[nombre]
        sup = nodos_sup[nombre]
        ax.plot([base[0], sup[0]], [base[1], sup[1]], [base[2], sup[2]], 
                'r-', linewidth=3, label='Columna P70x70' if nombre == 'A' else '')
    
    vigas_x = [('A', 'B'), ('B', 'C'), ('D', 'E'), ('E', 'F')]
    for i, (v1, v2) in enumerate(vigas_x):
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                'b-', linewidth=2, label='Viga RECT 5.00m' if i == 0 else '')
    
    vigas_y_borde = [('A', 'D'), ('C', 'F')]
    for i, (v1, v2) in enumerate(vigas_y_borde):
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                'g-', linewidth=2, label='Viga RECT 8.90m' if i == 0 else '')
    
    p1 = nodos_sup['B']
    p2 = nodos_sup['E']
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
            'm-', linewidth=2, label='Viga RECT 8.90m central')
    
    panel_izq = [nodos_sup['A'], nodos_sup['B'], nodos_sup['E'], nodos_sup['D']]
    poly_izq = Poly3DCollection([panel_izq], alpha=0.3, facecolor='cyan', edgecolor='blue')
    ax.add_collection3d(poly_izq)
    
    panel_der = [nodos_sup['B'], nodos_sup['C'], nodos_sup['F'], nodos_sup['E']]
    poly_der = Poly3DCollection([panel_der], alpha=0.3, facecolor='cyan', edgecolor='blue')
    ax.add_collection3d(poly_der)
    
    ax.quiver(0, 0, 0, 2, 0, 0, color='red', arrow_length_ratio=0.2, linewidth=2)
    ax.text(2.2, 0, 0, 'X', fontsize=12, color='red')
    ax.quiver(0, 0, 0, 0, 2, 0, color='green', arrow_length_ratio=0.2, linewidth=2)
    ax.text(0, 2.2, 0, 'Y', fontsize=12, color='green')
    ax.quiver(0, 0, 0, 0, 0, 2, color='blue', arrow_length_ratio=0.2, linewidth=2)
    ax.text(0, 0, 2.2, 'Z', fontsize=12, color='blue')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Benchmark RECTANGULAR 3D - Semana 1 MCOC\n10 nodos, 11 elementos - Vigas 0.60x0.80m')
    
    ax.legend(loc='upper left')
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos_rectangular' / 'geometria_3d.png', dpi=150, bbox_inches='tight')
    plt.close()

def visualizar_planta(datos):
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    nodos_sup = datos['nodos']['superior']
    
    for nombre, coord in nodos_sup.items():
        ax.plot(coord[0], coord[1], 'ko', markersize=8)
        ax.text(coord[0]+0.2, coord[1]+0.2, nombre, fontsize=10)
    
    vigas_x = [('A', 'B'), ('B', 'C'), ('D', 'E'), ('E', 'F')]
    for v1, v2 in vigas_x:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=2)
    
    vigas_y_borde = [('A', 'D'), ('C', 'F')]
    for v1, v2 in vigas_y_borde:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'g-', linewidth=2)
    
    p1 = nodos_sup['B']
    p2 = nodos_sup['E']
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'm-', linewidth=2)
    
    panel_izq_x = [nodos_sup['A'][0], nodos_sup['B'][0], 
                   nodos_sup['E'][0], nodos_sup['D'][0], nodos_sup['A'][0]]
    panel_izq_y = [nodos_sup['A'][1], nodos_sup['B'][1], 
                   nodos_sup['E'][1], nodos_sup['D'][1], nodos_sup['A'][1]]
    ax.fill(panel_izq_x, panel_izq_y, alpha=0.3, color='cyan', label='Panel izquierdo')
    
    panel_der_x = [nodos_sup['B'][0], nodos_sup['C'][0], 
                   nodos_sup['F'][0], nodos_sup['E'][0], nodos_sup['B'][0]]
    panel_der_y = [nodos_sup['B'][1], nodos_sup['C'][1], 
                   nodos_sup['F'][1], nodos_sup['E'][1], nodos_sup['B'][1]]
    ax.fill(panel_der_x, panel_der_y, alpha=0.3, color='cyan', label='Panel derecho')
    
    ax.annotate('', xy=(2, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(2.2, 0, 'X', fontsize=12, color='red')
    ax.annotate('', xy=(0, 2), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(0, 2.2, 'Y', fontsize=12, color='green')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Planta del Benchmark RECTANGULAR 3D\nVigas 0.60x0.80m')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.legend()
    
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 10)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos_rectangular' / 'planta.png', dpi=150, bbox_inches='tight')
    plt.close()

def visualizar_cargas(datos):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    ax1 = axes[0, 0]
    x = np.linspace(0, 5, 100)
    w = 12.5 * (1 - np.abs(x - 2.5) / 2.5)
    ax1.fill_between(x, w, alpha=0.3, color='blue')
    ax1.plot(x, w, 'b-', linewidth=2)
    ax1.set_xlabel('Posicion (m)')
    ax1.set_ylabel('Carga (kN/m)')
    ax1.set_title('Distribucion triangular - Vigas de 5m\n(A-B, B-C, D-E, E-F)')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 5)
    ax1.set_ylim(0, 15)
    ax1.text(2.5, 13, 'w_max = 12.50 kN/m', ha='center')
    ax1.text(2.5, 7, 'Area = 31.25 kN', ha='center')
    
    ax2 = axes[0, 1]
    x = np.linspace(0, 8.9, 100)
    w = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi < 2.5:
            w[i] = 12.5 * xi / 2.5
        elif xi < 6.4:
            w[i] = 12.5
        else:
            w[i] = 12.5 * (8.9 - xi) / 2.5
    ax2.fill_between(x, w, alpha=0.3, color='green')
    ax2.plot(x, w, 'g-', linewidth=2)
    ax2.set_xlabel('Posicion (m)')
    ax2.set_ylabel('Carga (kN/m)')
    ax2.set_title('Distribucion trapezoidal - Vigas de 8.9m\n(A-D, C-F)')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 8.9)
    ax2.set_ylim(0, 15)
    ax2.text(4.45, 13, 'w_max = 12.50 kN/m', ha='center')
    ax2.text(4.45, 7, 'Area = 80.00 kN', ha='center')
    
    ax3 = axes[1, 0]
    x = np.linspace(0, 8.9, 100)
    w = np.zeros_like(x)
    for i, xi in enumerate(x):
        if xi < 2.5:
            w[i] = 25.0 * xi / 2.5
        elif xi < 6.4:
            w[i] = 25.0
        else:
            w[i] = 25.0 * (8.9 - xi) / 2.5
    ax3.fill_between(x, w, alpha=0.3, color='red')
    ax3.plot(x, w, 'r-', linewidth=2)
    ax3.set_xlabel('Posicion (m)')
    ax3.set_ylabel('Carga (kN/m)')
    ax3.set_title('Distribucion trapezoidal doble - Viga central B-E')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 8.9)
    ax3.set_ylim(0, 30)
    ax3.text(4.45, 27, 'w_max = 25.00 kN/m', ha='center')
    ax3.text(4.45, 13, 'Area = 160.00 kN', ha='center')
    
    ax4 = axes[1, 1]
    vigas = ['A-D', 'B-E', 'C-F', 'A-B', 'B-C', 'D-E', 'E-F']
    cargas = [80.0, 160.0, 80.0, 31.25, 31.25, 31.25, 31.25]
    colores = ['green', 'red', 'green', 'blue', 'blue', 'blue', 'blue']
    
    bars = ax4.bar(vigas, cargas, color=colores, alpha=0.7)
    ax4.set_xlabel('Viga')
    ax4.set_ylabel('Carga total (kN)')
    ax4.set_title('Resumen de cargas por viga')
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, carga in zip(bars, cargas):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{carga:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos_rectangular' / 'cargas.png', dpi=150, bbox_inches='tight')
    plt.close()

def visualizar_ejes_locales(datos):
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    nodos_sup = datos['nodos']['superior']
    nodos_base = datos['nodos']['base']
    
    for nombre in ['A', 'C', 'D', 'F']:
        base = nodos_base[nombre]
        sup = nodos_sup[nombre]
        ax.plot([base[0], sup[0]], [base[1], sup[1]], [base[2], sup[2]], 
                'r-', linewidth=3)
    
    vigas_x = [('A', 'B'), ('B', 'C'), ('D', 'E'), ('E', 'F')]
    for v1, v2 in vigas_x:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'b-', linewidth=2)
    
    vigas_y_borde = [('A', 'D'), ('C', 'F')]
    for v1, v2 in vigas_y_borde:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'g-', linewidth=2)
    
    p1 = nodos_sup['B']
    p2 = nodos_sup['E']
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'm-', linewidth=2)
    
    longitud_flecha = 0.5
    for nombre in ['A', 'C', 'D', 'F']:
        base = nodos_base[nombre]
        sup = nodos_sup[nombre]
        medio = [(base[i] + sup[i])/2 for i in range(3)]
        ax.quiver(medio[0], medio[1], medio[2], 0, 0, longitud_flecha, 
                 color='red', arrow_length_ratio=0.3, linewidth=2)
        ax.quiver(medio[0], medio[1], medio[2], longitud_flecha, 0, 0, 
                 color='green', arrow_length_ratio=0.3, linewidth=2)
        ax.quiver(medio[0], medio[1], medio[2], 0, longitud_flecha, 0, 
                 color='blue', arrow_length_ratio=0.3, linewidth=2)
    
    for v1, v2 in vigas_x:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        medio = [(p1[i] + p2[i])/2 for i in range(3)]
        dx = p2[0] - p1[0]
        longitud = np.sqrt(dx**2)
        ax.quiver(medio[0], medio[1], medio[2], dx/longitud*longitud_flecha, 0, 0, 
                 color='red', arrow_length_ratio=0.3, linewidth=2)
        ax.quiver(medio[0], medio[1], medio[2], 0, 0, longitud_flecha, 
                 color='blue', arrow_length_ratio=0.3, linewidth=2)
        ax.quiver(medio[0], medio[1], medio[2], 0, longitud_flecha, 0, 
                 color='green', arrow_length_ratio=0.3, linewidth=2)
    
    vigas_y_todas = vigas_y_borde + [('B', 'E')]
    for v1, v2 in vigas_y_todas:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        medio = [(p1[i] + p2[i])/2 for i in range(3)]
        dy = p2[1] - p1[1]
        longitud = np.sqrt(dy**2)
        ax.quiver(medio[0], medio[1], medio[2], 0, dy/longitud*longitud_flecha, 0, 
                 color='red', arrow_length_ratio=0.3, linewidth=2)
        ax.quiver(medio[0], medio[1], medio[2], longitud_flecha, 0, 0, 
                 color='green', arrow_length_ratio=0.3, linewidth=2)
        ax.quiver(medio[0], medio[1], medio[2], 0, 0, longitud_flecha, 
                 color='blue', arrow_length_ratio=0.3, linewidth=2)
    
    ax.quiver(0, 0, 0, 2, 0, 0, color='red', arrow_length_ratio=0.2, linewidth=3)
    ax.text(2.2, 0, 0, 'X global', fontsize=12, color='red')
    ax.quiver(0, 0, 0, 0, 2, 0, color='green', arrow_length_ratio=0.2, linewidth=3)
    ax.text(0, 2.2, 0, 'Y global', fontsize=12, color='green')
    ax.quiver(0, 0, 0, 0, 0, 2, color='blue', arrow_length_ratio=0.2, linewidth=3)
    ax.text(0, 0, 2.2, 'Z global', fontsize=12, color='blue')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Ejes Locales de los Elementos - RECTANGULAR\nRojo: local x | Verde: local y | Azul: local z')
    
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos_rectangular' / 'ejes_locales.png', dpi=150, bbox_inches='tight')
    plt.close()

def visualizar_diagramas_vigas(resultados):
    diagramas = resultados.get('diagramas_vigas', {})
    if not diagramas:
        print("  [AVISO] No hay datos de diagramas_vigas en resultados.json")
        return
    
    orden = ['elem_5', 'elem_6', 'elem_7', 'elem_8', 'elem_9', 'elem_10', 'elem_11']
    etiquetas = {
        'elem_5': 'A-B  (5.0m, RECT)',
        'elem_6': 'B-C  (5.0m, RECT)',
        'elem_7': 'D-E  (5.0m, RECT)',
        'elem_8': 'E-F  (5.0m, RECT)',
        'elem_9': 'A-D  (8.9m, RECT)',
        'elem_10': 'B-E  (8.9m, RECT)',
        'elem_11': 'C-F (8.9m, RECT)',
    }
    
    colores = {
        'elem_5': '#1f77b4', 'elem_6': '#ff7f0e',
        'elem_7': '#1f77b4', 'elem_8': '#ff7f0e',
        'elem_9': '#2ca02c', 'elem_10': '#d62728',
        'elem_11': '#2ca02c',
    }
    
    fig, axes = plt.subplots(7, 2, figsize=(14, 20), sharex='col')
    
    for row, key in enumerate(orden):
        d = diagramas[key]
        xL = np.array(d['xL'])
        V = np.array(d['V'])
        M = np.array(d['M'])
        L = d['L']
        x = xL * L
        nombre = etiquetas[key]
        color = colores[key]
        
        ax_v = axes[row, 0]
        ax_v.fill_between(x, V, alpha=0.25, color=color)
        ax_v.plot(x, V, color=color, linewidth=1.5)
        ax_v.axhline(0, color='k', linewidth=0.5)
        ax_v.set_ylabel('V (kN)', fontsize=9)
        ax_v.set_title(f'{nombre}', fontsize=10, fontweight='bold', loc='left')
        ax_v.grid(True, alpha=0.3)
        ax_v.set_xlim(0, L)
        ax_v.text(0.02 * L, V[0], f' {V[0]:+.1f}', fontsize=7,
                  va='bottom' if V[0] >= 0 else 'top')
        ax_v.text(L * 0.98, V[-1], f'{V[-1]:+.1f} ', fontsize=7,
                  va='bottom' if V[-1] >= 0 else 'top', ha='right')
        
        ax_m = axes[row, 1]
        ax_m.fill_between(x, M, alpha=0.25, color=color)
        ax_m.plot(x, M, color=color, linewidth=1.5)
        ax_m.axhline(0, color='k', linewidth=0.5)
        ax_m.set_ylabel('M (kN*m)', fontsize=9)
        ax_m.set_title(f'{nombre}', fontsize=10, fontweight='bold', loc='left')
        ax_m.grid(True, alpha=0.3)
        ax_m.set_xlim(0, L)
        
        M_max = float(np.max(M))
        M_min = float(np.min(M))
        idx_max = int(np.argmax(M))
        idx_min = int(np.argmin(M))
        
        if abs(M_max) > 1.0:
            offset_y = M_max * 1.2 if M_max > 0 else M_max * 1.4
            ax_m.annotate(f'{M_max:+.1f}', xy=(x[idx_max], M_max),
                         xytext=(x[idx_max], offset_y),
                         fontsize=7, ha='center', fontweight='bold',
                         arrowprops=dict(arrowstyle='->', color=color, lw=0.8))
        if abs(M_min) > 1.0:
            offset_y = M_min * 1.2 if M_min < 0 else M_min * 1.4
            ax_m.annotate(f'{M_min:+.1f}', xy=(x[idx_min], M_min),
                         xytext=(x[idx_min], offset_y),
                         fontsize=7, ha='center', fontweight='bold',
                         arrowprops=dict(arrowstyle='->', color=color, lw=0.8))
    
    axes[-1, 0].set_xlabel('x (m)', fontsize=10)
    axes[-1, 1].set_xlabel('x (m)', fontsize=10)
    
    axes[0, 0].set_title('Cortante V(x) - Local Z', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Momento My(x) - Flexion', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos_rectangular' / 'diagramas_fuerzas.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("  Guardado: graficos_rectangular/diagramas_fuerzas.png")

    d_BE = diagramas.get('elem_10', None)
    if d_BE:
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        xL = np.array(d_BE['xL'])
        M = np.array(d_BE['M'])
        L_BE = d_BE['L']
        x = xL * L_BE

        ax.fill_between(x, M, alpha=0.2, color='#d62728')
        ax.plot(x, M, color='#d62728', linewidth=2, label='OpenSees (FEM)')
        ax.axhline(0, color='k', linewidth=0.5)
        ax.set_xlabel('x (m)', fontsize=11)
        ax.set_ylabel('My (kN*m)', fontsize=11)
        ax.set_title('Momento flector Viga B-E (elem 10) - RECTANGULAR\n'
                     'Trapezoidal 160 kN, L=8.9m',
                     fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)

        M_max = float(np.max(M))
        M_min = float(np.min(M))
        idx_max = int(np.argmax(M))
        idx_min = int(np.argmin(M))

        ax.annotate(f'M_max = {M_max:+.2f} kN*m', xy=(x[idx_max], M_max),
                    xytext=(x[idx_max] + 1.0, M_max + 15),
                    fontsize=9, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='black', lw=1))
        ax.annotate(f'M_min = {M_min:+.2f} kN*m', xy=(x[idx_min], M_min),
                    xytext=(x[idx_min] + 1.0, M_min - 15),
                    fontsize=9, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='black', lw=1))

        plt.tight_layout()
        plt.savefig(Path(__file__).parent / 'graficos_rectangular' / 'momento_BE.png',
                    dpi=150, bbox_inches='tight')
        plt.close()
        print("  Guardado: graficos_rectangular/momento_BE.png")

def hermite(t, L):
    """Funciones de forma de Hermite (viga Euler-Bernoulli) en t=s/L."""
    t2 = t * t
    t3 = t2 * t
    N1 = 1.0 - 3.0 * t2 + 2.0 * t3
    N2 = L * (t - 2.0 * t2 + t3)
    N3 = 3.0 * t2 - 2.0 * t3
    N4 = L * (-t2 + t3)
    return N1, N2, N3, N4


def construir_R(x_eje, vecz):
    """
    Matriz de rotacion global->local de un elemento, siguiendo la convencion
    de OpenSees geomTransf: local_z ~ vecz (ortogonalizado) y local_y = z x x.
    """
    L = np.linalg.norm(x_eje)
    x = x_eje / L
    v = np.array(vecz, dtype=float)
    z = v - np.dot(x, v) * x        # ortogonalizar vecz respecto al eje x
    z = z / np.linalg.norm(z)
    y = np.cross(z, x)
    return np.vstack([x, y, z])


def elastica_con_carga(fuerzas, puntos, EI, L, wi, wj, n_pts=80):
    """
    Reconstruye la deformada transversal (en el plano de flexion vertical)
    de una viga con carga usando doble integracion de la curvatura.

    M(x) = My_i + Vz_i*x - sum(P_k*(x-s_k))
    curv = M/EI
    v''(x) generada por la carga; luego se ajustan 2 constantes para que
    v(0)=wi y v(L)=wj (desplazamientos nodales reales).

    Devuelve array v(s) con los desplazamientos transversales (local z).
    """
    x_vals = np.linspace(0, L, n_pts)
    s_pos = np.array([p['x/L'] * L for p in puntos])
    P_vals = np.array([p['P'] for p in puntos])

    My_i = fuerzas['My_i']
    Vz_i = fuerzas['Vz_i']

    # M(x) e integrandos
    M = np.zeros(n_pts)
    for idx, x in enumerate(x_vals):
        M[idx] = My_i + Vz_i * x
        sel = s_pos < x - 1e-9
        if np.any(sel):
            M[idx] -= np.sum(P_vals[sel] * (x - s_pos[sel]))

    curva = M / EI          # curvatura (1/m)
    # g(x) = integral de curva de 0 a x (trapezoidal acumulada)
    g = np.concatenate([[0.0], np.cumsum(0.5 * (curva[1:] + curva[:-1]) * (x_vals[1:] - x_vals[:-1]))])
    # doble integral h(x) = integral de g de 0 a x
    h = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * (x_vals[1:] - x_vals[:-1]))])

    # v(x) = C0 + C1*x + h(x)   -> v(0)=wi => C0=wi ; v(L)=wj => C1=(wj - wi - h[L])/L
    C0 = wi
    C1 = (wj - wi - h[-1]) / L
    v = C0 + C1 * x_vals + h
    return x_vals, v


def curvas_deformadas(datos, resultados, factor_escala):
    """
    Reconstruye la elastica completa de vigas (integrando la carga) y de
    columnas (Hermite con giros nodales), proyectando en coordenadas globales.
    """
    nodos_base = datos['nodos']['base']
    nodos_sup = datos['nodos']['superior']
    desp = resultados['desplazamientos']

    E = datos['materiales']['concreto']['E']
    # Flexion vertical 3D usa Iy (todos los elementos con Iy de su seccion)
    Iy = datos['secciones']['viga_T_interior']['Iy']
    EI = E * Iy

    nodos = {}
    for nombre, c in nodos_base.items():
        nodos['base_' + nombre] = (np.array(c, dtype=float),
                                   np.array([desp['base_' + nombre][k] for k in
                                             ['UX', 'UY', 'UZ', 'RX', 'RY', 'RZ']]))
    for nombre, c in nodos_sup.items():
        nodos['sup_' + nombre] = (np.array(c, dtype=float),
                                  np.array([desp['sup_' + nombre][k] for k in
                                            ['UX', 'UY', 'UZ', 'RX', 'RY', 'RZ']]))

    # tag -> (nombre_ni, nombre_nj, vecz, tipo, grupo_carga)
    defs = {
        1: ('base_A', 'sup_A', (0, 1, 0), 'col', None),
        2: ('base_C', 'sup_C', (0, 1, 0), 'col', None),
        3: ('base_D', 'sup_D', (0, 1, 0), 'col', None),
        4: ('base_F', 'sup_F', (0, 1, 0), 'col', None),
        5: ('sup_A', 'sup_B', (0, 0, 1), 'viga', 'viga_5m'),
        6: ('sup_B', 'sup_C', (0, 0, 1), 'viga', 'viga_5m'),
        7: ('sup_D', 'sup_E', (0, 0, 1), 'viga', 'viga_5m'),
        8: ('sup_E', 'sup_F', (0, 0, 1), 'viga', 'viga_5m'),
        9: ('sup_A', 'sup_D', (0, 0, 1), 'viga', 'viga_8m_ext'),
        10: ('sup_B', 'sup_E', (0, 0, 1), 'viga', 'viga_8m_cent'),
        11: ('sup_C', 'sup_F', (0, 0, 1), 'viga', 'viga_8m_ext'),
    }

    ligas_orig = []
    curvas_def = []
    puntos_def = []
    n_pts = 80

    for tag, (ni, nj, vecz, tipo, grupo) in defs.items():
        Pi, Ui = nodos[ni]
        Pj, Uj = nodos[nj]
        ligas_orig.append((Pi, Pj))

        x_eje = Pj - Pi
        L = np.linalg.norm(x_eje)
        R = construir_R(x_eje, vecz)

        fu = resultados['fuerzas_locales_elementos'][f'elem_{tag}']
        # desplazamientos reales (escala 1) en local
        d_i = np.array([Ui[0], Ui[1], Ui[2]])
        d_j = np.array([Uj[0], Uj[1], Uj[2]])
        u_i = R @ d_i
        u_j = R @ d_j
        wx_i, wy_i, wz_i = u_i   # local: x=axial, y, z
        wx_j, wy_j, wz_j = u_j

        if tipo == 'viga' and grupo in resultados['cargas_elementos']:
            puntos = resultados['cargas_elementos'][grupo]['puntos']
            x_vals, v_local = elastica_con_carga(fu, puntos, EI, L, wz_i, wz_j, n_pts)
            # deformacion axial y en local y (lineal, despreciables)
            ux_loc = wx_i + (wx_j - wx_i) * (x_vals / L)
            uy_loc = wy_i + (wy_j - wy_i) * (x_vals / L)
            u_local = np.column_stack([ux_loc, uy_loc, v_local])
        else:
            # columnas: Hermite con giros nodales reales (escala 1)
            th_i = R @ np.array(Ui[3:6])
            th_j = R @ np.array(Uj[3:6])
            ux_i, v_i, w_i = u_i
            ux_j, v_j, w_j = u_j
            thx_i, thy_i, thz_i = th_i
            thx_j, thy_j, thz_j = th_j
            t_vals = np.linspace(0, 1, n_pts)
            u_local = np.zeros((n_pts, 3))
            for idx, t in enumerate(t_vals):
                N1, N2, N3, N4 = hermite(t, L)
                u_local[idx, 0] = ux_i + (ux_j - ux_i) * t
                u_local[idx, 1] = N1 * v_i + N2 * thz_i + N3 * v_j + N4 * thz_j
                u_local[idx, 2] = N1 * w_i + N2 * (-thy_i) + N3 * w_j + N4 * (-thy_j)

        # punto sobre eje original
        t_axis = np.linspace(0, 1, u_local.shape[0])
        P_eje = Pi[None, :] + (Pj - Pi)[None, :] * t_axis[:, None]
        # desplazamiento total = (curva elastica - elongacion axial lineal ya incluida)*escala
        P_def = P_eje + (u_local * factor_escala) @ R
        curvas_def.append(P_def)

        puntos_def.append(P_def[0])
        # asegurar que el extremo j quede registrado
        if tag in [4, 8, 11]:
            puntos_def.append(P_def[-1])

    return ligas_orig, curvas_def, puntos_def


def visualizar_deformada(datos, resultados, factor_escala=500, nombre_archivo='deformada.png'):
    """
    Visualiza la estructura original y deformada tras aplicar cargas,
    reconstruyendo la elastica completa (curvas de Hermite) de cada viga.

    factor_escala: amplificacion de los desplazamientos para hacer visible
    la deformacion (el valor real del desplazamiento maximo es ~1-2 mm).
    nombre_archivo: nombre del PNG a guardar en graficos_rectangular/.
    """
    ligas_orig, curvas_def, puntos_def = curvas_deformadas(datos, resultados, factor_escala)

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Estructura original (gris solido)
    for i, (Pi, Pj) in enumerate(ligas_orig):
        ax.plot([Pi[0], Pj[0]], [Pi[1], Pj[1]], [Pi[2], Pj[2]],
                '-', color='gray', linewidth=2, alpha=0.6,
                label='Original' if i == 0 else '')

    # Estructura deformada (curvas de Hermite, rojo)
    for i, curva in enumerate(curvas_def):
        ax.plot(curva[:, 0], curva[:, 1], curva[:, 2],
                '-', color='red', linewidth=2.5,
                label='Deformada (elastica, x%d)' % factor_escala if i == 0 else '')

    # Nodos
    for Pi, Pj in ligas_orig:
        ax.scatter(Pi[0], Pi[1], Pi[2], c='gray', s=60)
    for p in puntos_def:
        ax.scatter(p[0], p[1], p[2], c='red', s=80)

    desp = resultados['desplazamientos']
    # Etiquetas de desplazamiento en nodos B y E
    for nombre in ['B', 'E']:
        d = desp['sup_' + nombre]
        nodos_sup = datos['nodos']['superior']
        c = np.array(nodos_sup[nombre]) + np.array([d['UX'], d['UY'], d['UZ']]) * factor_escala
        ax.text(c[0], c[1], c[2] + 0.25, f'{nombre} UZ={d["UZ"]*1000:.2f} mm',
                fontsize=10, color='red', fontweight='bold')

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    titulo_escala = (' (amplificacion x%d)' % factor_escala) if factor_escala != 1 else ' (escala real)'
    ax.set_title('Estructura Original y Deformada tras Aplicar Cargas\n'
                'Elastica reconstruida%s' % titulo_escala)

    ax.legend(loc='upper left')
    ax.view_init(elev=20, azim=45)

    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos_rectangular' / nombre_archivo, dpi=150, bbox_inches='tight')
    plt.close()
    print("  Guardado: graficos_rectangular/%s" % nombre_archivo)


def visualizar_deformadas(datos, resultados):
    """
    Genera dos comparaciones original vs deformada:
      - deformada_escala1.png   : escala real (la deformacion es casi imperceptible)
      - deformada_escala500.png : amplificada x500 para apreciar las curvas
    """
    # Escala real (x1)
    visualizar_deformada(datos, resultados, factor_escala=1,
                         nombre_archivo='deformada_escala1.png')
    # Amplificada (x500)
    visualizar_deformada(datos, resultados, factor_escala=500,
                         nombre_archivo='deformada_escala500.png')

def main():
    print("=" * 60)
    print("VISUALIZACION - BENCHMARK RECTANGULAR 3D")
    print("=" * 60)
    ruta_datos = Path(__file__).parent / 'datos_entrada.json'
    ruta_resultados = Path(__file__).parent / 'resultados_rectangular' / 'resultados.json'
    
    datos = cargar_datos(ruta_datos)
    
    with open(ruta_resultados, 'r') as f:
        resultados = json.load(f)
    
    print("\nGenerando geometria 3D...")
    visualizar_modelo(datos)
    
    print("Generando planta...")
    visualizar_planta(datos)
    
    print("Generando cargas...")
    visualizar_cargas(datos)
    
    print("Generando ejes locales...")
    visualizar_ejes_locales(datos)
    
    print("Generando estructura deformada...")
    visualizar_deformadas(datos, resultados)
    
    print("Generando diagramas de fuerzas internas...")
    visualizar_diagramas_vigas(resultados)
    
    print("\n" + "=" * 60)
    print("VISUALIZACIONES RECTANGULARES COMPLETADAS")
    print("=" * 60)

if __name__ == "__main__":
    main()

"""
VISUALIZACIÓN - BENCHMARK 3D SEMANA 1 MCOC
==========================================
Visualización de geometría, ejes locales y cargas
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pathlib import Path

def cargar_datos(ruta_datos):
    """Carga los parámetros desde el archivo JSON."""
    with open(ruta_datos, 'r') as f:
        return json.load(f)

def visualizar_modelo(datos):
    """Visualiza la geometría completa del modelo."""
    
    # Crear figura 3D
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Obtener coordenadas de nodos
    nodos_base = datos['nodos']['base']
    nodos_sup = datos['nodos']['superior']
    
    # Dibujar nodos
    for nombre, coord in nodos_base.items():
        ax.scatter(coord[0], coord[1], coord[2], c='red', s=100, marker='o')
        ax.text(coord[0], coord[1], coord[2]-0.3, f'Base {nombre}', fontsize=8)
    
    for nombre, coord in nodos_sup.items():
        ax.scatter(coord[0], coord[1], coord[2], c='blue', s=100, marker='o')
        ax.text(coord[0], coord[1], coord[2]+0.2, f'Sup {nombre}', fontsize=8)
    
    # Dibujar columnas
    for nombre in ['A', 'C', 'D', 'F']:
        base = nodos_base[nombre]
        sup = nodos_sup[nombre]
        ax.plot([base[0], sup[0]], [base[1], sup[1]], [base[2], sup[2]], 
                'r-', linewidth=3, label='Columna P70x70' if nombre == 'A' else '')
    
    # Dibujar vigas en direccion X (seccion L 5.00m)
    vigas_x = [('A', 'B'), ('B', 'C'), ('D', 'E'), ('E', 'F')]
    for i, (v1, v2) in enumerate(vigas_x):
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                'b-', linewidth=2, label='Viga L 5.00m' if i == 0 else '')
    
    # Dibujar vigas en direccion Y - borde (seccion L 8.90m)
    vigas_y_borde = [('A', 'D'), ('C', 'F')]
    for i, (v1, v2) in enumerate(vigas_y_borde):
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                'g-', linewidth=2, label='Viga L 8.90m' if i == 0 else '')
    
    # Dibujar viga Y interior (seccion T 8.90m)
    p1 = nodos_sup['B']
    p2 = nodos_sup['E']
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
            'm-', linewidth=2, label='Viga T 8.90m')
    
    # Dibujar losas (semi-transparentes)
    # Panel izquierdo: A-B-E-D
    panel_izq = [
        nodos_sup['A'],
        nodos_sup['B'],
        nodos_sup['E'],
        nodos_sup['D']
    ]
    poly_izq = Poly3DCollection([panel_izq], alpha=0.3, facecolor='cyan', edgecolor='blue')
    ax.add_collection3d(poly_izq)
    
    # Panel derecho: B-C-F-E
    panel_der = [
        nodos_sup['B'],
        nodos_sup['C'],
        nodos_sup['F'],
        nodos_sup['E']
    ]
    poly_der = Poly3DCollection([panel_der], alpha=0.3, facecolor='cyan', edgecolor='blue')
    ax.add_collection3d(poly_der)
    
    # Dibujar ejes globales
    ax.quiver(0, 0, 0, 2, 0, 0, color='red', arrow_length_ratio=0.2, linewidth=2)
    ax.text(2.2, 0, 0, 'X', fontsize=12, color='red')
    
    ax.quiver(0, 0, 0, 0, 2, 0, color='green', arrow_length_ratio=0.2, linewidth=2)
    ax.text(0, 2.2, 0, 'Y', fontsize=12, color='green')
    
    ax.quiver(0, 0, 0, 0, 0, 2, color='blue', arrow_length_ratio=0.2, linewidth=2)
    ax.text(0, 0, 2.2, 'Z', fontsize=12, color='blue')
    
    # Configurar ejes
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Benchmark 3D - Semana 1 MCOC\n10 nodos, 11 elementos - Colaboracion monolitica losa-viga')
    
    # Leyenda
    ax.legend(loc='upper left')
    
    # Ajustar vista
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos' / 'geometria_3d.png', dpi=150, bbox_inches='tight')
    plt.close()

def visualizar_planta(datos):
    """Visualiza la planta del modelo."""
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Obtener coordenadas de nodos superiores
    nodos_sup = datos['nodos']['superior']
    
    # Dibujar nodos
    for nombre, coord in nodos_sup.items():
        ax.plot(coord[0], coord[1], 'ko', markersize=8)
        ax.text(coord[0]+0.2, coord[1]+0.2, nombre, fontsize=10)
    
    # Dibujar vigas en direccion X (L 5.00m)
    vigas_x = [('A', 'B'), ('B', 'C'), ('D', 'E'), ('E', 'F')]
    for v1, v2 in vigas_x:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=2)
    
    # Dibujar vigas en direccion Y - borde (L 8.90m)
    vigas_y_borde = [('A', 'D'), ('C', 'F')]
    for v1, v2 in vigas_y_borde:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'g-', linewidth=2)
    
    # Dibujar viga Y interior (T 8.90m)
    p1 = nodos_sup['B']
    p2 = nodos_sup['E']
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'm-', linewidth=2)
    
    # Dibujar losas
    # Panel izquierdo
    panel_izq_x = [nodos_sup['A'][0], nodos_sup['B'][0], 
                   nodos_sup['E'][0], nodos_sup['D'][0], nodos_sup['A'][0]]
    panel_izq_y = [nodos_sup['A'][1], nodos_sup['B'][1], 
                   nodos_sup['E'][1], nodos_sup['D'][1], nodos_sup['A'][1]]
    ax.fill(panel_izq_x, panel_izq_y, alpha=0.3, color='cyan', label='Panel izquierdo')
    
    # Panel derecho
    panel_der_x = [nodos_sup['B'][0], nodos_sup['C'][0], 
                   nodos_sup['F'][0], nodos_sup['E'][0], nodos_sup['B'][0]]
    panel_der_y = [nodos_sup['B'][1], nodos_sup['C'][1], 
                   nodos_sup['F'][1], nodos_sup['E'][1], nodos_sup['B'][1]]
    ax.fill(panel_der_x, panel_der_y, alpha=0.3, color='cyan', label='Panel derecho')
    
    # Dibujar ejes globales
    ax.annotate('', xy=(2, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(2.2, 0, 'X', fontsize=12, color='red')
    
    ax.annotate('', xy=(0, 2), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(0, 2.2, 'Y', fontsize=12, color='green')
    
    # Configurar ejes
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Planta del Benchmark 3D\nVigas con colaboracion monolitica losa-viga')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.legend()
    
    # Ajustar límites
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 10)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos' / 'planta.png', dpi=150, bbox_inches='tight')
    plt.close()

def visualizar_cargas(datos):
    """Visualiza las cargas distribuidas en las vigas."""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Carga triangular en vigas de 5m
    ax1 = axes[0, 0]
    x = np.linspace(0, 5, 100)
    w = 12.5 * (1 - np.abs(x - 2.5) / 2.5)
    ax1.fill_between(x, w, alpha=0.3, color='blue')
    ax1.plot(x, w, 'b-', linewidth=2)
    ax1.set_xlabel('Posición (m)')
    ax1.set_ylabel('Carga (kN/m)')
    ax1.set_title('Distribución triangular - Vigas de 5m\n(A-B, B-C, D-E, E-F)')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 5)
    ax1.set_ylim(0, 15)
    ax1.text(2.5, 13, 'w_max = 12.50 kN/m', ha='center')
    ax1.text(2.5, 7, 'Área = 31.25 kN', ha='center')
    
    # Carga trapezoidal en vigas de 8.9m exteriores
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
    ax2.set_xlabel('Posición (m)')
    ax2.set_ylabel('Carga (kN/m)')
    ax2.set_title('Distribución trapezoidal - Vigas de 8.9m\n(A-D, C-F)')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 8.9)
    ax2.set_ylim(0, 15)
    ax2.text(4.45, 13, 'w_max = 12.50 kN/m', ha='center')
    ax2.text(4.45, 7, 'Área = 80.00 kN', ha='center')
    
    # Carga trapezoidal en viga central B-E
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
    ax3.set_xlabel('Posición (m)')
    ax3.set_ylabel('Carga (kN/m)')
    ax3.set_title('Distribución trapezoidal doble - Viga central B-E')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 8.9)
    ax3.set_ylim(0, 30)
    ax3.text(4.45, 27, 'w_max = 25.00 kN/m', ha='center')
    ax3.text(4.45, 13, 'Área = 160.00 kN', ha='center')
    
    # Resumen de cargas
    ax4 = axes[1, 1]
    vigas = ['A-D', 'B-E', 'C-F', 'A-B', 'B-C', 'D-E', 'E-F']
    cargas = [80.0, 160.0, 80.0, 31.25, 31.25, 31.25, 31.25]
    colores = ['green', 'red', 'green', 'blue', 'blue', 'blue', 'blue']
    
    bars = ax4.bar(vigas, cargas, color=colores, alpha=0.7)
    ax4.set_xlabel('Viga')
    ax4.set_ylabel('Carga total (kN)')
    ax4.set_title('Resumen de cargas por viga')
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Agregar valores en las barras
    for bar, carga in zip(bars, cargas):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{carga:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos' / 'cargas.png', dpi=150, bbox_inches='tight')
    plt.close()

def visualizar_ejes_locales(datos):
    """Visualiza los ejes locales de los elementos."""
    
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Obtener coordenadas de nodos
    nodos_sup = datos['nodos']['superior']
    
    # Dibujar estructura
    # Columnas
    nodos_base = datos['nodos']['base']
    for nombre in ['A', 'C', 'D', 'F']:
        base = nodos_base[nombre]
        sup = nodos_sup[nombre]
        ax.plot([base[0], sup[0]], [base[1], sup[1]], [base[2], sup[2]], 
                'r-', linewidth=3)
    
    # Vigas X (L 5.00m)
    vigas_x = [('A', 'B'), ('B', 'C'), ('D', 'E'), ('E', 'F')]
    for v1, v2 in vigas_x:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'b-', linewidth=2)
    
    # Vigas Y borde (L 8.90m)
    vigas_y_borde = [('A', 'D'), ('C', 'F')]
    for v1, v2 in vigas_y_borde:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'g-', linewidth=2)
    
    # Viga Y interior (T 8.90m)
    p1 = nodos_sup['B']
    p2 = nodos_sup['E']
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'm-', linewidth=2)
    
    # Dibujar ejes locales para columnas
    longitud_flecha = 0.5
    for nombre in ['A', 'C', 'D', 'F']:
        base = nodos_base[nombre]
        sup = nodos_sup[nombre]
        medio = [(base[i] + sup[i])/2 for i in range(3)]
        
        # Eje local x (vertical)
        ax.quiver(medio[0], medio[1], medio[2], 0, 0, longitud_flecha, 
                 color='red', arrow_length_ratio=0.3, linewidth=2)
        
        # Eje local y
        ax.quiver(medio[0], medio[1], medio[2], longitud_flecha, 0, 0, 
                 color='green', arrow_length_ratio=0.3, linewidth=2)
        
        # Eje local z
        ax.quiver(medio[0], medio[1], medio[2], 0, longitud_flecha, 0, 
                 color='blue', arrow_length_ratio=0.3, linewidth=2)
    
    # Dibujar ejes locales para vigas X
    for v1, v2 in vigas_x:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        medio = [(p1[i] + p2[i])/2 for i in range(3)]
        
        # Eje local x (dirección de la viga)
        dx = p2[0] - p1[0]
        longitud = np.sqrt(dx**2)
        ax.quiver(medio[0], medio[1], medio[2], dx/longitud*longitud_flecha, 0, 0, 
                 color='red', arrow_length_ratio=0.3, linewidth=2)
        
        # Eje local y
        ax.quiver(medio[0], medio[1], medio[2], 0, 0, longitud_flecha, 
                 color='blue', arrow_length_ratio=0.3, linewidth=2)
        
        # Eje local z
        ax.quiver(medio[0], medio[1], medio[2], 0, longitud_flecha, 0, 
                 color='green', arrow_length_ratio=0.3, linewidth=2)
    
    # Dibujar ejes locales para vigas Y (borde L + interior T)
    vigas_y_todas = vigas_y_borde + [('B', 'E')]
    for v1, v2 in vigas_y_todas:
        p1 = nodos_sup[v1]
        p2 = nodos_sup[v2]
        medio = [(p1[i] + p2[i])/2 for i in range(3)]
        
        # Eje local x (dirección de la viga)
        dy = p2[1] - p1[1]
        longitud = np.sqrt(dy**2)
        ax.quiver(medio[0], medio[1], medio[2], 0, dy/longitud*longitud_flecha, 0, 
                 color='red', arrow_length_ratio=0.3, linewidth=2)
        
        # Eje local y
        ax.quiver(medio[0], medio[1], medio[2], longitud_flecha, 0, 0, 
                 color='green', arrow_length_ratio=0.3, linewidth=2)
        
        # Eje local z
        ax.quiver(medio[0], medio[1], medio[2], 0, 0, longitud_flecha, 
                 color='blue', arrow_length_ratio=0.3, linewidth=2)
    
    # Dibujar ejes globales
    ax.quiver(0, 0, 0, 2, 0, 0, color='red', arrow_length_ratio=0.2, linewidth=3)
    ax.text(2.2, 0, 0, 'X global', fontsize=12, color='red')
    
    ax.quiver(0, 0, 0, 0, 2, 0, color='green', arrow_length_ratio=0.2, linewidth=3)
    ax.text(0, 2.2, 0, 'Y global', fontsize=12, color='green')
    
    ax.quiver(0, 0, 0, 0, 0, 2, color='blue', arrow_length_ratio=0.2, linewidth=3)
    ax.text(0, 0, 2.2, 'Z global', fontsize=12, color='blue')
    
    # Configurar ejes
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Ejes Locales de los Elementos\nRojo: local x | Verde: local y | Azul: local z')
    
    # Ajustar vista
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / 'graficos' / 'ejes_locales.png', dpi=150, bbox_inches='tight')
    plt.close()

def visualizar_diagramas_vigas(resultados):
    """Diagramas de cortante V(x) y momento M(x) para las 7 vigas."""
    
    diagramas = resultados.get('diagramas_vigas', {})
    if not diagramas:
        print("  [AVISO] No hay datos de diagramas_vigas en resultados.json")
        return
    
    orden = ['elem_5', 'elem_6', 'elem_7', 'elem_8', 'elem_9', 'elem_10', 'elem_11']
    etiquetas = {
        'elem_5': 'A-B  (5.0m, L)',
        'elem_6': 'B-C  (5.0m, L)',
        'elem_7': 'D-E  (5.0m, L)',
        'elem_8': 'E-F  (5.0m, L)',
        'elem_9': 'A-D  (8.9m, L)',
        'elem_10': 'B-E  (8.9m, T)',
        'elem_11': 'C-F (8.9m, L)',
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
    plt.savefig(Path(__file__).parent / 'graficos' / 'diagramas_fuerzas.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("  Guardado: graficos/diagramas_fuerzas.png")

    # Figura 2: Momento B-E con analitico
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
        ax.set_title('Momento flector Viga B-E (elem 10) - Empotrado-Empotrado\n'
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
        plt.savefig(Path(__file__).parent / 'graficos' / 'momento_BE.png',
                    dpi=150, bbox_inches='tight')
        plt.close()
        print("  Guardado: graficos/momento_BE.png")

def main():
    """Funcion principal de visualizacion."""
    
    print("=" * 60)
    print("VISUALIZACION - BENCHMARK 3D SEMANA 1 MCOC")
    print("=" * 60)
    
    ruta_datos = Path(__file__).parent / 'datos_entrada.json'
    ruta_resultados = Path(__file__).parent / 'resultados' / 'resultados.json'
    
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
    
    print("Generando diagramas de fuerzas internas...")
    visualizar_diagramas_vigas(resultados)
    
    print("\n" + "=" * 60)
    print("VISUALIZACIONES COMPLETADAS")
    print("=" * 60)

if __name__ == "__main__":
    main()

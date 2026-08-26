"""
SCRIPT PRINCIPAL - BENCHMARK 3D SEMANA 1 MCOC
=============================================
Ejecuta ambas versiones (TL y Rectangular) y la comparacion.
"""

import sys
import subprocess
from pathlib import Path

PYTHON = str(Path(__file__).parent / '.venv' / 'Scripts' / 'python.exe')

def correr(script, descripcion):
    print("\n" + "=" * 60)
    print(f"  {descripcion}")
    print("=" * 60)
    ok = subprocess.run([PYTHON, str(script)], cwd=str(Path(__file__).parent))
    if ok.returncode != 0:
        print(f"  [ERROR] {descripcion} fallo con codigo {ok.returncode}")
        return False
    return True

def main():
    print("=" * 60)
    print("  BENCHMARK 3D - COMPARACION TL vs RECTANGULAR")
    print("=" * 60)

    base = Path(__file__).parent

    # --- Version TL ---
    correr(base / 'modelo_opensees.py', 'MODELO TL (secciones T/L)')
    correr(base / 'verificaciones.py', 'VERIFICACIONES TL')
    correr(base / 'visualizacion.py', 'VISUALIZACION TL')

    # --- Version Rectangular ---
    correr(base / 'benchmark_rectangular' / 'modelo_opensees.py',
           'MODELO RECTANGULAR (secciones 0.60x0.80)')
    correr(base / 'benchmark_rectangular' / 'verificaciones.py',
           'VERIFICACIONES RECTANGULAR')
    correr(base / 'benchmark_rectangular' / 'visualizacion.py',
           'VISUALIZACION RECTANGULAR')

    # --- Resumen final ---
    print("\n" + "=" * 60)
    print("  ARCHIVOS GENERADOS")
    print("=" * 60)
    print("  TL:")
    print("    resultados/resultados.json")
    print("    graficos/*.png")
    print("  Rectangular:")
    print("    benchmark_rectangular/resultados_rectangular/resultados.json")
    print("    benchmark_rectangular/graficos_rectangular/*.png")
    print("=" * 60)

if __name__ == "__main__":
    sys.exit(main())

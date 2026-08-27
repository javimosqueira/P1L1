# P1L1 — Benchmark 3D OpenSees vs SAP2000

Benchmark estructural de un pórtico 3D de hormigón armado desarrollado en **OpenSeesPy** y verificado contra **SAP2000**, dentro de la materia **MCOC** (Modelación Computacional y... / Mecánica Computacional).

El proyecto cubre el ciclo completo: construcción del modelo, extracción de desplazamientos, reacciones y fuerzas en elementos, verificaciones automáticas, visualización y comparación numérica contra SAP2000.

## Contenido del repositorio

| Ruta | Descripción |
|------|-------------|
| `Informe_P1L1_Benchmark.md` | Informe técnico completo del benchmark |
| `Resultados_P1L1_SAP.xlsx` | Resultados de verificación exportados de SAP2000 |
| `P1L1_SAP.sdb` | Modelo de SAP2000 |
| `datos_entrada.json` | Datos de entrada del modelo (geometría, materiales, secciones, cargas) |
| `modelo_opensees.py` | Modelo OpenSeesPy (versión compuesta) |
| `verificaciones.py` | Script de verificaciones automáticas |
| `visualizacion.py` | Script de visualización y gráficos |
| `ejecutar_todo.py` | Ejecutor de modelo + verificaciones + visualización |
| `benchmark_rectangular/` | **Semana 1**: vigas rectangulares 0.60×0.80 m |
| `benchmark_portable/` | Versión portable (instalar.bat / ejecutar.bat) |

## Requisitos e instalación

- Python 3.8+
- [OpenSeesPy](https://openseespydocs.readthedocs.io/en/latest/) (`pip install openseespy`)
- `numpy`
- `matplotlib`

```bash
pip install openseespy numpy matplotlib
```

## Cómo ejecutar (benchmark rectangular)

```bash
python modelo_opensees.py    # construye y resuelve el modelo, exporta resultados.json
python verificaciones.py     # verifica equilibrio, cargas, desplazamientos y esfuerzos
python visualizacion.py      # genera los gráficos (geometría 3D, planta, ejes, cargas, diagramas)
```

Los resultados quedan en `benchmark_rectangular/resultados_rectangular/` y los gráficos en `benchmark_rectangular/graficos_rectangular/`.

## Datos del modelo (semana 1 — rectangular)

- Pórtico 3D de **2 paños**: 10 m × 8.9 m en planta, altura **3.96 m**
- 10 nodos, 11 elementos (4 columnas + 7 vigas)
- Columnas **0.70 × 0.70 m**, vigas **0.60 × 0.80 m**
- Concreto: E = 25 GPa, ν = 0.20, G = 10.42 GPa
- 4 empotramientos en base
- Carga superficial G = 5.0 kN/m² sobre 89 m² de losa → **445 kN totales**
- Tributación a 45° hacia las vigas (triangular en vigas de 5 m, trapezoidal en vigas de 8.9 m)
- Análisis estático lineal elástico (solo gravitacional)

## Resultados de verificación (OpenSees vs SAP2000)

| Magnitud | OpenSeesPy | SAP2000 | Diferencia |
|----------|-----------:|--------:|-----------:|
| Reacción vertical total ΣRZ | 445.00 kN | 444.96 kN | ≈0.0 % |
| Axial columna A | +111.25 kN | +111.24 kN | ≈0.0 % |
| Momento My viga B–E (extremo i) | −142.36 kN·m | −142.62 kN·m | 0.2 % |
| Momento My viga B–E (media luz) | +78.32 kN·m | +78.85 kN·m | 0.7 % |
| Cortante Vz viga B–E (extremo i) | +80.00 kN | +79.99 kN | ≈0.0 % |
| Desplazamiento vertical nodo B | −1.567 mm | — | — |

Todas las verificaciones del modelo (geometría, áreas tributarias, carga total, equilibrio de reacciones, esfuerzos) superan la tolerancia definida.

## Gráficos

| Archivo | Contenido |
|---------|-----------|
| `geometria_3d.png` | Vista 3D de la estructura con nodos, elementos y losas |
| `planta.png` | Vista en planta con grilla y paños |
| `ejes_locales.png` | Orientación de ejes locales de cada elemento |
| `cargas.png` | Distribuciones de carga triangular/trapezoidal y resumen por viga |
| `diagramas_fuerzas.png` | Diagramas de cortante y momento de las 7 vigas |
| `momento_BE.png` | Diagrama de momento flector de la viga central B–E |
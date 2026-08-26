@echo off
echo ============================================================
echo  BENCHMARK 3D RECTANGULAR - EJECUCION COMPLETA
echo ============================================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Entorno virtual no encontrado.
    echo Ejecute primero "instalar.bat" para configurar el entorno.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

echo [1/4] Ejecutando modelo OpenSeesPy...
echo.
python modelo_opensees.py
if %errorlevel% neq 0 (
    echo [ERROR] Fallo el modelo.
    pause
    exit /b 1
)

echo.
echo [2/4] Ejecutando verificaciones...
echo.
python verificaciones.py
if %errorlevel% neq 0 (
    echo [ERROR] Fallaron las verificaciones.
    pause
    exit /b 1
)

echo.
echo [3/4] Generando graficos...
echo.
python visualizacion.py
if %errorlevel% neq 0 (
    echo [ERROR] Falló la generación de gráficos.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  PROCESO COMPLETADO
echo ============================================================
echo.
echo  Resultados JSON:  resultados_rectangular\resultados.json
echo  Reporte:          resultados_rectangular\reporte_verificacion.txt
echo  Graficos:         graficos_rectangular\*.png
echo.
echo ============================================================
pause

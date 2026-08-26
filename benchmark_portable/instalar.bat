@echo off
echo ============================================================
echo  INSTALACION - Benchmark 3D Rectangular
echo ============================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado en el PATH.
    echo Instale Python 3.10+ desde https://www.python.org/downloads/
    echo Marque "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo Creando entorno virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo crear el entorno virtual.
    pause
    exit /b 1
)

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Falló la instalación de dependencias.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  INSTALACION COMPLETADA
echo ============================================================
echo  Para ejecutar el modelo, doble clic en "ejecutar.bat"
echo ============================================================
pause

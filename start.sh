#!/bin/bash

# Este script se ejecuta al iniciar Azure App Service.
# Su propósito es instalar las dependencias del sistema operativo (Linux)
# necesarias para el paquete Python pyodbc antes de iniciar la aplicación.

echo "-> Inicializando el contenedor..."

# 1. Instalar el controlador ODBC necesario para pyodbc.
echo "-> Instalando dependencias del sistema (unixodbc-dev)..."
apt-get update -y
apt-get install -y unixodbc-dev

# 2. Verificar la instalación del controlador (Opcional, pero útil)
echo "-> Verificando la instalación del controlador ODBC..."
odbcinst -q -d || echo "Advertencia: No se pudo verificar el controlador ODBC, pero se intenta continuar."

# 3. Iniciar la aplicación Gunicorn (¡El cambio clave!)
echo "-> Iniciando Gunicorn: sgt.main:app"
python3 -m gunicorn --bind=0.0.0.0 --workers=4 --timeout=90 sgt.main:app

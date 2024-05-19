#!/usr/bin/env bash
# Exit on error
set -o errexit

# instala las dependencias necesarias
pip install -r requirements.txt

# Convertir archivos estáticos
python manage.py collectstatic --no-input

# Aplicar cualquier migración de base de datos pendiente
python manage.py migrate
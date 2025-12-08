#!/usr/bin/env bash

echo "🚀 Iniciando build para Render..."

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Cargar datos iniciales si existen los comandos
if python manage.py help | grep -q "cargar_fases_cronograma"; then
    python manage.py cargar_fases_cronograma
fi

if python manage.py help | grep -q "cargar_carreras_completas"; then
    python manage.py cargar_carreras_completas
fi

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

echo "✅ Build completado!"
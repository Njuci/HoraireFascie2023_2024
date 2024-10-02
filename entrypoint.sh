#!/bin/bash

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques (si applicable)
python manage.py collectstatic --noinput

# Démarrer le serveur Django
exec python manage.py runserver 0.0.0.0:8000

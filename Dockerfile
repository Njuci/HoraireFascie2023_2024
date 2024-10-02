# Utiliser une image Python slim comme base
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /HoraireFascie2023_2024

# Créer le fichier sources.list si non existant et utiliser un autre miroir Debian
RUN [ ! -f /etc/apt/sources.list ] && echo "deb http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list
RUN sed -i 's|http://deb.debian.org/debian|http://ftp.de.debian.org/debian|g' /etc/apt/sources.list

# Installer pkg-config, gcc, wget, et les bibliothèques de développement MariaDB
RUN apt-get update && \
    apt-get install -y pkg-config gcc wget libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt
COPY requirements.txt .

# Mettre à jour pip
RUN pip install --upgrade pip

# Installer les dépendances avec un timeout augmenté
RUN pip install --default-timeout=100 -r requirements.txt

# Copier le reste des fichiers du projet
COPY . .

# Démarrer l'application Django sans spécifier de port (Cloud Run gère cela automatiquement)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

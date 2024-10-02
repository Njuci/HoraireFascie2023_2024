# Utiliser l'image Python slim comme base
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /HoraireFascie2023_2024

# Installer les dépendances système nécessaires pour MariaDB et autres bibliothèques
RUN apt-get update && \
    apt-get install -y pkg-config gcc wget libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances Python (requirements.txt)
COPY requirements.txt .

# Mettre à jour pip
RUN pip install --upgrade pip

# Installer les dépendances Python à partir du fichier requirements.txt avec un timeout augmenté
RUN pip install --default-timeout=100 -r requirements.txt

# Copier le reste des fichiers du projet
COPY . .

# Copier le script d'entrée et le rendre exécutable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer le port sur lequel l'application fonctionne (ajuster selon les besoins)
EXPOSE 8000

# Définir le script d'entrée comme commande par défaut
ENTRYPOINT ["/entrypoint.sh"]

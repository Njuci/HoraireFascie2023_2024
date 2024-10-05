#!/bin/bash

# Configuration des variables
PROJECT_ID="elated-ranger-437311-b2"
SERVICE_NAME="horaire-fascie-2023-2024"
REGION="us-central1"
INSTANCE_CONNECTION_NAME="elated-ranger-437311-b2:us-central1:horaire3760"
CLOUD_RUN_URL="https://$SERVICE_NAME-y7h44d5u6a-uc.a.run.app"
LOCAL_PORT=8080

# Docker image
IMAGE_NAME="horairefascie2023_2024"
TAG="latest"
DOCKER_IMAGE="us-central1-docker.pkg.dev/$PROJECT_ID/horaire/$IMAGE_NAME:$TAG"

# Chemin Cloud SQL pour l'accès via Cloud Run
CLOUD_SQL_INSTANCE="$PROJECT_ID:us-central1:horaire3760"

# Fonction pour déployer localement
deploy_local() {
    echo "Déploiement local de l'application..."

    # Lancer l'application localement
    docker run -d \
        -p $LOCAL_PORT:8080 \
        -e DB_ENGINE=django.db.backends.mysql \
        -e DB_NAME=horaire_univ \
        -e DB_USER=njuci \
        -e DB_PASSWORD=3670njci \
        -e DB_HOST=34.122.218.103 \
        -e DB_PORT=3306 \
        $DOCKER_IMAGE

    echo "Application lancée localement à http://localhost:$LOCAL_PORT"
}

# Fonction pour déployer sur Cloud Run
deploy_cloud_run() {
    echo "Déploiement sur Cloud Run..."

    # Construire et pousser l'image Docker
    docker build -t $DOCKER_IMAGE .
    docker push $DOCKER_IMAGE

    # Déployer sur Cloud Run
    gcloud run deploy $SERVICE_NAME \
        --image $DOCKER_IMAGE \
        --add-cloudsql-instances $CLOUD_SQL_INSTANCE \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --set-env-vars "DB_ENGINE=django.db.backends.mysql,DB_NAME=horaire_univ,DB_USER=njuci,DB_PASSWORD=3670njci,DB_HOST=/cloudsql/$INSTANCE_CONNECTION_NAME,DB_PORT=3306" \
        --timeout 300s

    echo "Déploiement terminé. Application disponible à $CLOUD_RUN_URL"
}

# Vérification des arguments du script
if [ "$1" == "local" ]; then
    deploy_local
elif [ "$1" == "cloud" ]; then
    deploy_cloud_run
else
    echo "Utilisation : ./deploy.sh [local|cloud]"
fi

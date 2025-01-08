# Utiliser l'image officielle Python, variante slim-buster
FROM python:3.10-slim-buster

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les paquets requis
RUN pip install -r requirements.txt

# Définir le dossier de travail à /app
WORKDIR /app

# Copier tous les fichiers depuis le répertoire local vers /app dans le conteneur
COPY . /app

# Remplacer 'app' par le nom du module ou script Python que vous souhaitez exécuter
ENTRYPOINT ["python", "-m", "etl-app"]



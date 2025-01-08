FROM python:3.10-slim-buster
# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les paquets requis
RUN pip install -r requirements.txt

# Définir le dossier de travail à /app
WORKDIR /app

# Copier tous les fichiers depuis le répertoire local vers /app dans le conteneur
COPY . /app

ENTRYPOINT ["python", "-m", "app"]
EXPOSE 5000
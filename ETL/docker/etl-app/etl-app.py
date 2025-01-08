import pandas as pd
import sqlite3
from fuzzywuzzy import fuzz
import requests
from fuzzywuzzy import process

data_path="./data"

#EXtrére  la base dedonnée
df = pd.read_csv(f'{data_path}/point_apports_poubelles.csv')
volume_total_par_type = df.groupby(["commune","type_conteneur"])["volume_m3"].sum().reset_index()

nombre_par_type = df[["commune","type_conteneur"]].value_counts().reset_index()

donne = pd.merge(volume_total_par_type, nombre_par_type ,on=["commune","type_conteneur"])
donne.columns= ['commune','type_poubelle', 'volume_total_par_type', 'nombre_par_type']
population_par_per= pd.read_csv(f'{data_path}/population_per_commune.csv')

df = pd.merge(donne,population_par_per,on=["commune"])
df['nombre_total_type'] = df.groupby('commune')['nombre_par_type'].transform('sum')
# Step 2: Calculer le pourcentage de population par type de poubelle
df['pop_per_poub'] = ((df['population']*df['nombre_par_type'])/ df['nombre_total_type'])
poubelles = df.drop(['nombre_total_type'], axis=1)
conn = sqlite3.connect(f'{data_path}/poubelle_metro.db')
curs = conn.cursor()
# Step 2: Add new columns to the poubelle table
try:
    curs.execute("ALTER TABLE poubelle ADD COLUMN population INTEGER")
    print("Added 'population' column to 'poubelle' table.")
except sqlite3.OperationalError:
    print("'population' column already exists.")

try:
    curs.execute("ALTER TABLE poubelle ADD COLUMN pop_per_poub REAL")
    print("Added 'pop_per_poub' column to 'poubelle' table.")
except sqlite3.OperationalError:
    print("'pop_per_poub' column already exists.")

conn = sqlite3.connect(f'{data_path}/poubelle_metro.db')
curs = conn.cursor()
# Load the transformed data into the 'poubelle' table
# Use 'append' mode to add data to the existing table
poubelles.to_sql('poubelle', conn, if_exists='append', index=False)

# Commit and close the connection
conn.commit()


print("Data loaded into the 'poubelle' table successfully.")  
for i, row in df.iterrows():
    # Requête SQL pour mettre à jour les colonnes avec les valeurs du DataFrame
    query = """
    UPDATE poubelle
    SET population = ?
    WHERE commune = ? -- Utilise une colonne pour identifier la ligne à mettre à jour
    """
    # Exécuter la requête en passant les valeurs du DataFrame
    curs.execute(query, (row['population'], row['commune']))

conn.commit()

# Étape 1: Charger le fichier CSV avec les coordonnées GPS des villes
ville = pd.read_csv(f'{data_path}/villes_france_etl.csv')
# Assurez-vous que les noms des colonnes correspondent (les ajuster si nécessaire)
# Exemple : villes_france_etl.csv
base_extraire = ville.loc[:,["city_code","latitude","longitude"]]
base_extraire  
# renommé les colonnes 
base_extraire.columns=('commune','gps_lon', 'gps_lat')
base_extraire

patterns = ville["label"]
patterns

municipality = poubelles["commune"]
for commune in municipality:

    # Trouver la meilleure correspondance dans 'patterns'

    best_match = process.extractOne(commune, patterns)

    

    if best_match:

        print(f"Commune: {commune} - Best Match: {best_match[0]} with score {best_match[1]}")

        # Étape suivante : mise à jour de la table 'population_gps' avec 'best_match'

        # Vous pouvez ajouter ici le code de mise à jour de la table si nécessaire
    # Étape 2: Connexion à la base de données SQLite et lecture des communes de la table 'poubelle'
conn = sqlite3.connect(f'{data_path}/poubelle_metro.db')
cursor = conn.cursor()
# Lire les communes distinctes de la table 'poubelle'
query = "SELECT DISTINCT commune, population FROM poubelle"
poubelle_df = pd.read_sql_query(query, conn)
poubelle_df.head(5)
# Étape 3: Faire une jointure entre les communes de 'poubelle' et les villes du fichier CSV
# Attention à bien gérer les différences de casse ou d'accents
merged_df = pd.merge(poubelle_df,base_extraire, how="inner",on=["commune"])
merged_df.head(5)
# Étape 4: Filtrer uniquement les colonnes nécessaires (nom de la commune, latitude, longitude)
population_gps= merged_df[['commune', 'gps_lon', 'gps_lat']].drop_duplicates()
population_gps

# Étape 5: Charger les résultats dans la table 'population_gps'
# Créer la table 'population_gps' si elle n'existe pas déjà
create_table_query = """
CREATE TABLE IF NOT EXISTS population_gps (
    commune TEXT PRIMARY KEY,
    latitude REAL,
    longitude REAL
)
"""
cursor.execute(create_table_query)
# Insérer les données dans la table 'population_gps'
for index, row in merged_df.iterrows():
    insert_query = """
    INSERT OR IGNORE INTO population_gps (commune, latitude, longitude)
    VALUES (?, ?, ?)
    """
    cursor.execute(insert_query, (row['commune'], row['latitude'], row['longitude']))

# Commit les changements et fermer la connexion
conn.commit()
conn.close()

print("Insertion réussie des communes avec leurs coordonnées GPS dans la table 'population_gps'.")





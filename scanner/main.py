import requests
import psycopg2
import time

# Tentatives de connexion à PostgreSQL
def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="password",
                host="db",  # L'hôte de la DB dans Docker
                port="5432"
            )
            print("Connexion à la base de données réussie.")
            return conn  # Si la connexion réussit, retourne la connexion
        except psycopg2.OperationalError as e:
            print(f"Erreur de connexion à la base de données: {e}")
            print("Nouvelle tentative dans 3 secondes...")
            time.sleep(3)  # Attente de 3 secondes avant de réessayer

# Connexion à PostgreSQL (en réessayant si nécessaire)
conn = connect_to_db()

def fetch_urls_and_frequencies():
    with conn.cursor() as cursor:
        cursor.execute("SELECT url, frequency FROM urls_table;")
        return cursor.fetchall()

def check_and_update_data(url):
    try:
        response = requests.get(url)
        data = response.json()  # Supposons que la réponse est en JSON

        # Exemple d'analyse et mise à jour de la BDD si les données sont différentes
        if data.get("important_info") != "expected_value":
            with conn.cursor() as cursor:
                cursor.execute("UPDATE urls_table SET last_checked_data=%s WHERE url=%s;", (data, url))
                conn.commit()

    except requests.RequestException as e:
        print(f"Erreur lors de la requête HTTP sur {url}: {e}")

# Boucle principale
for url, frequency in fetch_urls_and_frequencies():
    check_and_update_data(url)
    time.sleep(frequency)  # Attente en fonction de la fréquence

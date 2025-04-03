import os
import csv
import logging

# Configuración del logger
log = logging.getLogger(__name__)

# Obtener la ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
MOVIES_FILE = os.path.join(DATA_DIR, "movies.csv")
RATINGS_FILE = os.path.join(DATA_DIR, "ratings.csv")
USER_FILE = os.path.join(DATA_DIR, "users.csv")

# Crear la carpeta "data" si no existe
os.makedirs(DATA_DIR, exist_ok=True)

def ensure_files_exist():
    """ Validar que las rutas y los archivos csv existen """
    if not os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "description", "category"])
        log.info(f"Created {MOVIES_FILE}")

    if not os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["user_name"])
        log.info(f"Created {RATINGS_FILE}")

def load_movies():
    """ Leer las películas desde el archivo csv y devolver una lista de diccionarios """
    with open(MOVIES_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        log.info(f"Movies file {MOVIES_FILE} loaded")
        return [row for row in reader]

def load_ratings():
    """ Leer las valoraciones desde el archivo csv """
    if not os.path.exists(RATINGS_FILE) or os.stat(RATINGS_FILE).st_size == 0:
        log.info(f"Ratings file {RATINGS_FILE} is empty or does not exist")
        return []

    with open(RATINGS_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        log.info(f"Ratings file {RATINGS_FILE} loaded")
        return [row for row in reader]
    
def load_users():
    """ Leer las valoraciones desde el archivo csv """
    if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
        log.info(f"User file {USER_FILE} is empty or does not exist")
        return []

    with open(USER_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        log.info(f"User file {USER_FILE} loaded")
        return [row for row in reader]
    
def get_column_from_movies_file(column_name):
    """ Obtener una columna específica del archivo CSV de películas """
    with open(MOVIES_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        log.info(f"Column {column_name} consulted")
        return [row[column_name] for row in reader if column_name in row]

def get_column_from_ratings_file(column_name):
    """ Obtener una columna específica del archivo CSV de valoraciones """
    with open(RATINGS_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        log.info(f"Column {column_name} consulted")
        return [row[column_name] for row in reader if column_name in row]

def update_user_rating(user_json):
    """
    Actualiza la calificación de un usuario para una película específica en el CSV de ratings.
    """
    print(user_json)
    user = user_json["username"]
    movie = user_json["movie"]
    rating_value = user_json["rating"]
    
    rows = []
    user_found = False
    with open(RATINGS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        for row in reader:
            if row["user_name"] == user:
                if movie in headers:
                    row[movie] = str(rating_value)
                    user_found = True
            rows.append(row)
        log.info(f"Updated rating for user {user} and movie {movie} to {rating_value}")
    
    if not user_found:
        new_row = {col: "" for col in headers}
        new_row["user_name"] = user
        if movie in headers:
            new_row[movie] = str(rating_value)
        rows.append(new_row)
        log.info(f"Added new user {user} with rating for {movie}")
    
    with open(RATINGS_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
        
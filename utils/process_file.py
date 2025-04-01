import os
import csv
import json

MOVIES_FILE = "data\\movies.csv"
RATINGS_FILE = "data\\ratings.csv"

def ensure_files_exist():
    """ Validar que las rutas y los archivos csv existen """
    os.makedirs("data", exist_ok=True)

    # Crear movies.csv (si no existe) y agregar encabezado
    if not os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "description", "category"])
        print(f"Created {MOVIES_FILE}")

    # Crear ratings.csv si no existe
    if not os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["user_name"])  # Solo escribe la cabecera 'user_name'
        print(f"Created {RATINGS_FILE}")

def load_movies():
    """ Leer las películas desde el archivo csv y devolver una lista de diccionarios """
    with open(MOVIES_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]  # Retorna una lista de diccionarios con nombre, descripción y categoría

def load_ratings():
    """ Leer las valoraciones desde el archivo csv """
    if not os.path.exists(RATINGS_FILE) or os.stat(RATINGS_FILE).st_size == 0:
        return []  # Si no existe o está vacío, devolver una lista vacía

    with open(RATINGS_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        return [row for row in reader]  # Devolver todas las filas

def add_user_ratings_from_json(user_json):
    """ Agregar valoraciones desde un JSON """
    user_data = json.loads(user_json)
    user_name = user_data["user"]
    movie_ratings = user_data["ratings"]

    # Cargar las películas desde movies.csv
    movies = load_movies()

    ratings = load_ratings()

    # Si no existe el encabezado, agregar todas las películas al encabezado de ratings.csv
    if not ratings:
        # Escribir encabezado con los nombres de las películas
        header = ["user_name"] + [movie["name"] for movie in movies]
        
        # Escribir encabezado y la primera fila de valoraciones en el archivo CSV
        with open(RATINGS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Escribir el encabezado
            user_ratings = [user_name] + [movie_ratings.get(movie["name"], "") for movie in movies]
            writer.writerow(user_ratings)  # Escribir la fila con las valoraciones del usuario
        print(f"User {user_name}'s ratings saved successfully!")
        return  # Salir después de escribir el archivo cuando está vacío

    # Si ya existe el encabezado, solo agregar la nueva fila
    user_ratings = [user_name] + [movie_ratings.get(movie["name"], "") for movie in movies]
    
    # Abrir el archivo en modo 'a' para agregar las valoraciones sin sobrescribir el archivo
    with open(RATINGS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(user_ratings)  # Escribir solo la nueva valoración del usuario
    
    print(f"User {user_name}'s ratings saved successfully!")


# Ejemplo
if __name__ == "__main__":
    # Validar la existencia de la carpeta y archivos
    ensure_files_exist()

    # Leer las películas del archivo csv
    """ 
    Devuelve una lista de diccionarios con nombre, descripción y categoría 
        Ejemplo de salida:
        [
            {'name': 'Interstellar', 'description': 'Space adventure', 'category': 'Sci-Fi'},
            {'name': 'Avatar', 'description': 'Blue aliens on a planet', 'category': 'Action'},
            {'name': 'Titanic', 'description': 'Ship sinking drama', 'category': 'Romance'},
            {'name': 'Forrest Gump', 'description': 'Life story', 'category': 'Drama'}
        ]
    """
    movies = load_movies()

    # Ejemplo del JSON que recibe sobre una valoración de usuario
    user_json = '''{
        "user": "Ana",
        "ratings": {
            "Interstellar": 5,
            "Avatar": 4,
            "Titanic": 2,
            "Forrest Gump": 4
        }
    }'''

    # Agregar valoración del usuario desde el JSON
    add_user_ratings_from_json(user_json)

    # Leer valoraciones del csv
    """ 
    Devuelve una lista de listas. Cada lista interna representa una fila del archivo ratings.csv, 
    con el primer valor siendo el nombre de usuario y los valores restantes las valoraciones de las películas. 
    Ejemplo de salida:
    [
        ['user_name', 'Interstellar', 'Avatar', 'Titanic', 'Forrest Gump'],
        ['Juan', '5', '3', '0', '4']
    ]
    """
    ratings = load_ratings()
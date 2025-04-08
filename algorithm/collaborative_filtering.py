import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils.process_file import load_movies, load_ratings, load_users

class UserBasedCollaborativeFiltering:
    """
    Sistema de recomendación basado en filtrado colaborativo por usuarios,
    adaptado para trabajar con archivos CSV.
    """
    
    def __init__(self):
        """Inicializa el sistema de filtrado colaborativo."""
        self.usuarios = []
        self.items = []
        self.ratings_matrix = None
        self.similarity_matrix = None
        self.df_ratings = []
        self.df_movies = []
    
    def load_from_csv(self):
        """
        Carga datos desde archivos CSV.
        """
        try:
            # Cargar usuarios
            self.usuarios = load_users()
            # print(self.usuarios)
            
            # Cargar calificaciones
            self.df_ratings = load_ratings()
            # print(self.df_ratings)
            
            # Cargar películas
            self.df_movies = load_movies()
            # print(self.df_movies)
            
            # Verificar que los datos son válidos
            if len(self.usuarios) == 0 or self.df_ratings.empty or self.df_movies.empty:
                print("Error: Uno o más archivos CSV están vacíos.")
                return False
            
            # Extraer nombres de películas de las columnas del dataframe de calificaciones
            self.items = [col for col in self.df_ratings.columns if col != 'user_name']
            print(self.items)
            
            # Construir matriz de calificaciones
            self._build_ratings_matrix()
            
            # Calcular similitud entre usuarios
            self.calculate_similarity()
            
            return True
            
        except Exception as e:
            print(f"Error al cargar datos desde CSV: {e}")
            return False
    
    def _build_ratings_matrix(self):
        """
        Construye la matriz de calificaciones a partir del DataFrame de calificaciones.
        Las filas representan usuarios y las columnas películas.
        """
        # Inicializar matriz con ceros
        self.ratings_matrix = np.zeros((len(self.usuarios), len(self.items)))
        
        # Llenar la matriz con calificaciones
        for i, usuario in enumerate(self.usuarios):
            # Buscar fila del usuario en el dataframe
            user_row = self.df_ratings[self.df_ratings['user_name'] == usuario]
            
            if not user_row.empty:
                for j, item in enumerate(self.items):
                    if item in user_row.columns:
                        rating = user_row[item].values[0]
                        # Convertir NaN a 0 (no calificado)
                        if not pd.isna(rating):
                            self.ratings_matrix[i, j] = rating
        
        return self.ratings_matrix
    
    def calculate_similarity(self):
        """Calcula la matriz de similitud entre usuarios utilizando similitud del coseno."""
        if self.ratings_matrix is None:
            print("Error: No hay matriz de calificaciones para calcular similitud.")
            return None
            
        self.similarity_matrix = cosine_similarity(self.ratings_matrix)
        return self.similarity_matrix
    
    def predict_rating(self, user_idx, item_idx):
        """
        Predice la calificación que un usuario daría a un item.
        """
        if self.ratings_matrix[user_idx, item_idx] > 0:
            return self.ratings_matrix[user_idx, item_idx]  # Ya calificado
            
        numerator = 0.0
        denominator = 0.0
        
        for u in range(len(self.usuarios)):
            if u != user_idx and self.ratings_matrix[u, item_idx] > 0:
                numerator += self.similarity_matrix[user_idx, u] * self.ratings_matrix[u, item_idx]
                denominator += abs(self.similarity_matrix[user_idx, u])
                
        if denominator == 0:
            return None
            
        return numerator / denominator
    
    def get_recommendations(self, username, top_n=5):
        """
        Función única para obtener recomendaciones proporcionando solo el nombre de usuario.
        
        Parámetros:
        - username: Nombre del usuario
        - top_n: Número máximo de recomendaciones (predeterminado: 5)
        
        Retorna:
        - Diccionario con información de los items recomendados
        """
        if username not in self.usuarios:
            return {"error": f"Usuario '{username}' no encontrado"}
            
        user_idx = self.usuarios.index(username)
        missing_items = np.where(self.ratings_matrix[user_idx] == 0)[0]
        
        predictions = {}
        for item_idx in missing_items:
            pred_rating = self.predict_rating(user_idx, item_idx)
            if pred_rating is not None:
                item_name = self.items[item_idx]
                predictions[item_name] = pred_rating
                
        # Ordenar predicciones de mayor a menor
        recommended_items = sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        # Formatear resultados con información adicional de las películas
        results = []
        for item_name, rating in recommended_items:
            # Buscar información adicional en el dataframe de películas
            movie_info = self.df_movies[self.df_movies['name'] == item_name]
            
            if not movie_info.empty:
                results.append({
                    'name': item_name,
                    'predicted_rating': round(float(rating), 2),
                    'description': movie_info['description'].values[0] if 'description' in movie_info.columns else '',
                    'category': movie_info['category'].values[0] if 'category' in movie_info.columns else ''
                })
            else:
                results.append({
                    'name': item_name,
                    'predicted_rating': round(float(rating), 2)
                })
                
        return {
            'user': username,
            'recommendations': results
        }
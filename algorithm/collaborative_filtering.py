import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from utils.process_file import load_movies, load_ratings

movies = load_movies()
ratings = load_ratings()

def recommend_movies_collab(username, limit=None):
    """
    Recomienda películas utilizando filtrado colaborativo basado en similitud entre usuarios.
    """
    if not movies or len(ratings) < 2:
        return []
    
    # Create a DataFrame for movies
    df_movies = pd.DataFrame(movies)
    
    header = ratings[0]
    static_movies = header[1:]
    df_ratings = pd.DataFrame(ratings[1:], columns=header)
    
    # Verify if the user exists
    users = df_ratings["user_name"].tolist()
    if username not in users:
        return []
    
    # Convert rating columns to numeric
    for movie in static_movies:
        df_ratings[movie] = pd.to_numeric(df_ratings[movie], errors="coerce").fillna(0)
    
    # Create the ratings matrix
    ratings_matrix = df_ratings[static_movies].to_numpy(dtype=float)
    
    # Calculate the similarity between users
    similarity_matrix = cosine_similarity(ratings_matrix)
    
    users_list = df_ratings["user_name"].tolist()
    target_idx = users_list.index(username)
    
    # Detect unrated movies by user
    user_ratings = ratings_matrix[target_idx]
    missing_indices = np.where(user_ratings == 0)[0]
    
    # Calculate predictions for missing movies
    predictions = {}
    for movie_idx in missing_indices:
        numerator = 0.0
        denominator = 0.0
        for other_idx in range(len(users_list)):
            if other_idx == target_idx:
                continue
            other_rating = ratings_matrix[other_idx, movie_idx]
            if other_rating != 0:
                sim = similarity_matrix[target_idx, other_idx]
                numerator += sim * other_rating
                denominator += abs(sim)
        if denominator != 0:
            predictions[static_movies[movie_idx]] = numerator / denominator

    if not predictions:
        return []
    
    # Sort predictions
    sorted_recommendations = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    
    # Limit the number of recommendations
    if limit is not None:
        sorted_recommendations = sorted_recommendations[:limit]
    
    # Format recommendations
    formatted_recommendation = format_recommendations(sorted_recommendations, df_movies, username)
    
    return formatted_recommendation

def format_recommendations(recommended, df_movies, username):
    recommendations_list = []
    for movie_name, score in recommended:
        try:
            row = df_movies.loc[df_movies["name"] == movie_name].iloc[0]
        except IndexError:
            # En el caso poco probable de no encontrar la película, se omite
            continue
        recommendations_list.append({
            "title": row["name"],
            "description": row["description"],
            "category": row["category"]
        })
    
    response = {
        "user": username,
        "movies": recommendations_list
    }
    
    return response

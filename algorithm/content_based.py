import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.process_file import load_movies, load_ratings

movies = load_movies()
ratings = load_ratings()

def recommend_movies(username, min_fav_rating=4, limit=None):
    """
    Recommend movies based on user ratings and movie features.
    """
    if not movies or len(ratings) < 2:
        return []
    
    # Create a DataFrame for movies
    df_movies = pd.DataFrame(movies)
    df_movies["features"] = df_movies["description"] + " " + df_movies["category"]
    
    # Calculate TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df_movies["features"])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # Create a DataFrame for ratings
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
    
    # Get the user's ratings
    user_row = df_ratings.loc[df_ratings["user_name"] == username].iloc[0]
    user_ratings = user_row[static_movies].to_numpy(dtype=float)

    # Identify favorite static movies
    fav_indices = np.where(user_ratings >= min_fav_rating)[0]
    if len(fav_indices) == 0:
        print("No hay suficientes películas favoritas para generar recomendaciones.")
        return []

    # Get the full indices of the favorite movies
    fav_full_indices = []
    for idx in fav_indices:
        movie_name = static_movies[idx]
        matches = df_movies.index[df_movies["name"] == movie_name].tolist()
        if matches:
            fav_full_indices.append(matches[0])
            
    # Exclude static movies from candidates
    candidate_mask = ~df_movies["name"].isin(static_movies)
    candidate_indices = df_movies.index[candidate_mask].tolist()
    
    # Calculate similarities
    predictions = {}
    for cand_idx in candidate_indices:
        sim_sum = 0.0
        for fav_idx in fav_full_indices:
            sim_sum += similarity_matrix[cand_idx, fav_idx]
        avg_sim = sim_sum / len(fav_full_indices)
        predictions[df_movies.loc[cand_idx, "name"]] = avg_sim
    
    # Sort predictions
    sorted_recommendation = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    
    # Limit the number of recommendations
    if limit is not None:
        sorted_recommendation = sorted_recommendation[:limit]
    
    # Format recommendations
    formatted_recommendation = format_recommendations(sorted_recommendation, df_movies, username)
    return formatted_recommendation
    


def format_recommendations(recommended, df_movies, username):
    recommendations_list = []
    for movie_name, score in recommended:
        row = df_movies.loc[df_movies["name"] == movie_name].iloc[0]
        recommendations_list.append({
            "title": row["name"],
            "description": row["description"],
            "category": row["category"]
        })

    response = {
        "user": username,
        "recommendations": recommendations_list
    }
    
    return response


#! Example usage
if __name__ == "__main__":
    recommended = recommend_movies("Pablo", limit=5)
    print(recommended)
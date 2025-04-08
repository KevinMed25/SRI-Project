from config import config

from flask import Flask, request, render_template, jsonify, make_response
from flask_cors import CORS
from utils.process_file import ensure_files_exist, load_users, update_user_rating
from algorithm.content_based import recommend_movies
from algorithm.collaborative_filtering import recommend_movies_collab

app = Flask(__name__)
CORS(app) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rate")
def rate():
    return render_template("rate.html")


@app.route("/api/users", methods=['GET'])
def get_users(): 
    data = {"users": [{"name": name} for name in load_users()[0]]}    
    return jsonify(data)

@app.route('/api/save-ratings', methods=['POST'])
def save_ratings():
    json_rating = request.get_json()
    ensure_files_exist()
    update_user_rating(json_rating)
    return make_response({"message": "Valoraciones guardadas correctamente"},201)

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    username = request.args.get('user')
    
    if not username:
        return jsonify({"error": "El nombre de usuario es requerido"}), 400
    
    recomendations = recommend_movies(username, min_fav_rating=4, limit=6)
    
    return jsonify(recomendations)

@app.route('/api/collaborative-filtering', methods=['GET'])
def get_collaborative_filtering(): 
    username = request.args.get('user ')
    
    if not username:
        return jsonify({"error": "El nombre de usuario es requerido"}), 400
    
    recomendations = recommend_movies_collab(username)

    return jsonify(recomendations)


if __name__ == "__main__":
    app.run(debug=True)

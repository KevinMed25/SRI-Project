from flask import Flask, request, render_template, jsonify, make_response
from flask_cors import CORS
from utils.process_file import ensure_files_exist, load_users, get_column_from_ratings_file, update_user_rating
import json

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5000"]) 

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
    print(json_rating)
    ensure_files_exist()
    update_user_rating(json_rating)
    # add_user_ratings_from_json(json_rating)
    return make_response({"message": "Valoraciones guardadas correctamente"},201)

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    recomendations = [
        {
            "user": "Ana",
            "peliculas": [
                {
                    "titulo": "Inception", 
                    "descripcion": "Un ladrón que roba secretos", 
                    "categoria": "Ciencia ficción"
                },
                {
                    "titulo": "Interstellar", 
                    "descripcion": "Un grupo de astronautas viaja a través de un agujero de gusano", 
                    "categoria": "Ciencia ficción"
                }
            ]
        }
    ]
    return jsonify({"recommendations": recomendations})


if __name__ == "__main__":
    app.run(debug=True)

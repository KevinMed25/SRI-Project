from flask import Flask, request, render_template, jsonify, make_response
from flask_cors import CORS
import csv
import utils.process_file as pf 

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"]) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rate")
def rate():
    return render_template("rate.html")


@app.route("/api/users", methods=['GET'])
def get_users(): 
    users_list = []

    with open('./data/users.csv', mode='r', encoding='utf-8') as csv_file :
        csv_reader = csv.reader(csv_file)
        for row in csv_reader: 
            for name in row: 
                if name.strip(): 
                    users_list.append({"name": name.strip()})

    return jsonify({"users": users_list})
    

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies_list = []
    with open('./data/movies.csv', mode='r', encoding='utf-8') as csv_file :
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader: 
            movies_list.append({
                "name": row["name"],
                "description": row["description"],
                "category": row["category"]
            })

    return jsonify({"movies": movies_list})

@app.route('/api/save-ratings', methods=['POST'])
def save_ratings():
    json_rating = request.get_json()
    pf.ensure_files_exist()
    pf.add_user_ratings_from_json(json_rating)
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
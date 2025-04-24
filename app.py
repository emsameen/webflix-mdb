import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.sample_mflix

@app.route('/')
def home():
    genre_map = {}
    query = request.args.get('q')
    if query:
        # Search by actor
        movies = db.movies.find({"cast": {"$regex": query, "$options": "i"}}).limit(100)
        return render_template('search_results.html', query=query, movies=movies)
    else:
        # Group movies by genres
        all_movies = db.movies.find({"genres": {"$exists": True}, "title": {"$exists": True}}).limit(200)
        for movie in all_movies:
            for genre in movie.get("genres", []):
                genre_map.setdefault(genre, []).append(movie)
        return render_template('home.html', genre_map=genre_map)

@app.route('/movie/<id>')
def movie_detail(id):
    movie = db.movies.find_one({'_id': ObjectId(id)})
    return render_template('movie_detail.html', movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
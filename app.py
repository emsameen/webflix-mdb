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
        # Search by actor name
        movies = db.movies.find({"cast": {"$regex": query, "$options": "i"}}).limit(100)
        return render_template('search_results.html', query=query, movies=movies)

    # 1. Fetch all movies (limit for performance)
    all_movies = list(db.movies.find({
        "genres": {"$exists": True},
        "title": {"$exists": True}
    }).limit(200))

    # 2. Get all movie IDs
    movie_ids = [movie["_id"] for movie in all_movies]

    # 3. Aggregate comment counts per movie
    comment_data = db.comments.aggregate([
        {"$match": {"movie_id": {"$in": movie_ids}}},
        {"$group": {"_id": "$movie_id", "count": {"$sum": 1}}}
    ])
    comment_counts = {item["_id"]: item["count"] for item in comment_data}

    # 4. Attach comment counts to movies and group by genre
    for movie in all_movies:
        movie["comment_count"] = comment_counts.get(movie["_id"], 0)
        for genre in movie.get("genres", []):
            genre_map.setdefault(genre, []).append(movie)

    return render_template('home.html', genre_map=genre_map)



@app.route('/movie/<id>')
def movie_detail(id):
    movie = db.movies.find_one({'_id': ObjectId(id)})
    comments = db.comments.find({'movie_id': ObjectId(id)}).sort('date', -1).limit(10)
    return render_template('movie_detail.html', movie=movie, comments=comments)


if __name__ == '__main__':
    app.run(debug=True)
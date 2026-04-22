from flask import Flask, request, jsonify
import mysql.connector
from config import DB_CONFIG
from modules.movies import search_movies, get_trending, get_movie_details
from modules.watchlist import (add_to_watchlist, get_watchlist,
                                update_status, remove_from_watchlist, add_rating)
from modules.recommendations import get_recommendations, get_top_rated_by_genre

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "query parameter is required"}), 400
    results = search_movies(query)
    return jsonify(results)


@app.route("/trending", methods=["GET"])
def trending():
    results = get_trending()
    return jsonify(results)


@app.route("/details/<content_type>/<int:tmdb_id>", methods=["GET"])
def details(content_type, tmdb_id):
    result = get_movie_details(tmdb_id, content_type)
    return jsonify(result)


@app.route("/watchlist/add", methods=["POST"])
def add_watchlist():
    data = request.json
    result = add_to_watchlist(
        data["user_id"],
        data["tmdb_id"],
        data.get("content_type", "movie"),
        data.get("status", "want_to_watch")
    )
    return jsonify(result)


@app.route("/watchlist/<int:user_id>", methods=["GET"])
def watchlist(user_id):
    status = request.args.get("status")
    result = get_watchlist(user_id, status)
    return jsonify(result)


@app.route("/watchlist/update", methods=["PUT"])
def update_watchlist():
    data = request.json
    result = update_status(data["user_id"], data["tmdb_id"], data["status"])
    return jsonify(result)


@app.route("/watchlist/remove", methods=["DELETE"])
def remove_watchlist():
    data = request.json
    result = remove_from_watchlist(data["user_id"], data["tmdb_id"])
    return jsonify(result)


@app.route("/rate", methods=["POST"])
def rate():
    data = request.json
    result = add_rating(
        data["user_id"],
        data["tmdb_id"],
        data["rating"],
        data.get("review")
    )
    return jsonify(result)


@app.route("/recommendations/<int:user_id>", methods=["GET"])
def recommendations(user_id):
    result = get_recommendations(user_id)
    return jsonify(result)


@app.route("/top-rated", methods=["GET"])
def top_rated():
    genre = request.args.get("genre", "")
    result = get_top_rated_by_genre(genre)
    return jsonify(result)


@app.route("/user/register", methods=["POST"])
def register():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (data["username"], data["email"], data["password"])
        )
        db.commit()
        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    print("🎬 OTT Content Tracker API is running!")
    print("📡 Base URL: http://localhost:5000")
    app.run(debug=True, port=5000)
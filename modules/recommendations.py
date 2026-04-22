import requests
import mysql.connector
from config import TMDB_API_KEY, TMDB_BASE_URL, DB_CONFIG
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
session.verify = False


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def get_recommendations(user_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT c.genre, c.tmdb_id, c.content_type, c.title
        FROM watchlist w
        JOIN content c ON w.content_id = c.id
        WHERE w.user_id = %s AND w.status = 'completed'
        ORDER BY w.updated_at DESC
        LIMIT 5
    """
    cursor.execute(query, (user_id,))
    watched = cursor.fetchall()
    cursor.close()
    db.close()

    if not watched:
        return {"message": "Watch and complete some content first to get recommendations!"}

    recommendations = []
    seen_ids = set()

    for item in watched:
        tmdb_id = item["tmdb_id"]
        content_type = item["content_type"]

        url = f"{TMDB_BASE_URL}/{content_type}/{tmdb_id}/similar"
        params = {"api_key": TMDB_API_KEY, "language": "en-US", "page": 1}
        response = requests.get(url, params=params)
        data = response.json()

        for rec in data.get("results", [])[:3]:
            rec_id = rec.get("id")
            if rec_id not in seen_ids:
                seen_ids.add(rec_id)
                recommendations.append({
                    "tmdb_id": rec_id,
                    "title": rec.get("title") or rec.get("name"),
                    "type": content_type,
                    "rating": rec.get("vote_average"),
                    "overview": rec.get("overview"),
                    "because_you_watched": item["title"]
                })

    return recommendations[:10]


def get_top_rated_by_genre(genre):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT title, content_type, genre, release_year, tmdb_rating
        FROM content
        WHERE genre LIKE %s
        ORDER BY tmdb_rating DESC
        LIMIT 10
    """
    cursor.execute(query, (f"%{genre}%",))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results
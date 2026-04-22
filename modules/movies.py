import requests
import mysql.connector
import urllib3
import ssl
from config import TMDB_API_KEY, TMDB_BASE_URL, DB_CONFIG

# Fix SSL issue
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()
session.verify = False

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def search_movies(query):
    url = f"{TMDB_BASE_URL}/search/multi"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US",
        "page": 1
    }
    response = session.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("results", [])[:10]:
        if item.get("media_type") in ["movie", "tv"]:
            results.append({
                "tmdb_id": item.get("id"),
                "title": item.get("title") or item.get("name"),
                "type": item.get("media_type"),
                "release_year": (item.get("release_date") or item.get("first_air_date") or "")[:4],
                "overview": item.get("overview"),
                "rating": item.get("vote_average"),
                "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None
            })
    return results


def get_movie_details(tmdb_id, content_type="movie"):
    url = f"{TMDB_BASE_URL}/{content_type}/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = session.get(url, params=params)
    data = response.json()

    genres = [g["name"] for g in data.get("genres", [])]

    return {
        "tmdb_id": data.get("id"),
        "title": data.get("title") or data.get("name"),
        "type": content_type,
        "genre": ", ".join(genres),
        "release_year": (data.get("release_date") or data.get("first_air_date") or "")[:4],
        "overview": data.get("overview"),
        "poster_path": data.get("poster_path"),
        "rating": data.get("vote_average")
    }


def save_content(tmdb_id, content_type="movie"):
    details = get_movie_details(tmdb_id, content_type)
    db = get_db()
    cursor = db.cursor()

    query = """
        INSERT IGNORE INTO content 
        (tmdb_id, title, content_type, genre, release_year, overview, poster_path, tmdb_rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        details["tmdb_id"],
        details["title"],
        details["type"],
        details["genre"],
        details["release_year"] or None,
        details["overview"],
        details["poster_path"],
        details["rating"]
    ))
    db.commit()

    cursor.execute("SELECT id FROM content WHERE tmdb_id = %s", (tmdb_id,))
    content_id = cursor.fetchone()[0]

    cursor.close()
    db.close()
    return content_id


def get_trending():
    url = f"{TMDB_BASE_URL}/trending/all/week"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = session.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("results", [])[:10]:
        results.append({
            "tmdb_id": item.get("id"),
            "title": item.get("title") or item.get("name"),
            "type": item.get("media_type"),
            "rating": item.get("vote_average"),
            "overview": item.get("overview"),
            "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get("poster_path") else None
        })
    return results
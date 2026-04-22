import mysql.connector
from config import DB_CONFIG
from modules.movies import save_content


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def add_to_watchlist(user_id, tmdb_id, content_type="movie", status="want_to_watch"):
    content_id = save_content(tmdb_id, content_type)
    db = get_db()
    cursor = db.cursor()

    query = """
        INSERT INTO watchlist (user_id, content_id, status)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE status = %s, updated_at = CURRENT_TIMESTAMP
    """
    cursor.execute(query, (user_id, content_id, status, status))
    db.commit()
    cursor.close()
    db.close()
    return {"message": f"Added to watchlist with status: {status}"}


def get_watchlist(user_id, status=None):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if status:
        query = """
            SELECT c.title, c.content_type, c.genre, c.release_year,
                   c.tmdb_rating, w.status, w.updated_at
            FROM watchlist w
            JOIN content c ON w.content_id = c.id
            WHERE w.user_id = %s AND w.status = %s
            ORDER BY w.updated_at DESC
        """
        cursor.execute(query, (user_id, status))
    else:
        query = """
            SELECT c.title, c.content_type, c.genre, c.release_year,
                   c.tmdb_rating, w.status, w.updated_at
            FROM watchlist w
            JOIN content c ON w.content_id = c.id
            WHERE w.user_id = %s
            ORDER BY w.updated_at DESC
        """
        cursor.execute(query, (user_id,))

    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results


def update_status(user_id, tmdb_id, new_status):
    db = get_db()
    cursor = db.cursor()

    query = """
        UPDATE watchlist w
        JOIN content c ON w.content_id = c.id
        SET w.status = %s, w.updated_at = CURRENT_TIMESTAMP
        WHERE w.user_id = %s AND c.tmdb_id = %s
    """
    cursor.execute(query, (new_status, user_id, tmdb_id))
    db.commit()
    cursor.close()
    db.close()
    return {"message": f"Status updated to: {new_status}"}


def remove_from_watchlist(user_id, tmdb_id):
    db = get_db()
    cursor = db.cursor()

    query = """
        DELETE w FROM watchlist w
        JOIN content c ON w.content_id = c.id
        WHERE w.user_id = %s AND c.tmdb_id = %s
    """
    cursor.execute(query, (user_id, tmdb_id))
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Removed from watchlist"}


def add_rating(user_id, tmdb_id, rating, review=None):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id FROM content WHERE tmdb_id = %s", (tmdb_id,))
    result = cursor.fetchone()
    if not result:
        return {"error": "Content not found. Add to watchlist first."}

    content_id = result[0]

    query = """
        INSERT INTO ratings (user_id, content_id, rating, review)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE rating = %s, review = %s, rated_at = CURRENT_TIMESTAMP
    """
    cursor.execute(query, (user_id, content_id, rating, review, rating, review))
    db.commit()
    cursor.close()
    db.close()
    return {"message": f"Rated {rating}/10 successfully"}
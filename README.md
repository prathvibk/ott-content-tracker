# 🎬 OTT Content Tracker & Recommendation Engine

A backend REST API system built with Python and Flask to track movies and shows
across OTT platforms like Netflix, Prime Video, and Hotstar.
Powered by real-time data from the TMDB API.

---

## 🚀 Features

- 🔍 **Search Movies & Shows** — Search any content using TMDB live data
- 📈 **Trending Content** — Fetch what's trending globally this week
- 📋 **Watchlist Management** — Add, update, and remove content from your watchlist
- ⭐ **Ratings & Reviews** — Rate and review movies and shows
- 🤖 **Recommendations** — Get personalized recommendations based on watch history
- 🗄️ **MySQL Database** — 6 interlinked tables for structured data storage

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.x |
| Framework | Flask |
| Database | MySQL |
| External API | TMDB API |
| Testing | Postman |
| Tools | Git, VS Code |

---

## 📁 Project Structure


ott-content-tracker/
│
├── modules/
│   ├── movies.py          # TMDB API integration & search
│   ├── watchlist.py       # Watchlist & ratings logic
│   └── recommendations.py # Recommendation engine
│
├── db/
│   └── schema.sql         # Database schema
│
├── config.py              # API key & DB configuration
├── main.py                # Flask app & all API routes
└── README.md

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.x
- MySQL
- TMDB API key (free at themoviedb.org)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/prathvibk/ott-content-tracker.git
cd ott-content-tracker

# 2. Install dependencies
pip install flask mysql-connector-python requests

# 3. Set up database
mysql -u root -p < db/schema.sql

# 4. Configure config.py
# Add your MySQL password and TMDB API key

# 5. Run the app
python main.py
```

---

## 📡 API Endpoints

### Movies
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/trending` | Get trending movies and shows |
| GET | `/search?query=inception` | Search movies and shows |
| GET | `/details/movie/{id}` | Get movie details |
| GET | `/details/tv/{id}` | Get TV show details |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/user/register` | Register a new user |

### Watchlist
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/watchlist/add` | Add content to watchlist |
| GET | `/watchlist/{user_id}` | Get user's watchlist |
| PUT | `/watchlist/update` | Update watchlist status |
| DELETE | `/watchlist/remove` | Remove from watchlist |

### Ratings & Recommendations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rate` | Rate and review content |
| GET | `/recommendations/{user_id}` | Get personalized recommendations |
| GET | `/top-rated?genre=Action` | Get top rated by genre |

---

## 🗄️ Database Schema

users → watchlist → content → platforms
↓
ratings → recommendations

6 tables: users, content, platforms, content_platforms, watchlist, ratings

---

## 🧪 Testing with Postman

### Register User
```json
POST /user/register
{
    "username": "prathvi",
    "email": "prathvibk686@gmail.com",
    "password": "prathvi123"
}
```

### Add to Watchlist
```json
POST /watchlist/add
{
    "user_id": 1,
    "tmdb_id": 76479,
    "content_type": "tv",
    "status": "want_to_watch"
}
```

### Rate Content
```json
POST /rate
{
    "user_id": 1,
    "tmdb_id": 76479,
    "rating": 8.5,
    "review": "Amazing show!"
}
```

---

## 🔐 Security

- Parameterized SQL queries to prevent SQL injection
- Role-based access control for sensitive operations
- Environment-based configuration for API keys

---

## 📌 Future Improvements

- [ ] Add JWT authentication
- [ ] Deploy to cloud (AWS / Render)
- [ ] Build React frontend
- [ ] Add data visualization dashboard
- [ ] Write unit tests with pytest

---

## 👨‍💻 Author

**Prathvi B K**
MCA Graduate — PES University, Bangalore
📧 prathvibk686@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/prathvi-bk)
⭐ [GitHub](https://github.com/prathvibk)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).




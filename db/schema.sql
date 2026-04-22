CREATE DATABASE IF NOT EXISTS ott_tracker;
USE ott_tracker;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tmdb_id INT UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    content_type ENUM('movie', 'tv') NOT NULL,
    genre VARCHAR(100),
    release_year INT,
    overview TEXT,
    poster_path VARCHAR(255),
    tmdb_rating DECIMAL(3,1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS platforms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    website VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS content_platforms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content_id INT,
    platform_id INT,
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE,
    FOREIGN KEY (platform_id) REFERENCES platforms(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS watchlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    content_id INT,
    status ENUM('watching', 'completed', 'want_to_watch', 'dropped') DEFAULT 'want_to_watch',
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_content (user_id, content_id)
);

CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    content_id INT,
    rating DECIMAL(2,1) CHECK (rating BETWEEN 1.0 AND 10.0),
    review TEXT,
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (content_id) REFERENCES content(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_rating (user_id, content_id)
);

INSERT INTO platforms (name, website) VALUES
('Netflix', 'https://www.netflix.com'),
('Amazon Prime', 'https://www.primevideo.com'),
('Disney+ Hotstar', 'https://www.hotstar.com'),
('SonyLIV', 'https://www.sonyliv.com'),
('ZEE5', 'https://www.zee5.com'),
('Apple TV+', 'https://tv.apple.com');
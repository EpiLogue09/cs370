-- Active: 1708197661893@@localhost@3306@DetectAIveDB
CREATE DATABASE IF NOT EXISTS DetectAIveDB;
USE DetectAIveDB;

CREATE TABLE stories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    story_name VARCHAR(255),
    surface_story TEXT,
    truth TEXT
);
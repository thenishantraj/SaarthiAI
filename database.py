import sqlite3
import json
from datetime import datetime
import hashlib

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chat history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            message TEXT,
            topic TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # User progress table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            topic TEXT,
            mastery_level INTEGER DEFAULT 0,
            interactions INTEGER DEFAULT 0,
            last_studied TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    """Register a new user"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hash_password(password))
        )
        conn.commit()
        return True, "Registration successful!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists!"
        elif "email" in str(e):
            return False, "Email already registered!"
        return False, "Registration failed!"
    finally:
        conn.close()

def login_user(username, password):
    """Authenticate user login"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        "SELECT id, username FROM users WHERE username = ? AND password = ?",
        (username, hash_password(password))
    )
    user = c.fetchone()
    conn.close()
    return user if user else None

def save_chat_message(user_id, role, message, topic="general"):
    """Save chat message to database"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_history (user_id, role, message, topic) VALUES (?, ?, ?, ?)",
        (user_id, role, message, topic)
    )
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=50):
    """Get user's chat history"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        "SELECT role, message, topic, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    history = c.fetchall()
    conn.close()
    return history

def update_user_progress(user_id, topic, mastery_change):
    """Update user's mastery level for a topic"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Check if topic exists for user
    c.execute(
        "SELECT id, mastery_level, interactions FROM user_progress WHERE user_id = ? AND topic = ?",
        (user_id, topic)
    )
    result = c.fetchone()
    
    if result:
        # Update existing topic
        new_mastery = min(100, max(0, result[1] + mastery_change))
        c.execute(
            "UPDATE user_progress SET mastery_level = ?, interactions = interactions + 1, last_studied = CURRENT_TIMESTAMP WHERE id = ?",
            (new_mastery, result[0])
        )
    else:
        # Insert new topic
        c.execute(
            "INSERT INTO user_progress (user_id, topic, mastery_level, interactions, last_studied) VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)",
            (user_id, topic, min(100, max(0, mastery_change)))
        )
    
    conn.commit()
    conn.close()

def get_user_progress(user_id):
    """Get user's progress data"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        "SELECT topic, mastery_level, interactions, last_studied FROM user_progress WHERE user_id = ? ORDER BY last_studied DESC",
        (user_id,)
    )
    progress = c.fetchall()
    conn.close()
    return progress

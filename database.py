import sqlite3

DB_PATH = "ai_tutor.db"

def initialize_db():
    """Creates the database and the necessary tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    # ✅ Create quiz_scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER,
            total_questions INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ✅ Create quiz_attempts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            question TEXT,
            user_answer TEXT,
            correct_answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ✅ Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# ✅ Function to connect to the database
def connect_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

# ✅ Save quiz score
def save_quiz_score(username, score, total_questions):
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO quiz_scores (username, score, total_questions) VALUES (?, ?, ?)",
                   (username, score, total_questions))
    conn.commit()
    conn.close()

# ✅ Get past quiz scores
def get_quiz_scores(username, limit=5):
    conn, cursor = connect_db()
    cursor.execute("SELECT score, total_questions, timestamp FROM quiz_scores WHERE username = ? ORDER BY timestamp DESC LIMIT ?",
                   (username, limit))
    past_scores = cursor.fetchall()
    conn.close()
    return past_scores

# ✅ Get class average score
def get_class_average_score():
    conn, cursor = connect_db()
    cursor.execute("SELECT AVG(score) FROM quiz_scores")
    avg_score = cursor.fetchone()[0]
    conn.close()
    return avg_score if avg_score is not None else 0  

# ✅ Get user quiz history
def get_user_quiz_history(username):
    conn, cursor = connect_db()
    cursor.execute("SELECT score, total_questions, timestamp FROM quiz_scores WHERE username = ? ORDER BY timestamp DESC LIMIT 5",
                   (username,))
    past_scores = cursor.fetchall()
    conn.close()
    return past_scores

# ✅ Get incorrect answers
def get_incorrect_answers(username):
    """Fetch incorrect quiz answers from the database."""
    conn, cursor = connect_db()
    
    cursor.execute("""
        SELECT question, user_answer, correct_answer 
        FROM quiz_attempts 
        WHERE username = ? AND user_answer != correct_answer
    """, (username,))
    
    incorrect_answers = cursor.fetchall()
    conn.close()
    
    return incorrect_answers

# ✅ Save incorrect answers after a quiz
def save_incorrect_answers(username, question, user_answer, correct_answer):
    """Saves incorrect quiz answers to the database."""
    conn, cursor = connect_db()
    cursor.execute("""
        INSERT INTO quiz_attempts (username, question, user_answer, correct_answer) 
        VALUES (?, ?, ?, ?)
    """, (username, question, user_answer, correct_answer))
    conn.commit()
    conn.close()

# ✅ Ensure DB is initialized on first run
initialize_db()
import sqlite3

DATABASE_FILE = "highscores.db"

def create_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    return conn

def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS highscores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def load_highscores():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, score FROM highscores ORDER BY score DESC')
    rows = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "score": row[1]} for row in rows]

def update_highscores(name, score):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO highscores (name, score) VALUES (?, ?)', (name, score))
    conn.commit()
    conn.close()

# Initialisiere die Datenbank (Tabelle wird automatisch erstellt, falls sie nicht existiert)
init_db()

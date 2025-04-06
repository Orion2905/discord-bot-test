import sqlite3

def initialize_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, points INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS presence (id INTEGER PRIMARY KEY, seconds INTEGER)')
    conn.commit()
    conn.close()

def track_presence(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS presence (id INTEGER PRIMARY KEY, seconds INTEGER)')
    
    c.execute('SELECT seconds FROM presence WHERE id = ?', (user_id,))
    result = c.fetchone()
    print(f"Tracking presence for user {user_id}: {result}")
    if result:
        c.execute('UPDATE presence SET seconds = seconds + 60 WHERE id = ?', (user_id,))
    else:
        c.execute('INSERT INTO presence (id, seconds) VALUES (?, ?)', (user_id, 60))

    conn.commit()
    conn.close()

def get_top_users(limit=10):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, seconds FROM presence ORDER BY seconds DESC LIMIT ?', (limit,))
    results = c.fetchall()
    conn.close()
    return results


def get_or_create_presence(user_id: int) -> int:
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT seconds FROM presence WHERE id = ?", (user_id,))
    result = c.fetchone()

    if result is None:
        c.execute("INSERT INTO presence (id, seconds) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        seconds = 0
    else:
        seconds = result[0]

    conn.close()
    return seconds
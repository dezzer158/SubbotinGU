import sqlite3

conn = sqlite3.connect('posts.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT
)
''')

conn.commit()
conn.close()

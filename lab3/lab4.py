import sqlite3
import requests

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

response = requests.get('https://jsonplaceholder.typicode.com/posts')

posts = response.json()

conn = sqlite3.connect('posts.db')
cursor = conn.cursor()

for post in posts:
    cursor.execute('''
    INSERT INTO posts (id, user_id, title, body)
    VALUES (?, ?, ?, ?)
    ''', (post['id'], post['userId'], post['title'], post['body']))

def get_posts_by_user(user_id):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    posts = cursor.fetchall()

    conn.close()
    return posts

user_posts = get_posts_by_user(1)
for post in user_posts:
    print(post)

conn.commit()
conn.close()

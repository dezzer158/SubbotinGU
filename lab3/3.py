conn = sqlite3.connect('posts.db')
cursor = conn.cursor()

for post in posts:
    cursor.execute('''
    INSERT INTO posts (id, user_id, title, body)
    VALUES (?, ?, ?, ?)
    ''', (post['id'], post['userId'], post['title'], post['body']))

conn.commit()
conn.close()

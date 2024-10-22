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

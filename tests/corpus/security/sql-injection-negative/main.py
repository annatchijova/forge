def search(user):
    cursor.execute("SELECT * FROM users WHERE name = ?", (user,))

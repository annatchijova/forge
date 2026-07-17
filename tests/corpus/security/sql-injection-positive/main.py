@app.post("/search")
def search(user):
    cursor.execute(f"SELECT * FROM users WHERE name = '{user}'")

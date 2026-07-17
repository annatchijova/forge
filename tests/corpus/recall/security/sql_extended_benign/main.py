QUERIES = {"active": "SELECT * FROM t WHERE active = 1"}


def find(cur, user_id, user_choice):
    cur.execute("SELECT * FROM t WHERE id = ?", (user_id,))
    cur.execute("SELECT * FROM t WHERE id = %s", (user_id,))
    cur.execute("SELECT * FROM t WHERE active = 1")
    return cur.execute(QUERIES[user_choice])

import sqlite3

conn = sqlite3.connect('../../data/crawled_web.db')
_cursor = conn.cursor()

def insert_result(params):
    sql = "INSERT INTO result VALUES (?, ?, ?)"
    _cursor.execute(sql, (params))

def get_intial_url_load():
    sql = "SELECT url FROM result"
    rows = _cursor.execute(sql)
    return rows.fetchall()
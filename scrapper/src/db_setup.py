import sqlite3
conn = sqlite3.connect('crawled_web.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE result
             (url text, title text, content text)''')
conn.close()
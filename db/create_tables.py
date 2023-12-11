import sqlite3

conn = sqlite3.connect('project.sql3')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS auth (
                    username TEXT PRIMARY KEY,
                    password TEXT
                )''')

conn.commit()

conn.close()
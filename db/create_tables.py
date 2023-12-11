import sqlite3

conn = sqlite3.connect('project.sql3')

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS auth (
                    username TEXT PRIMARY KEY,
                    password TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    username INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

conn.commit()

conn.close()
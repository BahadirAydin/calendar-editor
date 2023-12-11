import sqlite3

conn = sqlite3.connect("project.sql3")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS auth (
                    id INTEGER PRIMARY KEY,
                    password TEXT,
                    FOREIGN KEY (id) REFERENCES user(id)
                )"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    username INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )"""
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    fullname TEXT
    )
"""
)

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        description TEXT,
        protection TEXT,
        FOREIGN KEY (user_id) REFERENCES user(id) ) 
           """
)

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS event(
      id INTEGER PRIMARY KEY,
      schedule_id INTEGER,
      start_time TEXT,
      end_time TEXT,
      period TEXT,
      description TEXT,
      location TEXT,
      protection TEXT,
      assignee TEXT,
      FOREIGN KEY (assignee) REFERENCES user(username),
      FOREIGN KEY (schedule_id) REFERENCES schedule(id) ) 
    """
)

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS view (
            id INTEGER,
            user_id INTEGER,
            schedule_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (schedule_id) REFERENCES schedule(id),
            PRIMARY KEY (id, user_id, schedule_id)
            )
        """
)

conn.commit()

conn.close()

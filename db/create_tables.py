import sqlite3

conn = sqlite3.connect("project.sql3")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS auth (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    FOREIGN KEY (username) REFERENCES user(username)
                )"""
)

cursor.execute(
    '''CREATE TABLE auth_token (
            token TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            expiration_date TIMESTAMP NOT NULL,
            FOREIGN KEY (username) REFERENCES user(username)
        );'''
)

cursor.execute(
    """CREATE TABLE IF NOT EXISTS user (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    fullname TEXT
    )
"""
)

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS schedule (
        id TEXT PRIMARY KEY,
        user_id INTEGER,
        description TEXT,
        protection TEXT,
        FOREIGN KEY (user_id) REFERENCES user(id) ) 
           """
)

cursor.execute(
    """ CREATE TABLE IF NOT EXISTS event(
      id TEXT PRIMARY KEY,
      schedule_id INTEGER,
      start_time TEXT,
      end_time TEXT,
      period TEXT,
      description TEXT,
      event_type TEXT,
      location TEXT,
      protection TEXT,
      assignee TEXT,
      FOREIGN KEY (assignee) REFERENCES user(username),
      FOREIGN KEY (schedule_id) REFERENCES schedule(id)) 
    """
)

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS views_and_schedules (
            view_id TEXT,
            schedule_id TEXT,
            FOREIGN KEY (schedule_id) REFERENCES schedule(id),
            FOREIGN KEY (view_id) REFERENCES view(id),
            PRIMARY KEY (schedule_id, view_id)
            )
        """
)

cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS users_and_views (
            user_id TEXT,
            view_id TEXT,
            description TEXT,
            is_attached INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (view_id) REFERENCES view(id),
            PRIMARY KEY (user_id, view_id)
            )
        """
)

conn.commit()

conn.close()

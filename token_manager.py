import sqlite3
import secrets
import datetime

class TokenManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TokenManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.db_path = 'project.sql3'

    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        return conn

    def generate_token(self, username, duration_hours=1):
        print(username)
        token = secrets.token_hex(16)
        expiration_date = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)
        print(username)
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO auth_token (token, username, expiration_date) VALUES (?, ?, ?)",
                       (token, username, expiration_date))
        conn.commit()
        conn.close()

        return token

    def verify_token(self, token):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM auth_token WHERE token = ? AND expiration_date > ?",
                       (token, datetime.datetime.now()))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result is not None else None
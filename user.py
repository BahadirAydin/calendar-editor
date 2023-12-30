import uuid
import hashlib
import json
import sqlite3

class User:
    def __init__(self, username, email, fullname, passwd):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = hashlib.sha256(passwd.encode()).hexdigest()
        self.schedules = []
        self.views = []

    def get(self):
        return json.dumps(
            {
                "id": str(self.id),
                "username": self.username,
                "email": self.email,
                "fullname": self.fullname,
            }
        )

    def getId(self):
        return self.id

    @staticmethod
    def login(uname, passwd):
        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            query = f"select username,password from auth where username='{uname}'"
            row = c.execute(query)
        user = row.fetchone()
        if user != None and user[1] == str(hashlib.sha256(passwd.encode()).hexdigest()):
            return True
        return False

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"No attribute named {key}")

    def delete(self):
        self.username = None
        self.email = None
        self.fullname = None
        self.passwd = None
        self.id = None

    def save(self):
        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            if c.execute(
                "select * from auth where username=?", (self.username,)
            ).fetchone():
                return False
            c.execute(
                "insert into user values (?,?,?,?)",
                (self.id, self.username, self.email, self.fullname),
            )
            c.execute("insert into auth values (?,?)", (self.username, self.passwd))

    def authenticate(self, passwd):
        return self.passwd == hashlib.sha256(passwd.encode()).hexdigest()

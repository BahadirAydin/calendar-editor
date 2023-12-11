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

    def auth(self, passwd):
        return self.passwd == hashlib.sha256(passwd.encode()).hexdigest()

    def login(self, uname, passwd):
        with sqlite3.connect('project.sql3') as db:
            c = db.cursor()
            row = c.execute('select username,password from auth where username=?',(uname))
        if hashlib.sha256(passwd.encode()).hexdigest() == row[1]:
            return True
        return False
    
    def adduser(self, user,passwd):
        encpasswd = hashlib.sha256(passwd.encode()).hexdigest()
        with sqlite3.connect('project.sql3') as db:
            c = db.cursor()
            c.execute('insert into auth values (?,?)',(user,encpasswd))
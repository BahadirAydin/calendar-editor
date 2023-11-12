from schedule import Schedule
import uuid
import hashlib


class User:
    def __init__(self, username, email, fullname, passwd):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = hashlib.sha256(passwd.encode()).hexdigest()
        self.id = uuid.uuid4()

    def getid(self):
        return self.id

    def get(self):
        # json-like object
        return {
            "username": self.username,
            "email": self.email,
            "fullname": self.fullname,
            "passwd": self.passwd,
            "id": self.id,
        }

    def update(self, **kw):
        for k, v in kw.items():
            if k == "username":
                self.username = v
            elif k == "email":
                self.email = v
            elif k == "fullname":
                self.fullname = v
            elif k == "passwd":
                self.passwd = v
            else:
                raise KeyError(f"Invalid key {k}")

    def delete(self):
        self.username = None
        self.email = None
        self.fullname = None
        self.passwd = None
        self.id = None

class View:
    def __init__(self, description):
        self.description = description
        self.schedules = []
    def addSchedule(self, schid):
        pass
        # TODO there should be a structure that holds all the schedules


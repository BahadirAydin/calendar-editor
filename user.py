from schedule import Schedule
import uuid
import hashlib


class User:
    def __init__(self, username, email, fullname, passwd):
        self.id = uuid.uuid4()
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = hashlib.sha256(passwd.encode()).hexdigest()

    def getId(self, id):
        return self.id

    def get(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "fullname": self.fullname
        }

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

class View:
    def __init__(self, description):
        self.description = description
        self.schedules = []
    def addSchedule(self, schid):
        pass
        # TODO there should be a structure that holds all the schedules


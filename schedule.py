import json
import uuid
from event import Event
import sqlite3

class Schedule:
    def __init__(self, description, protection, user_id):
        self.id = uuid.uuid4()
        self.description = description
        self.protection = protection
        self.user_id = user_id
        self.events = []

    def add_event(self, event):
        if isinstance(event, Event):
            self.events.append(event)
        else:
            raise TypeError("The object must be an instance of Event.")

    def get(self):
        return json.dumps(
            {
                "id": str(self.id),
                "description": self.description,
                "protection": self.protection,
                "events": [event.get() for event in self.events],
            }
        )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"No attribute named {key}")

    def delete_event(self, event_id):
        self.events = [event for event in self.events if event.id != event_id]

    def list_events(self):
        return [event.get() for event in self.events]

    def search(self, **kwargs):
        pass

    def delete(self):
        pass
    
    def save(self):
        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            if c.execute("select * from schedule where id=?", (self.id,)).fetchone():
                return False
            c.execute("insert into user schedule (?,?,?,?)", (self.id, self.user_id, self.description, self.protection))

import uuid
import sqlite3

event_types = ["MEETING", "SEMINAR", "LECTURE", "APPOINTMENT", "OFFICEHOUR", "FUN"]


class Event:
    def __init__(
        self,
        event_type,
        start,
        end,
        period,
        description,
        location,
        protection,
        assignee,
        schedule_id,
    ):
        if event_type not in event_types:
            print("Invalid event type")
            return None
        self.id = uuid.uuid4()
        self.event_type = event_type
        self.start = start
        self.end = end
        self.period = period
        self.description = description
        self.location = location
        self.protection = protection
        self.assignee = assignee
        self.schedule_id = schedule_id

    def get(self):
        return {
            "id": str(self.id),
            "event_type": self.event_type,
            "start": self.start,
            "end": self.end,
            "period": self.period,
            "description": self.description,
            "location": self.location,
            "protection": self.protection,
            "assignee": self.assignee,
            "schedule_id": self.schedule_id,
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"No attribute named {key}")

    def delete(self):
        pass

    def save(self):
        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            if c.execute("select * from event where id=?", (str(self.id),)).fetchone():
                return False
            c.execute(
                "insert into event values (?,?,?,?,?,?,?,?,?)",
                (
                    str(self.id),
                    str(self.schedule_id),
                    self.start,
                    self.end,
                    self.period,
                    self.description,
                    self.event_type,
                    self.location,
                    self.protection,
                    self.assignee,
                ),
            )

import uuid

event_types = ["MEETING", "SEMINAR", "LECTURE", "APPOINTMENT", "OFFICEHOUR", "FUN"]

class Event:
    def __init__(self, event_type, start, end, period, description, location, protection, assignee):
        if event_type not in event_types:
            raise ValueError("Unknown event type")
        self.id = uuid.uuid4()
        self.event_type = event_type
        self.start = start
        self.end = end
        self.period = period
        self.description = description
        self.location = location
        self.protection = protection
        self.assignee = assignee

    def get(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "start": self.start,
            "end": self.end,
            "period": self.period,
            "description": self.description,
            "location": self.location,
            "protection": self.protection,
            "assignee": self.assignee
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"No attribute named {key}")

    def delete(self):
        pass

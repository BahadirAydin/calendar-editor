import json
import uuid
from event import Event


class Schedule:
    # CRUD
    def __init__(self, description, protection):
        self.id = uuid.uuid4()
        self.description = description
        self.protection = protection
        self.events = []

    def get(self):
        # json-like object
        return json.dumps(
            {"description": self.description, "protection": self.protection}
        )

    def update(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    def delete(self):
        self.description = None
        self.protection = None

    # ID
    def getid(self):
        return self.id

    def newEvent(
        self,
        event_type,
        start,
        end,
        period,
        description,
        location,
        protection,
        assignee,
    ):
        event = Event(
            event_type,
            start,
            end,
            period,
            description,
            location,
            protection,
            assignee,
        )
        self.events.append(event)
        return event

    def getEvent(self, event_id):
        for event in self.events:
            if event.getid() == event_id:
                return event
        return None

    def updateEvent(self, event_id, **kw):
        event = self.getEvent(event_id)
        if event is not None:
            event.update(**kw)

    def deleteEvent(self, event_id):
        event = self.getEvent(event_id)
        if event is not None:
            event.delete()
            self.events.remove(event)

    def isReadable(self, event):
        # TODO: it will be implemented in the second phase.
        # no implementation for now
        pass

    # Only events that are readable by the user is listed
    def listEvents(self):
        return [event for event in self.events if self.isReadable(event)]

    def search(self, **kw):
        # for string based paramters it is case insensitive substring search
        # for start and end it defines interval overlapping with the event
        results = []

        for event in self.events:
            match = True

            for k, v in kw.items():
                if k in ["description", "location", "protection", "assignee"]:
                    if not str(v).lower() in str(getattr(event, k)).lower():
                        match = False
                        break
                elif k == "start":
                    if event.end < v:
                        match = False
                        break
                elif k == "end":
                    if event.start > v:
                        match = False
                        break
                else:
                    raise ValueError("Unknown parameter")

            if match:
                results.append(event)

        return results

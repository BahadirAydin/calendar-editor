import uuid

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
    ):
        if event_type not in event_types:
            raise ValueError("Unknown event type")
        self.id = uuid.uuid4()
        self.event_type = event_type
        self.start = start
        self.end = end
        self.period = period
        self.description = description
        self.location = location
        # defines who can view/modify the event
        self.protection = protection
        # list of users to invite the event
        self.assignee = assignee

    # ID
    def getid(self):
        return self.id

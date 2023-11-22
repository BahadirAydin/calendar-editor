class View:
    def __init__(self, description):
        self.description = description
        self.schedules = {}  # Stores schedules with their respective filters
        self.current_view = None  # To keep track of the main view for notifications

    def addSchedule(self, schedule_id, schedule):
        self.schedules[schedule_id] = {"schedule": schedule, "filters": {}}

    def deleteSchedule(self, schedule_id):
        if schedule_id in self.schedules:
            del self.schedules[schedule_id]

    def setFilter(self, schedule_id, **kwargs):
        if schedule_id in self.schedules:
            self.schedules[schedule_id]["filters"] = kwargs

    def removefilters(self, schedule_id):
        if schedule_id in self.schedules:
            self.schedules[schedule_id]["filters"] = {}

    def listItems(self):
        for schedule_id, data in self.schedules.items():
            filters = data["filters"]
            for event in data["schedule"].events:
                if self._matches_filters(event, filters):
                    yield event

    def _matches_filters(self, event, filters):
        for key, value in filters.items():
            if not hasattr(event, key) or getattr(event, key) != value:
                return False
        return True

    def attachView(self, view_id):
        self.current_view = view_id

    def detachView(self, view_id):
        if self.current_view == view_id:
            self.current_view = None

    @classmethod
    def listViews(cls, user):
        return cls.views.get(user.id, [])

    @classmethod
    def getView(cls, view_id):
        return cls.views.get(view_id)

import uuid
import sqlite3

class View:
    current_view = None  # To keep track of the main view for notifications

    def __init__(self, description):
        self.id = uuid.uuid4()
        self.description = description
        self.schedules = {}  # Stores schedules with their respective filters

    def addSchedule(self, schedule_id, schedule):
        self.schedules[schedule_id] = {"schedule": schedule, "filters": {}}
        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            if c.execute(
                "select * from views_and_schedules where schedule_id=? and view_id", (schedule_id, self.id)
            ).fetchone():
                return False
            c.execute("insert into views_and_schedules values (?,?)", (self.id, self.description))
            db.commit()

    def deleteSchedule(self, schedule_id):
        if schedule_id in self.schedules:
            del self.schedules[schedule_id]
        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            if c.execute(
                "delete from views_and_schedules where schedule_id=? and view_id=?", (schedule_id, self.id,)
            ).fetchone():
                return False
            db.commit()

    def setFilter(self, schedule_id, **kwargs):
        if schedule_id in self.schedules:
            self.schedules[schedule_id]["filters"] = kwargs

    def removefilters(self, schedule_id):
        if schedule_id in self.schedules:
            self.schedules[schedule_id]["filters"] = {}

    def listItems(self):
        for _, data in self.schedules.items():
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

    def attachView(self, view_id, user_id):
        self.current_view = view_id
        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            if c.execute(
                "insert into users_and_views values (?,?)", (user_id, view_id)
            ).fetchone():
                return False
            db.commit()


    def detachView(self, view_id):
        if self.current_view == view_id:
            self.current_view = None

        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            if c.execute(
                "delete from users_and_views where view_id=(?,)", (view_id,)
            ).fetchone():
                return False
            db.commit()


    def save(self):
        with sqlite3.connect("project.sql3") as db:
            c = db.cursor()
            if c.execute(
                "select * from view where id=?", (self.id,)
            ).fetchone():
                return False
            c.execute("insert into view values (?,?)", (self.id, self.description))
            db.commit()

    @classmethod
    def listViews(cls, user):
        return cls.views.get(user.id, [])

    @classmethod
    def getView(cls, view_id):
        return cls.views.get(view_id)

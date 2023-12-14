from user import User
from schedule import Schedule
from view import View
from event import Event
import threading
import sqlite3
import uuid
import datetime

# NOTE
# WE HAVE CREATE, GET, UPDATE, DELETE
# FOR USER, SCHEDULE, VIEW, EVENT
# TODO VIEW FUNCTIONS, I COULDNT UNDERSTAND THE LOGIC

# TODO SELAM DENİZ
# BEN BU TOKEN MANTIĞINI ANLAMADIM BİRAZ BAKABİLİR MİSİN
# SANKİ BİZİM SESSON'DA ÜRETTİĞİMİZ TOKENI DİĞER SOCKET'E
# GÖNDERMEMİZ GEREKİYOR GİBİ DURUYOR AMA BİLMİYORUM


class ScheduleManager:
    _instance = None
    _session_map = dict()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScheduleManager, cls).__new__(cls)
            cls._instance.mutex = threading.Lock()
        return cls._instance

    # -------------------------
    # User-related Functions
    # -------------------------
    def create_or_get_user(self, username, email, fullname, passwd):
        with self.mutex:
            if self.user_exists(username):
                return None
            user = User(username, email, fullname, passwd)
            user.save()
            return user

    def get_user_id(self, username):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select id from user where username='{username}'"
            row = c.execute(query)
            return row.fetchone()[0]

    def get_user_by_id(self, user_id):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select * from user where id={user_id}"
            row = c.execute(query)
            return row.fetchone()

    def user_exists(self, username):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select * from user where username='{username}'"
        row = c.execute(query)
        if row.fetchone():
            return True
        return False

    def update_user(self, **kwargs):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"update user set "
            for key, value in kwargs.items():
                query += f"{key}={value},"
            query = query[:-1]
            query += f" where id={kwargs['id']}"
            c.execute(query)
            db.commit()

    def delete_user_by_id(self, user_id):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"delete from user where id={user_id}"
            c.execute(query)
            db.commit()

    def save_session(self, thread_id, username, obj):
        if thread_id not in self._session_map:
            self._session_map[thread_id] = {username: username, obj: obj}

    def is_logged_in(self, username):
        for thread_id in self._session_map:
            if self._session_map[thread_id]["username"] == username:
                return True
        return False

    # -------------------------
    # Schedule-related Functions
    # -------------------------

    def create_schedule(self, userid, description, protection_level):
        with self.mutex:
            if self.schedule_exists(userid, description):
                return None
            schedule = Schedule(userid, description, protection_level)
            schedule.save()
            return schedule

    def get_schedule_by_id(self, schid):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select * from schedule where id={schid}"
            row = c.execute(query)
            return row.fetchone()

    def get_schedule_id(self, userid, description):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select id from schedule where user_id={userid} and description='{description}'"
        row = c.execute(query)
        return row.fetchone()[0]

    def get_schedule_by_description(self, userid, description):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select * from schedule where user_id={userid} and description='{description}'"
            row = c.execute(query)
            return row.fetchone()

    def schedule_exists(self, userid, description):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select * from schedule where user_id={userid} and description='{description}'"
        row = c.execute(query)
        if row.fetchone():
            return True
        return False

    def update_schedule(self, **kwargs):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"update schedule set "
            for key, value in kwargs.items():
                query += f"{key}={value},"
            query = query[:-1]
            query += f" where id={kwargs['id']}"
            c.execute(query)
            db.commit()

    def delete_schedule(self, user, schid):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"delete from schedule where id={schid}"
            c.execute(query)
            db.commit()

    # -------------------------
    # View-related Functions
    # -------------------------

    def delete_view_by_id(self, view_id):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"delete from view where id={view_id}"
            c.execute(query)
            db.commit()

    # -------------------------
    # Event-related Functions
    # -------------------------

    def create_event(
        self,
        schid,
        event_type,
        start,
        end,
        period,
        description,
        location,
        protection,
        assignee,
    ):
        with self.mutex:
            if self.event_exists(schid, description, start, end):
                return None
            event = Event(
                event_type,
                start,
                end,
                period,
                description,
                location,
                protection,
                assignee,
                schid,
            )
            event.save()
            return event

    def get_event_by_id(self, event_id):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select * from event where id={event_id}"
            row = c.execute(query)
            return row.fetchone()

    def get_event_id(self, schid, description):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select id from event where schedule_id={schid} and description='{description}'"
            row = c.execute(query)
            return row.fetchone()[0]

    def event_exists(self, schid, description, start, end):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select * from event where schedule_id={schid} and description='{description}' and start='{start}' and end='{end}'"
            row = c.execute(query)
            if row.fetchone():
                return True
            return False

    def update_event(self, **kwargs):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"update event set "
            for key, value in kwargs.items():
                query += f"{key}={value},"
            query = query[:-1]
            query += f" where id={kwargs['id']}"
            c.execute(query)
            db.commit()

    def delete_event(self, event_id):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"delete from event where id={event_id}"
            c.execute(query)
            db.commit()

    # -------------------------
    # Other Helper Functions
    # -------------------------

    def is_user_authenticated(self, username):
        for thread_id in self._session_map:
            if self._session_map[thread_id]["username"] == username:
                return True

    def get_user_by_thread_id(self, thread_id):
        return self._session_map[thread_id].get("username")

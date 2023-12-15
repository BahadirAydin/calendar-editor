from os import wait
from user import User
from schedule import Schedule
from view import View
from event import Event
import threading
import sqlite3
import uuid
import hashlib
import datetime


class ScheduleManager:
    _instance = None
    _session_map = dict()
    users = []
    schedules = []
    events = []
    views = []
    users_and_views = []
    views_and_schedules = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScheduleManager, cls).__new__(cls)
            cls._instance.mutex = threading.Lock()
        return cls._instance

    # -------------------------
    # User-related Functions
    # -------------------------
    def create_user(self, username, email, fullname, passwd):
        with self.mutex:
            if self.user_exists(username):
                return None
            user = User(username, email, fullname, passwd)
            user.save()
            self.users.append(user)
            return user

    def get_user_id(self, username):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select id from user where username='{username}'"
            row = c.execute(query)
            v = row.fetchone()
            if v is None:
                return None
            return v[0]

    def get_user_by_id(self, user_id):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select * from user where id='{user_id}'"
        row = c.execute(query)
        v = row.fetchone()
        if v is None:
            return None

        return {"id": v[0], "username": v[1], "email": v[2], "fullname": v[3]}

    def get_username_by_id(self, user_id):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select username from user where id='{user_id}'"
        row = c.execute(query)
        v = row.fetchone()
        if v is None:
            return None
        return v[0]

    def user_exists(self, username):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select * from user where username='{username}'"
        row = c.execute(query)
        if row.fetchone():
            return True
        return False

    def update_user(self, user_id, new_password):
        with self.mutex:
            try:
                db = sqlite3.connect("project.sql3")
                c = db.cursor()
                username = self.get_username_by_id(user_id)
                pwd = str(hashlib.sha256(new_password.encode()).hexdigest())
                query = f"update auth set password='{pwd}' where username='{username}'"
                c.execute(query)
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def delete_user_by_id(self, user_id):
        with self.mutex:
            try:
                db = sqlite3.connect("project.sql3")
                c = db.cursor()
                username = self.get_username_by_id(user_id)
                query = f"delete from auth where username='{username}'"
                c.execute(query)
                query = f"delete from schedule where user_id='{user_id}'"
                c.execute(query)
                query = f"delete from user where id='{user_id}'"
                c.execute(query)
                db.commit()
                for user in self.users:
                    if user.id == user_id:
                        self.users.remove(user)
                return True
            except Exception as e:
                print(e)
                return False

    def save_session(self, thread_id, username, obj):
        if thread_id not in self._session_map:
            self._session_map[thread_id] = {"username": username, "obj": obj}

    def is_logged_in(self, username):
        for thread_id in self._session_map:
            if self._session_map[thread_id]["username"] == username:
                return True
        return False

    # -------------------------
    # Schedule-related Functions
    # -------------------------

    def create_schedule(self, description, protection_level, userid):
        with self.mutex:
            if self.schedule_exists(userid, description):
                return None
            schedule = Schedule(description, protection_level, userid)
            schedule.save()
            self.schedules.append(schedule)
            return schedule

    def get_schedule_by_id(self, schid):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select * from schedule where id='{schid}'"
            row = c.execute(query)
            return row.fetchone()

    def get_schedule_id(self, userid, description):
        try:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select id from schedule where user_id='{userid}' AND description='{description}'"
            row = c.execute(query)
            v = row.fetchone()
            if v is None:
                return None
            return v[0]
        except Exception as e:
            print(e)
            return None

    def get_schedule_by_description(self, userid, description):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select id from schedule where user_id='{userid}' AND description='{description}'"
            print(query)
            row = c.execute(query)
            v = row.fetchone()
            if v is None:
                return None
            return v[0]

    def get_schedule_obj(self, schid):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"select * from schedule where id='{schid}'"
            print(query)
            row = c.execute(query)
            v = row.fetchone()
            if v is None:
                return None
            query = f"select * from event where schedule_id='{schid}'"
            print(query)
            row = c.execute(query)
            events = row.fetchall()
            data = {
                "id": v[0],
                "description": v[2],
                "protection": v[3],
                "user_id": v[1],
                "events": events,
            }
            return data

    def schedule_exists(self, userid, description):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select * from schedule where user_id='{userid}' AND description='{description}'"
        print(query)
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

    def delete_schedule(self, schid):
        with self.mutex:
            try:
                db = sqlite3.connect("project.sql3")
                c = db.cursor()
                query = f"delete from event where schedule_id='{schid}'"
                c.execute(query)
                query = f"delete from schedule where id='{schid}'"
                c.execute(query)
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False

    # -------------------------
    # View-related Functions
    # -------------------------

    def delete_view_by_id(self, view_id):
        with self.mutex:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = f"delete from view where id='{view_id}'"
            c.execute(query)
            db.commit()

    def get_view_id_by_description(self, description):
        try:
            db = sqlite3.connect("project.sql3")
            c = db.cursor()
            query = (
                f"select view_id from users_and_views where description='{description}'"
            )
            row = c.execute(query)
            v = row.fetchone()
            if v is None:
                return None
            return v[0]
        except Exception as e:
            print(e)
            return None

    def get_schedules_in_view(self, view_id):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select schedule_id from views_and_schedules where view_id='{view_id}'"
        row = c.execute(query)
        return row.fetchall()

    def view_exists(self, view_id):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select * from users_and_views where view_id='{ view_id}'"
        row = c.execute(query)
        if row.fetchone():
            return True
        return False

    def is_user_attached(self, user_id):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = (
            f"select * from users_and_views where user_id='{user_id}' AND is_attached=1"
        )
        row = c.execute(query)
        if row.fetchone():
            return True
        return False

    def create_view(self, description, user_id):
        with self.mutex:
            try:
                view = View(description)
                view.save(user_id)
                self.views.append(view)
                return True
            except Exception as e:
                print(e)
                return False

    def add_to_view(self, view_id, schedule_id):
        with self.mutex:
            try:
                db = sqlite3.connect("project.sql3")
                c = db.cursor()
                query = f"insert into views_and_schedules values ('{view_id}', '{schedule_id}')"
                c.execute(query)
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def attach_view(self, view_id, user_id):
        with self.mutex:
            try:
                db = sqlite3.connect("project.sql3")
                c = db.cursor()
                query = f"update users_and_views set is_attached=1 where user_id='{user_id}' AND view_id='{view_id}'"
                print(query)
                c.execute(query)
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def detach_view(self, view_id, user_id):
        with self.mutex:
            try:
                db = sqlite3.connect("project.sql3")
                c = db.cursor()
                query = f"update users_and_views set is_attached=0 where user_id='{user_id}' AND view_id='{view_id}'"
                c.execute(query)
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def is_view_attached(self, view_id, user_id):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select * from users_and_views where user_id='{user_id}' AND view_id='{view_id}' AND is_attached=1"
        print("CHECK", query)
        row = c.execute(query)
        if row.fetchone():
            return True
        return False

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
            query = f"select id from event where schedule_id='{schid}' AND description='{description}'"
            row = c.execute(query)
            return row.fetchone()[0]

    def event_exists(self, schid, description, start, end):
        db = sqlite3.connect("project.sql3")
        c = db.cursor()
        query = f"select * from event where schedule_id='{schid}' AND description='{description}' AND start_time='{start}' AND end_time='{end}'"
        print(query)
        row = c.execute(query)
        if row.fetchone():
            return True
        return False

    def update_event(
        self,
        schid,
        old_description,
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
            try:
                db = sqlite3.connect("project.sql3")
                c = db.cursor()
                query = f"update event set description='{description}', event_type='{event_type}', start_time='{start}', end_time='{end}', period='{period}', location='{location}', protection='{protection}', assignee='{assignee}' where schedule_id='{schid}' AND description='{old_description}'"
                c.execute(query)
                db.commit()
                return True
            except Exception as e:
                print(e)
                return False

    def delete_event(self, event_id):
        with self.mutex:
            try:
                db = sqlite3.connect("project.sql3")
                c = db.cursor()
                query = f"delete from event where id='{event_id}'"
                c.execute(query)
                db.commit()
            except Exception as e:
                print(e)
                return False

    # -------------------------
    # Other Helper Functions
    # -------------------------

    def is_user_authenticated(self, username):
        for thread_id in self._session_map:
            if self._session_map[thread_id]["username"] == username:
                return True

    def get_user_by_thread_id(self, thread_id):
        if thread_id in self._session_map:
            return self._session_map[thread_id].get("username")

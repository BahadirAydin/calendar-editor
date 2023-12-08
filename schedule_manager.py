from schedule import Schedule
from user import User
from view import View
from event import Event
import threading


class ScheduleManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScheduleManager, cls).__new__(cls)
            cls._instance.users = []
            cls._instance.mutex = threading.Lock()
        return cls._instance

    def get_user(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user.get()
        return None

    def get_schedule(self, schid):
        for user in self.users:
            for schedule in user.schedules:
                if schedule.id == schid:
                    return schedule.get()
        return None

    def create_user(self, username, email, fullname, passwd):
        with self.mutex:
            for user in self.users:
                if user.username == username or user.email == email:
                    return user.id

            user = User(username, email, fullname, passwd)
            self.users.append(user)
            return user.id

    def user_instance(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def schedule_instance(self, schid):
        for user in self.users:
            for schedule in user.schedules:
                if schedule.id == schid:
                    return schedule
        return None

    def delete_user(self, user):
        with self.mutex:
            self.users.remove(user)

    def create_schedule(self, userid, description, protection_level):
        with self.mutex:
            schedule = Schedule(description, protection_level)
            user = self.user_instance(userid)
            user.schedules.append(schedule)
            return schedule.id

    def delete_schedule(self, user, schid):
        with self.mutex:
            schedule = self.schedule_instance(schid)
            user.schedules.remove(schedule)

    def create_view(self, userid, description):
        with self.mutex:
            view = View(description)
            user = self.user_instance(userid)
            user.views.append(view)
            return view.id

    def view_instance(self, viewid):
        for user in self.users:
            for view in user.views:
                if view.id == viewid:
                    return view
        return None

    def add_schedule_to_view(self, viewid, schid):
        with self.mutex:
            view = self.view_instance(viewid)
            schedule = self.schedule_instance(schid)
            view.addSchedule(schid, schedule)
            return view.id

    def delete_view(self, user, view):
        with self.mutex:
            user.views.remove(view)

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
            schedule = self.schedule_instance(schid)
            schedule.events.append(event)
            return event.id

    def event_instance(self, event_id):
        for user in self.users:
            for schedule in user.schedules:
                for event in schedule.events:
                    if event.id == event_id:
                        return event
        return None

    def delete_event(self, schedule, event):
        with self.mutex:
            schedule.events.remove(event)

from schedule_manager import ScheduleManager
from user import User
from view import View
from schedule import Schedule
from event import Event
import sqlite3


def retrieve_objects():
    conn = sqlite3.connect("project.sql3")
    cursor = conn.cursor()

    print("Restoring state and initializing objects...")

    print("Restoring users...")

    query_user = """
        SELECT a.username, a.password, u.id, u.email, u.fullname
        FROM auth a
        JOIN user u ON a.username = u.username
    """

    cursor.execute(query_user)

    results = cursor.fetchall()

    for row in results:
        user = User(username=row[0], passwd=row[1], email=row[3], fullname=row[4])
        user.id = row[2]
        ScheduleManager().users.append(user)

    print("Restoring schedules...")

    query_schedule = """
        SELECT s.id, s.user_id, s.description, s.protection
        FROM schedule s
    """

    cursor.execute(query_schedule)

    results = cursor.fetchall()

    for row in results:
        schedule = Schedule(description=row[2], protection=row[3], user_id=row)
        schedule.id = row[0]
        ScheduleManager().schedules.append(schedule)

    print("Restoring events...")

    query_event = "SELECT id, schedule_id, start_time, end_time, period, description, event_type, location, protection, assignee FROM event"

    cursor.execute(query_event)

    results = cursor.fetchall()

    for row in results:
        event = Event(
            schedule_id=row[1],
            event_type=row[6],
            start=row[2],
            end=row[3],
            period=row[4],
            description=row[5],
            location=row[7],
            protection=row[8],
            assignee=row[9],
        )
        event.id = row[0]
        ScheduleManager().events.append(event)

    print("Restoring views...")

    query_view = "SELECT user_id, view_id, description FROM users_and_views"
    cursor.execute(query_view)
    results = cursor.fetchall()

    for row in results:
        view = View(description=row[1])
        view.id = row[0]
        ScheduleManager().views.append(view)

    print("Mapping schedules to views...")

    query_views_and_schedules = "SELECT schedule_id, view_id FROM views_and_schedules"
    cursor.execute(query_views_and_schedules)
    results = cursor.fetchall()

    schedules_dict = {schedule.id: schedule for schedule in ScheduleManager().schedules}

    for schedule_id, view_id in results:
        view = next((v for v in ScheduleManager().views if v.id == view_id), None)
        schedule = schedules_dict.get(schedule_id)

        if view and schedule:
            view.schedules[schedule_id] = schedule

    conn.close()

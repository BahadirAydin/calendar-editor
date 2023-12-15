from schedule_manager import ScheduleManager
from user import User
from view import View
from schedule import Schedule
from event import Event
import sqlite3

def retrieve_objects():
    conn = sqlite3.connect('project.sql3')
    cursor = conn.cursor()

    print("Restoring state and initializing objects...")

    print("Restoring users")

    query_user = '''
        SELECT a.username, a.password, u.id, u.email, u.fullname
        FROM auth a
        JOIN user u ON a.username = u.username
    '''

    cursor.execute(query_user)

    results = cursor.fetchall()

    for row in results:
        user = User(username=row[0], passwd=row[1], email=row[3], fullname=row[4])
        user.id = row[2]
        ScheduleManager().users.append(user)

    print("Restoring schedules")

    query_schedule = '''
        SELECT s.id, s.user_id, s.description, s.protection
        FROM schedule s
    '''

    cursor.execute(query_schedule)

    results = cursor.fetchall()

    for row in results:
        schedule = Schedule(description=row[2], protection=row[3], user_id=row)
        schedule.id = row[1]
        ScheduleManager().schedules.append(schedule)

    print("Restoring events")

    query_event = '''
        SELECT s.id, s.user_id, s.description, s.protection
        FROM event e
    '''

    cursor.execute(query_schedule)

    results = cursor.fetchall()

    for row in results:
        schedule = Schedule(description=row[2], protection=row[3], user_id=row)
        schedule.id = row[1]
        ScheduleManager().schedules.append(schedule)

    conn.close()


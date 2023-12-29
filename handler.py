from os import wait
from user import User
from schedule_manager import ScheduleManager
import threading
import re
import json
from colorama import Fore, Style
import sqlite3


def verify_email(email):
    pat = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    return re.match(pat, email)


def verify_username(username):
    if len(username) < 4 or len(username) > 16 or not username[0].isalpha():
        return False
    return True


def verify_password(password):
    if len(password) < 6:
        return False
    return True


def handle_adduser(request):
    response = {"status": "error", "message": "Missing or too many arguments"}

    if len(request) == 4:
        if ScheduleManager().user_exists(request[0]):
            response["status"] = "error"
            response["message"] = "User already exists"
        elif not verify_username(request[0]):
            response["status"] = "error"
            response[
                "message"
            ] = "Username must be 4-16 characters long and start with a letter"
        elif not verify_email(request[1]):
            response["status"] = "error"
            response["message"] = "Invalid email address"
        elif not verify_password(request[3]):
            response["status"] = "error"
            response["message"] = "Password must be at least 6 characters long"
        else:
            username = request[0]
            email = request[1]
            fullname = request[2]
            password = request[3]

            if ScheduleManager().create_user(username, email, fullname, password):
                response["status"] = "success"
                response["message"] = f"User {username} added successfully"
            else:
                response["status"] = "error"
                response["message"] = "Database error"
    return json.dumps(response)


def handle_deleteuser(request):
    response = {"status": "error", "message": "Missing or too many arguments"}

    if len(request) == 2:
        username = request[0]
        password = request[1]

        if User.login(username, password):
            if ScheduleManager().delete_user_by_id(
                ScheduleManager().get_user_id(username)
            ):
                response["status"] = "success"
                response["message"] = f"User {username} deleted successfully"
            else:
                response["status"] = "error"
                response["message"] = "Database error"
        else:
            response["status"] = "error"
            response["message"] = "Invalid username or password"
    else:
        response["status"] = "error"
        response[
            "message"
        ] = "Missing or too much arguments.\n deleteuser requires <username> <password>"

    return json.dumps(response)


def handle_updateevent(request, user_id):
    if len(request) == 10:
        schedule_name = request[0]
        event_description = request[1]
        event_type = request[2]
        start = request[3]
        end = request[4]
        period = request[5]
        description = request[6]
        location = request[7]
        protection = request[8]
        assignee = request[9]

        if not ScheduleManager().schedule_exists(user_id, schedule_name):
            return "Schedule does not exist"

        schid = ScheduleManager().get_schedule_id(user_id, schedule_name)
        if ScheduleManager().update_event(
            schid,
            event_description,
            event_type,
            start,
            end,
            period,
            description,
            location,
            protection,
            assignee,
        ):
            for event in ScheduleManager().events:
                if (
                    event.schedule_id == schid
                    and event.description == event_description
                ):
                    event.event_type = event_type
                    event.start = start
                    event.end = end
                    event.period = period
                    event.description = description
                    event.location = location
                    event.protection = protection
                    event.assignee = assignee
                    event.schedule_id = schid

                    db = sqlite3.connect("project.sql3")
                    c = db.cursor()
                    query = (
                        f"select * from views_and_schedules where schedule_id='{schid}'"
                    )
                    row = c.execute(query)
                    if row.fetchone():
                        return True
                    return False

            return "Event updated successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n updateevent requires <schedule_name> <event_description> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>"


def handle_changepassword(request, user_id):
    response = {}

    if len(request) == 3:
        username = request[0]
        password = request[1]
        new_password = request[2]

        if User.login(username, password):
            if ScheduleManager().update_user(user_id, new_password):
                response["status"] = "success"
                response["message"] = f"User {username} updated successfully"
            else:
                response["status"] = "error"
                response["message"] = "Database error"
        else:
            response["status"] = "error"
            response["message"] = "Invalid username or password"

    return json.dumps(response)


def handle_signin(request):
    response = {"status": "error", "message": "Missing or too many arguments"}

    if len(request) == 2:
        username = request[0]
        password = request[1]

        if User.login(username, password):
            user = [u for u in ScheduleManager().users if u.username == username][0]
            ScheduleManager().save_session(threading.get_ident(), username, user)

            response["status"] = "success"
            response["message"] = f"User {username} signed in successfully"
        else:
            response["status"] = "error"
            response["message"] = "Invalid username or password"

    return json.dumps(response)


def handle_addschedule(request, user_id):
    response = {}

    if len(request) == 2:
        description = request[0]
        protection = request[1]

        if ScheduleManager().create_schedule(description, protection, user_id):
            response["status"] = "success"
            response["message"] = "Schedule added successfully"
        else:
            response["status"] = "error"
            response["message"] = "Database error"
    else:
        response["status"] = "error"
        response[
            "message"
        ] = "Missing or too many arguments.\n addschedule requires <username> <description> <protection>"

    return json.dumps(response)


def handle_addevent(request, userid):
    response = {}

    if len(request) == 9:
        schedule_name = request[0]
        event_type = request[1]
        start = request[2]
        end = request[3]
        period = request[4]
        description = request[5]
        location = request[6]
        protection = request[7]
        assignee = request[8]

        if not ScheduleManager().schedule_exists(userid, schedule_name):
            response["status"] = "error"
            response["message"] = "Schedule does not exist"
        else:
            schid = ScheduleManager().get_schedule_id(userid, schedule_name)

            if ScheduleManager().create_event(
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
                response["status"] = "success"
                response["message"] = "Event added successfully"
            else:
                response["status"] = "error"
                response["message"] = "Database error"

    return json.dumps(response)


def handle_deleteschedule(request, user_id):
    if len(request) == 1:
        description = request[0]

        if not ScheduleManager().schedule_exists(user_id, description):
            return "Schedule does not exist"

        schedule_id = ScheduleManager().get_schedule_id(user_id, description)
        if ScheduleManager().delete_schedule(schedule_id):
            return "Schedule deleted successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n deleteschedule requires <username> <schedule_id>"


def handle_deleteevent(request, user_id):
    if len(request) == 2:
        schedule_name = request[0]
        event_description = request[1]

        if not ScheduleManager().schedule_exists(user_id, schedule_name):
            return "Schedule does not exist"

        schedule_id = ScheduleManager().get_schedule_id(user_id, schedule_name)
        if ScheduleManager().delete_event(schedule_id, event_description):
            return "Event deleted successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n deleteevent requires <schedule_name> <event_description>"


#### PRINT


def handle_printuser(user_id):
    user = ScheduleManager().get_user_by_id(user_id)
    if user is None:
        return "User does not exist"
    output = (
        f"{Fore.YELLOW}User ID:{Style.RESET_ALL} {user['id']}\n"
        f"{Fore.YELLOW}Username:{Style.RESET_ALL} {user['username']}\n"
        f"{Fore.YELLOW}Email:{Style.RESET_ALL} {user['email']}\n"
        f"{Fore.YELLOW}Full Name:{Style.RESET_ALL} {user['fullname']}\n"
    )
    return output


def handle_printschedule(request, user_id):
    response = {}

    if len(request) == 1:
        description = request[0]
        schedule_id = ScheduleManager().get_schedule_by_description(
            user_id, description
        )
        schedule = ScheduleManager().get_schedule_obj(schedule_id)

        if schedule is None:
            response["status"] = "error"
            response["message"] = "Schedule does not exist"
        else:
            response["status"] = "success"
            response["schedule"] = {
                "id": schedule["id"],
                "description": schedule["description"],
                "protection": schedule["protection"],
                "user_id": schedule["user_id"],
                "events": [],
            }

            for event in schedule["events"]:
                response["schedule"]["events"].append(
                    {
                        "event_id": event[0],
                        "schedule_id": event[1],
                        "start_time": event[2],
                        "end_time": event[3],
                        "period": event[4],
                        "description": event[5],
                        "event_type": event[6],
                        "location": event[7],
                        "protection": event[8],
                        "assignee": event[9],
                    }
                )

    return json.dumps(response)


def handle_printallschedules(user_id):
    response = {"status": "error", "message": "Missing or too many arguments"}

    schedules = ScheduleManager().get_all_schedules(user_id)
    print(schedules)
    if schedules is None:
        response["status"] = "error"
        response["message"] = "Schedule does not exist"
    else:
        response["status"] = "success"
        response["schedules"] = []
        for schedule in schedules:
            response["schedules"].append(
                {
                    "id": schedule["id"],
                    "user_id": schedule["user_id"],
                    "description": schedule["description"],
                    "protection": schedule["protection"],
                    "events": [],
                }
            )
            for event in schedule["events"]:
                response["schedules"][-1]["events"].append(
                    {
                        "event_id": event[0],
                        "schedule_id": event[1],
                        "start_time": event[2],
                        "end_time": event[3],
                        "period": event[4],
                        "description": event[5],
                        "event_type": event[6],
                        "location": event[7],
                        "protection": event[8],
                        "assignee": event[9],
                    }
                )
    return json.dumps(response)

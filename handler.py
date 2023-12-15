from user import User
from schedule_manager import ScheduleManager
import threading
import re
import json
from colorama import Fore, Style


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
    if len(request) == 4:
        if ScheduleManager().user_exists(request[0]):
            return "User already exists"
        if not verify_username(request[0]):
            return "Username must be 4-16 characters long and start with a letter"
        username = request[0]
        if not verify_email(request[1]):
            return "Invalid email address"
        email = request[1]
        if not verify_password(request[3]):
            return "Password must be at least 6 characters long"
        fullname = request[2]
        password = request[3]
        if ScheduleManager().create_user(username, email, fullname, password):
            return f"User {username} added successfully"
        else:
            return "Database error"
    else:
        return "Missing or too much arguments.\n adduser requires <username> <email> <fullname> <password>"


def handle_deleteuser(request):
    if len(request) == 2:
        username = request[0]
        password = request[1]
        if User.login(username, password):
            if ScheduleManager().delete_user_by_id(
                ScheduleManager().get_user_id(username)
            ):
                return f"User {username} deleted successfully"
            else:
                return "Database error"
        else:
            return "Invalid username or password"
    else:
        return (
            "Missing or too much arguments.\n deleteuser requires <username> <password>"
        )


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
        if ScheduleManager().update_event(schid, event_description, event_type, start, end, period, description, location, protection, assignee):
            return "Event updated successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n updateevent requires <schedule_name> <event_description> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>"


def handle_changepassword(request, user_id):
    if len(request) == 3:
        username = request[0]
        password = request[1]
        new_password = request[2]
        if User.login(username, password):
            if ScheduleManager().update_user(user_id, new_password):
                return f"User {username} updated successfully"
            else:
                return "Database error"
        else:
            return "Invalid username or password"
    else:
        return "Missing or too much arguments.\n changepassword requires <username> <password> <new_password>"


def handle_signin(request):
    if len(request) == 2:
        username = request[0]
        password = request[1]
        if User.login(username, password):
            # FIXME
            ScheduleManager().save_session(threading.get_ident(), username, None)
            return f"User {username} signed in successfully"
        else:
            return "Invalid username or password"
    else:
        return "Missing or too much arguments.\n signin requires <username> <password>"


def handle_addschedule(request, user_id):
    if len(request) == 2:
        description = request[0]
        protection = request[1]

        if ScheduleManager().create_schedule(description, protection, user_id):
            return "Schedule added successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n addschedule requires <username> <description> <protection>"


def handle_addevent(request, userid):
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
            return "Schedule does not exist"

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
            return "Event added successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n addevent requires <schedule_name> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>"


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
    if len(request) == 1:
        description = request[0]
        schedule_id = ScheduleManager().get_schedule_by_description(
            user_id, description
        )
        schedule = ScheduleManager().get_schedule_obj(schedule_id)
        if schedule is None:
            return "Schedule does not exist"

        output = (
            f"{Fore.YELLOW}Schedule ID:{Style.RESET_ALL} {schedule['id']}\n"
            f"{Fore.YELLOW}Description:{Style.RESET_ALL} {schedule['description']}\n"
            f"{Fore.YELLOW}Protection Level:{Style.RESET_ALL} {schedule['protection_level']}\n"
            f"{Fore.YELLOW}User ID:{Style.RESET_ALL} {schedule['user_id']}\n"
            f"{Fore.YELLOW}Events:{Style.RESET_ALL}\n"
        )

        for event in schedule["events"]:
            output += (
                f"  {Fore.CYAN}Event ID:{Style.RESET_ALL} {event[0]}\n"
                f"    {Fore.CYAN}Schedule ID:{Style.RESET_ALL} {event[1]}\n"
                f"    {Fore.CYAN}Start Time:{Style.RESET_ALL} {event[2]}\n"
                f"    {Fore.CYAN}End Time:{Style.RESET_ALL} {event[3]}\n"
                f"    {Fore.CYAN}Priority:{Style.RESET_ALL} {event[4]}\n"
                f"    {Fore.CYAN}Name:{Style.RESET_ALL} {event[5]}\n"
                f"    {Fore.CYAN}Location:{Style.RESET_ALL} {event[6]}\n"
                f"    {Fore.CYAN}Status:{Style.RESET_ALL} {event[7]}\n"
                f"    {Fore.CYAN}Organizer:{Style.RESET_ALL} {event[8]}\n"
            )

        return output
    else:
        return f"{Fore.RED}Missing or too many arguments.{Style.RESET_ALL}\n printschedule requires <schedule_description>"

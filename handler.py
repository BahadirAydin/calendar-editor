from schedule_manager import ScheduleManager
import re


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
        if ScheduleManager().is_user_exists(request[0]):
            return "User already exists"
        if not verify_username(request[0]):
            return "Username must be 4-16 characters long and start with a letter"
        username = request[0]
        if not verify_email(request[1]):
            return "Invalid email address"
        email = request[1]
        fullname = request[2].replace('"', "")
        if not verify_password(request[3]):
            return "Password must be at least 6 characters long"
        password = request[3]
        if ScheduleManager().create_user(username, email, fullname, password):
            return f"User {username} added successfully"
        else:
            return "Database error"
    else:
        return "Missing or too much arguments.\n adduser requires <username> <email> <fullname> <password>"


def handle_signin(request):
    if len(request) == 2:
        username = request[0]
        password = request[1]
        if ScheduleManager().login(username, password):
            return f"User {username} signed in successfully"
        else:
            return "Invalid username or password"
    else:
        return "Missing or too much arguments.\n signin requires <username> <password>"

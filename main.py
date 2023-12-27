from schedule_manager import ScheduleManager
import argparse
import socket
import threading
from handler import *
from view_handlers import *
import atexit
import shlex
from retrieve_objects import retrieve_objects
from colorama import Fore, Style

schedule_manager = ScheduleManager()

HELP_TEXT = f"""{Fore.GREEN}Valid commands are:{Style.RESET_ALL}
{Fore.CYAN}adduser {Fore.WHITE}<username> <email> <fullname> <password>{Style.RESET_ALL}
{Fore.CYAN}deleteuser {Fore.WHITE}<username> <password>{Style.RESET_ALL}
{Fore.CYAN}signin {Fore.WHITE}<username> <password>{Style.RESET_ALL}
{Fore.CYAN}addschedule {Fore.WHITE}<username> <description> <protection>{Style.RESET_ALL}
{Fore.CYAN}deleteschedule {Fore.WHITE}<username> <schedule_id>{Style.RESET_ALL}
{Fore.CYAN}addevent {Fore.WHITE}<username> <schedule_id> <event_description> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>{Style.RESET_ALL}
{Fore.CYAN}deleteevent {Fore.WHITE}<username> <schedule_id> <event_id>{Style.RESET_ALL}
{Fore.CYAN}changepassword {Fore.WHITE}<username> <password> <new_password>{Style.RESET_ALL}
{Fore.CYAN}updateevent {Fore.WHITE}<username> <schedule_id> <event_description> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>{Style.RESET_ALL}
{Fore.CYAN}createview {Fore.WHITE}<description>{Style.RESET_ALL}
{Fore.CYAN}attachview {Fore.WHITE}<view_name> <description>{Style.RESET_ALL}
{Fore.CYAN}detachview {Fore.WHITE}<view_name> <description>{Style.RESET_ALL}
{Fore.CYAN}addtoview {Fore.WHITE}<view_name> <schedule_name>{Style.RESET_ALL}
{Fore.CYAN}PRINTUSER {Fore.WHITE}<username>{Style.RESET_ALL}
{Fore.CYAN}PRINTSCHEDULE {Fore.WHITE}<username> <schedule_id>{Style.RESET_ALL}
{Fore.CYAN}PRINTVIEW {Fore.WHITE}<view_name>{Style.RESET_ALL}
"""


def handle_client(connection, address):
    try:
        while True:
            request = connection.recv(1024).decode()
            if not request:
                break

            response = process_request(request, threading.get_ident())
            connection.sendall(response.encode())
    finally:
        connection.close()


def process_request(request, thread_id):
    parts = shlex.split(request)
    if len(parts) > 0:
        command = parts[0]
        if command == "adduser":
            return handle_adduser(parts[1:])
        elif command == "signin":
            return handle_signin(parts[1:])

        username = ScheduleManager().get_user_by_thread_id(thread_id)
        id = ScheduleManager().get_user_id(username)

        if not ScheduleManager().is_logged_in(username):
            return "You should authenticate to proceed."

        if command == "addschedule":
            return handle_addschedule(parts[1:], id)
        elif command == "deleteschedule":
            return handle_deleteschedule(parts[1:], id)
        elif command == "deleteuser":
            return handle_deleteuser(parts[1:])
        elif command == "addevent":
            return handle_addevent(parts[1:], id)
        elif command == "deleteevent":
            return handle_deleteevent(parts[1:], id)
        # UPDATE USER
        elif command == "changepassword":
            return handle_changepassword(parts[1:], id)
        elif command == "updateevent":
            return handle_updateevent(parts[1:], id)
        elif command == "createview":
            return handle_createview(parts[1:], id)
        elif command == "attachview":
            return handle_attachview(parts[1:], id)
        elif command == "detachview":
            return handle_detachview(parts[1:], id)
        elif command == "addtoview":
            return handle_addtoview(parts[1:], id)

        elif command == "PRINTUSER":
            return handle_printuser(id)
        elif command == "PRINTSCHEDULE":
            return handle_printschedule(parts[1:], id)
        elif command == "PRINTVIEW":
            return handle_printview(parts[1:], id)

    return HELP_TEXT

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # added to prevent socket already in use error.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen()
    atexit.register(server_socket.close)

    retrieve_objects()

    print(f"Server listening on port {port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server Application")
    parser.add_argument("--port", type=int, required=True, help="TCP port to listen on")
    args = parser.parse_args()

    start_server(args.port)

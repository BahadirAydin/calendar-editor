from schedule_manager import ScheduleManager
import argparse
import socket
import threading
from handler import *
import atexit
import shlex


schedule_manager = ScheduleManager()

VALID_COMMANDS = ["adduser", "signin"]
HELP_TEXT = """Valid commands are:
adduser <username> <email> <fullname> <password>
deleteuser <username> <password>
signin <username> <password>
addschedule <username> <description> <protection>
deleteschedule <username> <schedule_id>
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
        elif command == "changepassword":
            return handle_changepassword(parts[1:], id)
        elif command == "PRINTUSER":
            return handle_printuser(id)
        elif command == "PRINTSCHEDULE":
            return handle_printschedule(parts[1:], id)

    return HELP_TEXT


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # added to prevent socket already in use error.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen()
    atexit.register(server_socket.close)

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

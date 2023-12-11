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

            response = process_request(request)
            connection.sendall(response.encode())
    finally:
        connection.close()


def process_request(request):
    parts = shlex.split(request)
    if len(parts) > 0:
        command = parts[0]
        if command == "adduser":
            return handle_adduser(parts[1:])
        elif command == "signin":
            return handle_signin(parts[1:])
        elif command == "addschedule":
            return handle_addschedule(parts[1:])
        elif command == "deleteschedule":
            return handle_deleteschedule(parts[1:])

    return HELP_TEXT


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

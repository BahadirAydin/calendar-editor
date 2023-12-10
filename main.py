from schedule_manager import ScheduleManager
import argparse
import socket
import threading

schedule_manager = ScheduleManager()

def handle_client(connection, address):
    try:
        while True:
            request = connection.recv(1024).decode()
            print(request)
            if not request:
                break

            response = process_request(request)

            connection.sendall(response.encode())
    finally:
        connection.close()

def process_request(request):
    return "Response to the request"

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen()

    print(f"Server listening on port {port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server Application")
    parser.add_argument('--port', type=int, required=True, help='TCP port to listen on')
    args = parser.parse_args()

    start_server(args.port)

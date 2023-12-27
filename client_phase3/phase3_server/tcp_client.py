import socket

def connect_to_tcp_server(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        # Now you can send and receive data from the server
        # For example, to send a command:
        # client_socket.sendall(b'your_command_here')
        # To receive a response:
        # response = client_socket.recv(1024)
    except Exception as e:
        print(f"Error connecting to TCP server: {e}")
    finally:
        client_socket.close()

import socket
import threading

class TCPConnectionManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(TCPConnectionManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.client_socket = None

    def connect(self, host, port):
        if not self.client_socket:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))

    def send(self, message):
        if self.client_socket:
            self.client_socket.sendall(message.encode())

    def receive(self):
        if self.client_socket:
            return self.client_socket.recv(1024).decode()

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None

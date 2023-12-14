import socket

class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.token = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_request(self, message):
        if not self.socket:
            raise Exception("Connection not established. Call connect() first.")
        
        self.socket.sendall(message.encode())
        response = self.socket.recv(1024)
        return response.decode()

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
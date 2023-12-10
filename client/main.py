from client import TCPClient

def main():
    host = 'localhost' 
    port = 1423  

    client = TCPClient(host, port)
    client.connect()

    try:
        while True:
            message = input("Enter message to send: ")
            if message.lower() == 'exit':
                break

            response = client.send_request(message)
            print("Response:", response)
    finally:
        client.close()

if __name__ == "__main__":
    main()
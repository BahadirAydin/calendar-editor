from client import TCPClient
import argparse


def main(port_no):
    host = "localhost"
    port = port_no

    client = TCPClient(host, port)
    client.connect()

    try:
        while True:
            message = input("Enter message to send: ")
            if message.lower() == "exit":
                break

            response = client.send_request(message)
            print("Response:\n", response)
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server Application")
    parser.add_argument("--port", type=int, required=True, help="TCP port to listen on")
    args = parser.parse_args()
    main(args.port)

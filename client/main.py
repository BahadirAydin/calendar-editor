from client import TCPClient
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def main(port_no):
    host = "localhost"
    port = port_no

    client = TCPClient(host, port)
    client.connect()

    try:
        while True:
            message = input(f"{Fore.CYAN}Enter message to send:{Style.RESET_ALL} ")
            if message.lower() == "exit":
                break

            response = client.send_request(message)
            print(f"{Fore.GREEN}Response: {Style.RESET_ALL}{response}")
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server Application")
    parser.add_argument("--port", type=int, required=True, help="TCP port to listen on")
    args = parser.parse_args()
    main(args.port)

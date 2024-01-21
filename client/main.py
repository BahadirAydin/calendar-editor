from client import WebSocketClient
import argparse
from colorama import Fore, Style, init
import asyncio

# Initialize colorama
init(autoreset=True)

async def main(uri):
    client = WebSocketClient(uri)
    await client.connect()

    try:
        while True:
            message = input(f"{Fore.CYAN}Enter message to send:{Style.RESET_ALL} ")
            if message.lower() == "exit":
                break

            response = await client.send_request(message)
            print(f"{Fore.GREEN}Response: {Style.RESET_ALL}{response}")
    finally:
        await client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket Client Application")
    parser.add_argument("--port", type=int, required=True, help="WebSocket port to connect to")
    args = parser.parse_args()
    uri = f"ws://localhost:{args.port}"
    asyncio.get_event_loop().run_until_complete(main(uri))

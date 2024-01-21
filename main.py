import argparse
import asyncio
import websockets
import shlex
import json
from schedule_manager import ScheduleManager
from handler import *
from view_handlers import *
from token_manager import TokenManager
from retrieve_objects import retrieve_objects
from colorama import Fore, Style

schedule_manager = ScheduleManager()

HELP_TEXT = f"""{Fore.GREEN}Valid commands are:{Style.RESET_ALL}
{Fore.CYAN}adduser {Fore.WHITE}<username> <email> <fullname> <password>{Style.RESET_ALL}
{Fore.CYAN}deleteuser {Fore.WHITE}<username> <password>{Style.RESET_ALL}
{Fore.CYAN}signin {Fore.WHITE}<username> <password>{Style.RESET_ALL}
{Fore.CYAN}addschedule {Fore.WHITE}<username> <description> <protection>{Style.RESET_ALL}
{Fore.CYAN}deleteschedule {Fore.WHITE}<username> <schedule_id>{Style.RESET_ALL}
{Fore.CYAN}addevent {Fore.WHITE}<username> <schedule_id> <event_description> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>{Style.RESET_ALL}
{Fore.CYAN}deleteevent {Fore.WHITE}<username> <schedule_id> <event_id>{Style.RESET_ALL}
{Fore.CYAN}changepassword {Fore.WHITE}<username> <password> <new_password>{Style.RESET_ALL}
{Fore.CYAN}updateevent {Fore.WHITE}<username> <schedule_id> <event_description> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>{Style.RESET_ALL}
{Fore.CYAN}createview {Fore.WHITE}<description>{Style.RESET_ALL}
{Fore.CYAN}attachview {Fore.WHITE}<view_name> <description>{Style.RESET_ALL}
{Fore.CYAN}detachview {Fore.WHITE}<view_name> <description>{Style.RESET_ALL}
{Fore.CYAN}addtoview {Fore.WHITE}<view_name> <schedule_name>{Style.RESET_ALL}
{Fore.CYAN}PRINTUSER {Fore.WHITE}<username>{Style.RESET_ALL}
{Fore.CYAN}PRINTSCHEDULE {Fore.WHITE}<username> <schedule_id>{Style.RESET_ALL}
{Fore.CYAN}PRINTVIEW {Fore.WHITE}<view_name>{Style.RESET_ALL}
"""

async def handle_client(websocket, path):
    address = websocket.remote_address
    print(f"Connection from {address}")

    try:
        async for message in websocket:
            try:
                response = process_request(message)
            except Exception as e:
                response = json.dumps({"status": "error", "message": f"An error occurred: {str(e)}"})
                print(f"Error processing request from {address}: {e}")

            await websocket.send(response)
    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection with {address} closed unexpectedly.")
    except Exception as e:
        print(f"Unexpected error with {address}: {e}")

def process_request(request):
    try:
        parts = shlex.split(request)    
        if len(parts) > 0:
            command = parts[0]
            if command == "adduser":
                return handle_adduser(parts[1:])
            elif command == "signin":
                print(parts)
                return handle_signin(parts[1:])
            
            uname = TokenManager().verify_token(command)
            if uname is None:
                return json.dumps({"status": "error", "message" : "Not a valid authentication token. Please sign in again."})
            
            id = ScheduleManager().get_user_id(uname)

            command = parts[1]
            print(parts[2:])
            if command == "addschedule":
                return handle_addschedule(parts[2:], id)
            elif command == "schedules":
                return handle_printallschedules(id)
            elif command == "views":
                return handle_printallviews(id)
            elif command == "deleteschedule":
                return handle_deleteschedule(parts[2:], id)
            elif command == "deleteuser":
                return handle_deleteuser(parts[2:])
            elif command == "addevent":
                return handle_addevent(parts[2:], id)
            elif command == "deleteevent":
                return handle_deleteevent(parts[2:], id)
            # UPDATE USER
            elif command == "changepassword":
                return handle_changepassword(parts[2:], id)
            elif command == "updateevent":
                return handle_updateevent(parts[2:], id)
            elif command == "createview":
                return handle_createview(parts[2:], id)
            elif command == "attachview":
                return handle_attachview(parts[2:], id)
            elif command == "detachview":
                return handle_detachview(parts[2:], id)
            elif command == "addtoview":
                return handle_addtoview(parts[2:], id)

            elif command == "PRINTUSER":
                return handle_printuser(id)
            elif command == "PRINTSCHEDULE":
                return handle_printschedule(parts[2:], id)
            elif command == "PRINTVIEW":
                return handle_printview(parts[2:], id)

        return HELP_TEXT
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Error processing command: {str(e)}"})

async def start_server(port):
    server = await websockets.serve(handle_client, "", port)
    retrieve_objects()
    print(f"Server listening on port {port}")
    await server.wait_closed()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket Server Application")
    parser.add_argument("--port", type=int, required=True, help="WebSocket port to listen on")
    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(start_server(args.port))
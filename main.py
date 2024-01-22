import argparse
import shlex
import json
from websockets.sync import server
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from schedule_manager import ScheduleManager
from handler import *
from view_handlers import *
from token_manager import TokenManager
from retrieve_objects import retrieve_objects
from colorama import Fore, Style

schedule_manager = ScheduleManager()

HELP_TEXT = f"""Valid commands are:
    adduser <username> <email> <fullname> <password>
    deleteuser <username> <password>
    signin <username> <password>
    addschedule <username> <description> <protection>
    deleteschedule <username> <schedule_id>
    addevent <username> <schedule_id> <event_description> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>
    deleteevent <username> <schedule_id> <event_id>
    changepassword <username> <password> <new_password>
    updateevent <username> <schedule_id> <event_description> <event_type> <start> <end> <period> <description> <location> <protection> <assignee>
    createview <description>
    attachview <view_name> <description>
    detachview <view_name> <description>
    addtoview <view_name> <schedule_name>
    PRINTUSER <username>
    PRINTSCHEDULE <username> <schedule_id>
    PRINTVIEW <view_name>
"""
connected_clients = []
        
def process_request(request, sock):
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
            response = handle_addevent(parts[2:], id)
            schid = ScheduleManager().get_schedule_id(id, parts[2])
            print("schedule id: ", schid)
            message = json.dumps({"type": "NEW", "id" : schid, "command": "REFRESH" })
            broadcast_message(message, sock)
            return response        
        elif command == "deleteevent":
            response = handle_deleteevent(parts[2:], id)
            schid = ScheduleManager().get_schedule_id(id, parts[2])
            print("schedule id delete: ", schid)
            message = json.dumps({"type": "DELETE", "id" : schid, "command": "REFRESH" })
            broadcast_message(message, sock)
            return response 
               
        # UPDATE USER
        elif command == "changepassword":
            return handle_changepassword(parts[2:], id)
        elif command == "updateevent":
            response = handle_updateevent(parts[2:], id)
            schid = ScheduleManager().get_schedule_id(id, parts[2])
            print("schedule id update: ", schid)
            message = json.dumps({"type": "UPDATE", "id" : schid, "command": "REFRESH" })
            broadcast_message(message, sock)
            return response 
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
    return json.dumps({"response": HELP_TEXT})

def broadcast_message(message, sock):
    for client in connected_clients:
        if client != sock:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error sending message to a client: {e}")

def agent(sock):
    connected_clients.append(sock)
    try:
        while True:
            inp = sock.recv()
            response = process_request(inp, sock)
            sock.send(response)
    except ConnectionClosedOK:
        print('Client is terminating')
    except ConnectionClosedError:
        print('Client generated error')
    finally:
        connected_clients.remove(sock)

def start_server(host, port):
    retrieve_objects()
    print(f"Server listening on host {host}, port {port}")
    srv = server.serve(agent, host=host, port=port)
    srv.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket Server Application")
    parser.add_argument("--host", type=str, default="", help="WebSocket host to listen on")
    parser.add_argument("--port", type=int, required=True, help="WebSocket port to listen on")
    args = parser.parse_args()
    start_server(args.host, args.port)
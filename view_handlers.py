from schedule_manager import ScheduleManager
from colorama import Fore, Style
import json


def handle_createview(request, user_id):
    response = {"status": "error", "message": "Missing or too many arguments"}
    if len(request) == 1:
        description = request[0]

        if ScheduleManager().create_view(description, user_id):
            response["status"] = "success"
            response["message"] = "View created successfully"
        else:
            response["status"] = "error"
            response["message"] = "Database error"
    return json.dumps(response)


def handle_attachview(request, user_id):
    response = {"status": "error", "message": "Missing or too many arguments"}
    if len(request) == 1:
        description = request[0]
        if ScheduleManager().is_user_attached(user_id):
            response["status"] = "error"
            response["message"] = "User is already attached to a view"
            return json.dumps(response)

        view_id = ScheduleManager().get_view_id_by_description(description)
        if view_id is None:
            response["status"] = "error"
            response["message"] = "View does not exist"
        if ScheduleManager().attach_view(view_id, user_id):
            response["status"] = "success"
            response["message"] = "View attached successfully"
        else:
            response["status"] = "error"
            response["message"] = "Database error"
    return json.dumps(response)


def handle_detachview(request, user_id):
    response = {"status": "error", "message": "Missing or too many arguments"}
    if len(request) == 1:
        description = request[0]

        view_id = ScheduleManager().get_view_id_by_description(description)
        if view_id is None:
            response["status"] = "error"
            response["message"] = "View does not exist"
        if ScheduleManager().detach_view(view_id, user_id):
            response["status"] = "success"
            response["message"] = "View detached successfully"
        else:
            response["status"] = "error"
            response["message"] = "Database error"
    return json.dumps(response)


def handle_addtoview(request, user_id):
    response = {"status": "error", "message": "Missing or too many arguments"}
    if len(request) == 2:
        view_description = request[0]
        schedule_description = request[1]

        view_id = ScheduleManager().get_view_id_by_description(view_description)
        if view_id is None:
            response["status"] = "error"
            response["message"] = "View does not exist"
        schedule_id = ScheduleManager().get_schedule_id(user_id, schedule_description)
        if schedule_id is None:
            response["status"] = "error"
            response["message"] = "Schedule does not exist or you do not own it."
        if ScheduleManager().is_view_attached(view_id, user_id):
            if ScheduleManager().add_to_view(view_id, schedule_id):
                response["status"] = "success"
                response["message"] = "Schedule added to view successfully"
            else:
                response["status"] = "error"
                response["message"] = "Database error"
        else:
            response["status"] = "error"
            response["message"] = "View is not attached"
    return json.dumps(response)


def handle_printview(request, user_id):
    response = {}

    if len(request) == 1:
        view_description = request[0]
        view_id = ScheduleManager().get_view_id_by_description(view_description)

        if view_id is None:
            response["status"] = "error"
            response["message"] = "View does not exist"
        elif ScheduleManager().is_view_attached(view_id, user_id):
            schedule_ids = ScheduleManager().get_schedules_in_view(view_id)

            for schedule_id in schedule_ids:
                schedule = ScheduleManager().get_schedule_obj(schedule_id[0])
                if schedule is None:
                    response["status"] = "error"
                    response["message"] = "Schedule does not exist"
                    return json.dumps(response)

                output = {
                    "schedule_id": schedule["id"],
                    "user_id": schedule["user_id"],
                    "description": schedule["description"],
                    "protection": schedule["protection"],
                    "events": [],
                }

                for event in schedule["events"]:
                    output["events"].append(
                        {
                            "event_id": event[0],
                            "schedule_id": event[1],
                            "start_time": event[2],
                            "end_time": event[3],
                            "period": event[4],
                            "description": event[5],
                            "event_type": event[6],
                            "location": event[7],
                            "protection": event[8],
                            "assignee": event[9],
                        }
                    )

                response["status"] = "success"
                response["schedule"] = output

            return json.dumps(response)
        else:
            response["status"] = "error"
            response["message"] = "View is not attached."
    else:
        response["status"] = "error"
        response[
            "message"
        ] = "Missing or too many arguments. 'printview' requires <view_description>"

    return json.dumps(response)


def handle_printallviews(user_id):
    response = {"status": "error", "message": "Missing or too many arguments"}

    views = ScheduleManager().get_all_views(user_id)

    if views is None:
        response["status"] = "error"
        response["message"] = "Views do not exist"
    else:
        response["status"] = "success"
        response["views"] = []
        del response["message"]
        for view in views:
            response["views"].append(
                {
                    "id": view["view_id"],
                    "description": view["description"],
                    "attached": ScheduleManager().is_view_attached(
                        view["view_id"], user_id
                    ).__str__(),
                    "schedules": view["schedules"],
                }
            )

    return json.dumps(response)

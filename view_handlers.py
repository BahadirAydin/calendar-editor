from schedule_manager import ScheduleManager


def handle_createview(request):
    if len(request) == 1:
        description = request[0]

        if ScheduleManager().create_view(description):
            return "View created successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n createview requires <description>"


def handle_attachview(request, user_id):
    if len(request) == 1:
        description = request[0]

        if ScheduleManager().attach_view(description, user_id):
            return "View attached successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n attachview requires <view_name> <description>"


def handle_detachview(request, user_id):
    if len(request) == 1:
        description = request[0]

        if ScheduleManager().detach_view(description, user_id):
            return "View detached successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n detachview requires <view_name> <description>"

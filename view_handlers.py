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


def handle_addtoview(request, user_id):
    if len(request) == 2:
        view_description = request[0]
        schedule_description = request[1]

        if ScheduleManager().is_view_attached(view_description, user_id):
            if ScheduleManager().add_to_view(view_description, schedule_description):
                return "Schedule added to view successfully"
            else:
                return "Database error"
        else:
            return "View is not attached."

from schedule_manager import ScheduleManager
from colorama import Fore, Style


def handle_createview(request, user_id):
    if len(request) == 1:
        description = request[0]

        if ScheduleManager().create_view(description, user_id):
            return "View created successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n createview requires <description>"


def handle_attachview(request, user_id):
    if len(request) == 1:
        description = request[0]
        if ScheduleManager().is_user_attached(user_id):
            return "User already attached to a view"

        view_id = ScheduleManager().get_view_id_by_description(description)
        if view_id is None:
            return "View does not exist"
        if ScheduleManager().attach_view(view_id, user_id):
            return "View attached successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n attachview requires <view_name> <description>"


def handle_detachview(request, user_id):
    if len(request) == 1:
        description = request[0]

        view_id = ScheduleManager().get_view_id_by_description(description)
        if view_id is None:
            return "View does not exist"
        if ScheduleManager().detach_view(view_id, user_id):
            return "View detached successfully"
        else:
            return "Database error"
    else:
        return "Missing or too many arguments.\n detachview requires <view_name> <description>"


def handle_addtoview(request, user_id):
    if len(request) == 2:
        view_description = request[0]
        schedule_description = request[1]

        view_id = ScheduleManager().get_view_id_by_description(view_description)
        if view_id is None:
            return "View does not exist"
        schedule_id = ScheduleManager().get_schedule_id(user_id, schedule_description)
        if schedule_id is None:
            return "Schedule does not exist"
        if ScheduleManager().is_view_attached(view_id, user_id):
            if ScheduleManager().add_to_view(view_id, schedule_id):
                return "Schedule added to view successfully"
            else:
                return "Database error"
        else:
            return "View is not attached."


def handle_printview(request, user_id):
    if len(request) == 1:
        view_description = request[0]

        view_id = ScheduleManager().get_view_id_by_description(view_description)
        if view_id is None:
            return "View does not exist"
        if ScheduleManager().is_view_attached(view_id, user_id):
            schedule_ids = ScheduleManager().get_schedules_in_view(view_id)
            print(schedule_ids)
            outer_output = f"{Fore.RED}View ID:{Style.RESET_ALL} {view_id}\n"

            for schedule_id in schedule_ids:
                schedule = ScheduleManager().get_schedule_obj(schedule_id[0])
                if schedule is None:
                    return "Schedule does not exist"

                output = (
                    f"{Fore.RED}Schedule ID:{Style.RESET_ALL} {schedule['id']}\n"
                    f"{Fore.YELLOW}Description:{Style.RESET_ALL} {schedule['description']}\n"
                    f"{Fore.YELLOW}Protection Level:{Style.RESET_ALL} {schedule['protection']}\n"
                    f"{Fore.YELLOW}User ID:{Style.RESET_ALL} {schedule['user_id']}\n"
                    f"{Fore.YELLOW}Events:{Style.RESET_ALL}\n"
                )
                for event in schedule["events"]:
                    output += (
                        f"  {Fore.CYAN}Event ID:{Style.RESET_ALL} {event[0]}\n"
                        f"    {Fore.CYAN}Schedule ID:{Style.RESET_ALL} {event[1]}\n"
                        f"    {Fore.CYAN}Start Time:{Style.RESET_ALL} {event[2]}\n"
                        f"    {Fore.CYAN}End Time:{Style.RESET_ALL} {event[3]}\n"
                        f"    {Fore.CYAN}Priority:{Style.RESET_ALL} {event[4]}\n"
                        f"    {Fore.CYAN}Name:{Style.RESET_ALL} {event[5]}\n"
                        f"    {Fore.CYAN}Location:{Style.RESET_ALL} {event[6]}\n"
                        f"    {Fore.CYAN}Status:{Style.RESET_ALL} {event[7]}\n"
                        f"    {Fore.CYAN}Organizer:{Style.RESET_ALL} {event[8]}\n"
                    )
                outer_output += output

            return outer_output
        else:
            return "View is not attached."
    else:
        return "Missing or too many arguments.\n printview requires <view_description>"

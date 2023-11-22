from event import Event
from schedule import Schedule
from user import User
from view import View

users = []
schedules = []
current_user = None

def create_user():
    username = input("Enter username: ")
    email = input("Enter email: ")
    fullname = input("Enter fullname: ")
    passwd = input("Enter password: ")
    user = User(username, email, fullname, passwd)
    users.append(user)
    print(f"User created with ID: {user.id}")

def switch_user():
    global current_user
    user_id = input("Enter user ID to switch to: ")
    for user in users:
        if user.id == user_id:
            current_user = user
            print(f"Switched to user: {current_user.username}")
            return
    print("User not found.")

def create_event():
    if not current_user:
        print("Please switch to a user first.")
        return
    event_type = input("Enter event type: ")
    start = input("Enter start time: ")
    end = input("Enter end time: ")
    period = input("Enter period: ")
    description = input("Enter description: ")
    location = input("Enter location: ")
    protection = input("Enter protection level: ")
    assignee = input("Enter assignee: ")
    event = Event(event_type, start, end, period, description, location, protection, assignee)
    print(f"Event created with ID: {event.id}")
    return event

def create_schedule():
    if not current_user:
        print("Please switch to a user first.")
        return
    description = input("Enter schedule description: ")
    protection = input("Enter protection level: ")
    schedule = Schedule(description, protection)
    schedules.append(schedule)
    print(f"Schedule created with ID: {schedule.id}")

def add_event_to_schedule():
    schedule_id = input("Enter the schedule ID to add the event to: ")
    schedule = next((s for s in schedules if str(s.id) == str(schedule_id)), None)
    if schedule:
        event = create_event()
        if event:
            schedule.add_event(event)
            print("Event added to the schedule.")
    else:
        print("Schedule not found.")

def list_all_ids():
    print("User IDs:")
    for user in users:
        print(f"- {user.id}")

    print("\nSchedule IDs:")
    for schedule in schedules:
        print(f"- {schedule.id}")

def view_user_schedule():
    if not current_user:
        print("Please switch to a user first.")
        return
    
    schedule_id = input("Enter the schedule ID to view: ")
    schedule = next((s for s in schedules if s.id == schedule_id), None)

    if schedule:
        print(f"\nSchedule: {schedule.description}")
        for event in schedule.events:
            print(f"- Event ID: {event.id}, Type: {event.event_type}, Description: {event.description}")
    else:
        print("Schedule not found.")

def main_menu():
    while True:
        print("\n--- Schedule Manager ---")
        print("1. Create User")
        print("2. Switch User")
        print("3. Create Event")
        print("4. Create Schedule")
        print("5. Add Event to Schedule")
        print("6. View User's Schedule")
        print("7. List All IDs")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            switch_user()
        elif choice == "3":
            create_event()
        elif choice == "4":
            create_schedule()
        elif choice == "5":
            add_event_to_schedule()
        elif choice == "6":
            view_user_schedule()
        elif choice == "7":
            list_all_ids()
        elif choice == "8":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
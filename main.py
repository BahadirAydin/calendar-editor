from event import Event
from schedule import Schedule
from user import User
import uuid

# Temporary storage for demonstration purposes
events = []
users = []
schedules = []

def create_event():
    print("\nCreate Event")
    event_type = input("Enter event type (e.g., MEETING, SEMINAR): ")
    start = input("Enter start time (YYYY-MM-DD-HH:MM): ")
    end = input("Enter end time (YYYY-MM-DD-HH:MM): ")
    period = input("Enter period: ")
    description = input("Enter description: ")
    location = input("Enter location: ")
    protection = input("Enter protection level: ")
    assignee = input("Enter assignee: ")

    event = Event(event_type, start, end, period, description, location, protection, assignee)
    events.append(event)
    print(f"Event created with ID: {event.id}")

def view_event():
    event_id = input("Enter event ID to view: ")
    for event in events:
        if str(event.id).strip() == event_id.strip():
            print(vars(event))
            return
    print("Event not found.")

def update_event():
    event_id = input("Enter event ID to update: ")
    for event in events:
        if str(event.id).strip() == event_id.strip():
            event_type = input("Enter new event type (leave blank to keep current): ")
            start = input("Enter new start time (leave blank to keep current): ")
            end = input("Enter new end time (leave blank to keep current): ")
            description = input("Enter new description (leave blank to keep current): ")
            location = input("Enter new location (leave blank to keep current): ")

            updates = {k: v for k, v in zip(['event_type', 'start', 'end', 'description', 'location'], [event_type, start, end, description, location]) if v}
            event.update(**updates)
            print(f"Event {event_id} updated.")
            return
    print("Event not found.")

def delete_event():
    event_id = input("Enter event ID to delete: ")
    global events
    events = [event for event in events if event.id != event_id]
    print(f"Event {event_id} deleted.")
    
def main_menu():
    while True:
        print("\n--- Calendar/Schedule Editor ---")
        print("1. Create Event")
        print("2. View Event")
        print("3. Update Event")
        print("4. Delete Event")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_event()
        elif choice == "2":
            view_event()
        elif choice == "3":
            update_event()
        elif choice == "4":
            delete_event()
        elif choice == "5":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

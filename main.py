from event import Event
from schedule import Schedule

if __name__ == "__main__":
    # Create an event
    event = Event(
        "FUN",
        "2023-11-12-19:00",
        "2023-11-12-21:00",
        "period?",
        "Description: Fun event",
        "ODTÜ",
        "protected",
        "BahadirAydin:denizcan-yilmaz",
    )
    # Create a schedule
    schedule = Schedule("A good schedule", "not-protected")

    print("Successfully created an event and a schedule")

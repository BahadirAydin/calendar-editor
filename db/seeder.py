import sqlite3
import sys
import random
import string
import hashlib
import uuid
import datetime
from faker import Faker

# Initialize Faker instance
fake = Faker()

# Define possible event types
event_types = ["MEETING", "SEMINAR", "LECTURE", "APPOINTMENT", "OFFICEHOUR", "FUN"]

# Helper functions
def get_random_event_type():
    return random.choice(event_types)

def get_random_protection():
    return random.choice(["PUBLIC", "PRIVATE"])

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def hashed_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def random_datetime():
    year = random.randint(2020, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return datetime.datetime(year, month, day, hour, minute).isoformat()

# Main function for seeding data
def main(num_instances):
    # Connect to SQLite database
    conn = sqlite3.connect("project.sql3")
    cursor = conn.cursor()

    for _ in range(num_instances):
        # Generate user data
        user_id = str(uuid.uuid4())
        fullname = fake.name()
        username = fullname.replace(" ", "_").lower()
        email = username + "@example.com"

        # Insert user data
        cursor.execute("INSERT INTO user (id, username, email, fullname) VALUES (?, ?, ?, ?)",
                       (user_id, username, email, fullname))

        # Insert auth data
        password = hashed_password("password123")
        cursor.execute("INSERT INTO auth (username, password) VALUES (?, ?)",
                       (username, password))

        # Insert session data
        token = str(uuid.uuid4())
        cursor.execute("INSERT INTO sessions (token, username) VALUES (?, ?)",
                       (token, username))

        # Generate schedule data
        schedule_id = str(uuid.uuid4())
        description = fake.sentence(nb_words=6)
        protection = get_random_protection()

        # Insert schedule data
        cursor.execute("INSERT INTO schedule (id, user_id, description, protection) VALUES (?, ?, ?, ?)",
                       (schedule_id, user_id, description, protection))

        # Generate event data
        event_id = str(uuid.uuid4())
        start_time = random_datetime()
        end_time = random_datetime()
        period = "hourly"
        event_description = fake.sentence(nb_words=8)
        event_type = get_random_event_type()
        location = fake.city()

        # Insert event data
        cursor.execute("INSERT INTO event (id, schedule_id, start_time, end_time, period, description, event_type, location, protection, assignee) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (event_id, schedule_id, start_time, end_time, period, event_description, event_type, location, protection, username))

        #Generate view data
        view_id = str(uuid.uuid4())
        view_description = fake.sentence(nb_words=10)

        # Insert view data
        # cursor.execute("INSERT INTO view (id, description) VALUES (?, ?)",
        #                (view_id, view_description))

        # Insert views_and_schedules data
        cursor.execute("INSERT INTO views_and_schedules (schedule_id, view_id) VALUES (?, ?)",
                       (schedule_id, view_id))

        # Insert users_and_views data
        is_attached = random.choice([0, 1])
        cursor.execute("INSERT INTO users_and_views (user_id, view_id, description, is_attached) VALUES (?, ?, ?, ?)",
                       (user_id, view_id, view_description, is_attached))

    # Commit changes and close connection
    conn.commit()
    conn.close()

# Entry point for the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <number_of_instances>")
        sys.exit(1)

    num_instances = int(sys.argv[1])
    main(num_instances)

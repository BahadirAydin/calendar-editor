import sqlite3
import sys
import random
import string
import hashlib
import uuid
import datetime
from faker import Faker
import random

fake = Faker()

event_types = ["MEETING", "SEMINAR", "LECTURE", "APPOINTMENT", "OFFICEHOUR", "FUN"]

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

def main(num_instances):
    conn = sqlite3.connect("project.sql3")
    cursor = conn.cursor()

    for _ in range(num_instances):
        user_id = str(uuid.uuid4())
        fullname = fake.name()
        username = fullname.replace(" ", "_").lower()
        email = username+"@example.com"
        event_type = get_random_event_type()
        cursor.execute("INSERT INTO user (id, username, email, fullname) VALUES (?, ?, ?, ?)",
                       (user_id, username, email, fullname))

        password = hashed_password("password123")
        cursor.execute("INSERT INTO auth (username, password) VALUES (?, ?)",
                       (username, password))

        token = str(uuid.uuid4())
        cursor.execute("INSERT INTO sessions (token, username) VALUES (?, ?)",
                       (token, username))

        schedule_id = str(uuid.uuid4())
        description = fake.sentence(nb_words=6)
        protection = get_random_protection()
        cursor.execute("INSERT INTO schedule (id, user_id, description, protection) VALUES (?, ?, ?, ?)",
                       (schedule_id, user_id, description, protection))

        event_id = str(uuid.uuid4())
        start_time = random_datetime()
        end_time = random_datetime()
        period = "hourly"
        location = fake.city()
        event_description = fake.sentence(nb_words=8)
        cursor.execute("INSERT INTO event (id, schedule_id, start_time, end_time, period, description, event_type, location, protection, assignee) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (event_id, schedule_id, start_time, end_time, period, event_description, event_type, location, protection, username))

        view_id = str(uuid.uuid4())
        view_description = fake.sentence(nb_words=10)
        cursor.execute("INSERT INTO view (id, description) VALUES (?, ?)",
                       (view_id, view_description))

        cursor.execute("INSERT INTO views_and_schedules (id, schedule_id, view_id) VALUES (?, ?, ?)",
                       (str(uuid.uuid4()), schedule_id, view_id))

        cursor.execute("INSERT INTO users_and_views (id, user_id, view_id) VALUES (?, ?, ?)",
                       (str(uuid.uuid4()), user_id, view_id))
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <number_of_instances>")
        sys.exit(1)

    num_instances = int(sys.argv[1])
    main(num_instances)

import unittest
import json
from schedule_manager import ScheduleManager

FULLNAME = "Bahadır Aydın"
USERNAME = "baho"
EMAIL = "baho@example.com"
PASSWORD = "12345"
LOCATION = "Ankara"
DESCRIPTION = "Test..."
PROTECTION = "PUBLIC"
TYPE = "FUN"
START = "09.00"
END = "10.00"
PERIOD = "DAILY"
ASSIGNEE = "deno"


class TestScheduleManager(unittest.TestCase):
    def setUp(self):
        self.schedule_manager = ScheduleManager()

    def test_singleton(self):
        self.assertEqual(id(self.schedule_manager), id(ScheduleManager()))

    def test_create_or_get_user(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        user_json = self.schedule_manager.get_user(user_id)
        expected_user_json = json.dumps(
            {
                "id": str(user_id),
                "username": USERNAME,
                "email": EMAIL,
                "fullname": FULLNAME,
            }
        )
        self.assertEqual(user_json, expected_user_json)

    def test_create_schedule(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        schedule_id = self.schedule_manager.create_schedule(
            user_id, DESCRIPTION, PROTECTION
        )
        schedule_json = self.schedule_manager.get_schedule(schedule_id)
        expected_schedule_json = json.dumps(
            {
                "id": str(schedule_id),
                "description": DESCRIPTION,
                "protection": PROTECTION,
                "events": [],
            }
        )
        self.assertEqual(schedule_json, expected_schedule_json)

    def test_create_view(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        view_id = self.schedule_manager.create_view(user_id, DESCRIPTION)
        view = self.schedule_manager.view_instance(view_id)
        self.assertEqual(view.description, DESCRIPTION)

    def test_create_event(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        schid = self.schedule_manager.create_schedule(user_id, DESCRIPTION, PROTECTION)
        event_id = self.schedule_manager.create_event(
            schid, TYPE, START, END, PERIOD, DESCRIPTION, LOCATION, PROTECTION, ASSIGNEE
        )
        event = self.schedule_manager.event_instance(event_id)
        self.assertEqual(event.event_type, TYPE)
        self.assertEqual(event.start, START)
        self.assertEqual(event.end, END)
        self.assertEqual(event.period, PERIOD)
        self.assertEqual(event.description, DESCRIPTION)
        self.assertEqual(event.location, LOCATION)
        self.assertEqual(event.protection, PROTECTION)
        self.assertEqual(event.assignee, ASSIGNEE)
        schedule_json = self.schedule_manager.get_schedule(schid)
        expected_schedule_json = json.dumps(
            {
                "id": str(schid),
                "description": DESCRIPTION,
                "protection": PROTECTION,
                "events": [event.get()],
            }
        )
        self.assertEqual(schedule_json, expected_schedule_json)

    def test_add_schedule_to_view(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        view_id = self.schedule_manager.create_view(user_id, DESCRIPTION)
        schedule_id = self.schedule_manager.create_schedule(
            user_id, DESCRIPTION, PROTECTION
        )

        self.schedule_manager.add_schedule_to_view(view_id, schedule_id)

        view = self.schedule_manager.view_instance(view_id)
        schedule = self.schedule_manager.schedule_instance(schedule_id)

        expected_structure = {"schedule": schedule, "filters": {}}
        self.assertEqual(view.schedules[schedule_id], expected_structure)

    def test_delete_user(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        user = self.schedule_manager.user_instance(user_id)
        self.schedule_manager.delete_user(user)
        self.assertIsNone(self.schedule_manager.user_instance(user_id))

    def test_delete_schedule(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        schedule_id = self.schedule_manager.create_schedule(
            user_id, DESCRIPTION, PROTECTION
        )
        schedule = self.schedule_manager.schedule_instance(schedule_id)
        self.schedule_manager.delete_schedule(
            self.schedule_manager.user_instance(user_id), schedule_id
        )
        self.assertIsNone(self.schedule_manager.schedule_instance(schedule_id))

    def test_delete_view(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        view_id = self.schedule_manager.create_view(user_id, DESCRIPTION)
        view = self.schedule_manager.view_instance(view_id)
        self.schedule_manager.delete_view(
            self.schedule_manager.user_instance(user_id), view
        )
        self.assertIsNone(self.schedule_manager.view_instance(view_id))

    def test_delete_event(self):
        user_id = self.schedule_manager.create_or_get_user(USERNAME, EMAIL, FULLNAME, PASSWORD)
        schid = self.schedule_manager.create_schedule(user_id, DESCRIPTION, PROTECTION)
        event_id = self.schedule_manager.create_event(
            schid, TYPE, START, END, PERIOD, DESCRIPTION, LOCATION, PROTECTION, ASSIGNEE
        )
        event = self.schedule_manager.event_instance(event_id)
        schedule = self.schedule_manager.schedule_instance(schid)
        self.schedule_manager.delete_event(schedule, event)
        self.assertEqual(len(schedule.events), 0)


if __name__ == "__main__":
    unittest.main()

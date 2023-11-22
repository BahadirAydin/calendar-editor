class View:
    def __init__(self, description):
        self.description = description
        self.schedules = {}  # Stores schedules with their respective filters
        self.current_view = None  # To keep track of the main view for notifications

    def add_schedule(self, schedule_id, schedule):
        self.schedules[schedule_id] = {'schedule': schedule, 'filters': {}}

    def delete_schedule(self, schedule_id):
        if schedule_id in self.schedules:
            del self.schedules[schedule_id]

    def set_filter(self, schedule_id, **kwargs):
        if schedule_id in self.schedules:
            self.schedules[schedule_id]['filters'] = kwargs

    def remove_filters(self, schedule_id):
        if schedule_id in self.schedules:
            self.schedules[schedule_id]['filters'] = {}

    def list_items(self):
        for schedule_id, data in self.schedules.items():
            filters = data['filters']
            for event in data['schedule'].events:
                if self._matches_filters(event, filters):
                    yield event

    def _matches_filters(self, event, filters):
        for key, value in filters.items():
            if not hasattr(event, key) or getattr(event, key) != value:
                return False
        return True

    def attach_view(self, view_id):
        self.current_view = view_id

    def detach_view(self, view_id):
        if self.current_view == view_id:
            self.current_view = None

    @classmethod
    def list_views(cls, user):
        return cls.views.get(user.id, [])

    @classmethod
    def get_view(cls, view_id):
        return cls.views.get(view_id)

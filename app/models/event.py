from flask import current_app
from app import db


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    location = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=True)

    def task_completed(self):
        if self.completed_at:
            return True
        else:
            return False

    def return_task_json(self):
        event_dict = {
            "id": self.event_id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "date": self.date
        }

        return event_dict

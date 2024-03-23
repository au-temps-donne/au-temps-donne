from model.event import Event
from database.db import db
from app import app
from exception.event import EventAccessDbException

class EventRepo():    

    def select_one_by_id(self, event_id: int) -> Event:
        try:
            event = Event.query.filter_by(id=event_id).first()
            return event
        except Exception:
            raise EventAccessDbException(event_id=event_id, method="getting")

    
    def select_all(self) -> list[Event]:
        try:
            events = Event.query.all()
            if not events:
                return None
            return events
        except Exception:
            raise EventAccessDbException(event_id=None, method="getting")


    def insert(self, new_event: Event) -> None:
        try:
            with app.app_context():
                db.session.add(new_event)
                db.session.commit()
                db.session.close()
        except Exception:
            raise EventAccessDbException(event_id=None, method="creating")
    

    def update(self, event_id: int, update_event: Event) -> None:
        try:
            with app.app_context():
                event = Event.query.filter_by(id=event_id).first()
                event.name = update_event.name
                event.datetime = update_event.datetime
                event.description = update_event.description
                event.capacity = update_event.capacity
                event.group = update_event.group
                db.session.commit()
                db.session.close()
        except Exception:
            raise EventAccessDbException(event_id=event_id, method="updating")


    def delete(self, event_id: int) -> None:
        try:
            event = Event.query.filter_by(id=event_id).first()
            with app.app_context():
                db.session.delete(event)
                db.session.commit()
                db.session.close()
        except Exception:
            raise EventAccessDbException(event_id=event_id, method="deleting")
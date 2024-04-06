from database.db import db
import os


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(320), unique=True)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(64))
    status = db.Column(db.Integer)  # 0 = waiting, 1 = valided

    roles = db.relationship(
        'Role', secondary='user_is_role', back_populates='users')
    events = db.relationship(
        'Event', secondary='user_participates_event', back_populates='users')
    tickets = db.relationship(
        'Ticket', secondary='user_writes_ticket', back_populates='users')

    def json(self):
        roles = [role.json_rest() for role in self.roles]

        events = []
        if self.events:
            events = [event.json_rest() for event in self.events]

        return {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'status': self.status,
                'phone': self.phone,
                'roles': roles,
                'events': events}

    def json_rest(self):
        return {'url': f"{os.getenv('API_PATH')}/user/{self.id}",
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email}

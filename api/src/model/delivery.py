from database.db import db
import os


class Delivery(db.Model):
    __tablename__ = "delivery"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime)
    roadmap = db.Column(db.String(200))
    pdf = db.Column(db.String(200))
    status = db.Column(db.Integer)
    packages = db.relationship('Package', backref='delivery')

    vehicle_id = db.Column(db.Integer, db.ForeignKey(
        'vehicle.id'), nullable=False)

    users = db.relationship(
        'User', secondary='user_delivers', back_populates='deliveries')

    locations = db.relationship(
        'Location', secondary='delivers_to_location', back_populates='deliveries')


    def json(self):
        users = [user.json_rest() for user in self.users] if self.users else []
        locations = [location.json_rest()
                     for location in self.locations] if self.locations else []
        return {'id': self.id,
                'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'user': users,
                'vehicle': self.vehicle.json_rest(),
                'roadmap': self.roadmap,
                'pdf': self.pdf,
                'locations': locations,
                'packages': [package.json_rest_delivery() for package in self.packages]}


    def json_rest_user(self):
        locations = [location.json_rest()
                     for location in self.locations] if self.locations else []
        return {'url': f"{os.getenv('API_PATH')}/delivery/{self.id}",
                'id': self.id,
                'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'roadmap': self.roadmap,
                'pdf': self.pdf,
                'vehicle': self.vehicle.json_rest(),
                'locations': locations,
                'packages': [package.json_rest_delivery() for package in self.packages]}


    def json_rest_location(self):
        users = [user.json_rest() for user in self.users] if self.users else []

        return {'url': f"{os.getenv('API_PATH')}/delivery/{self.id}",
                'id': self.id,
                'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'roadmap': self.roadmap,
                'pdf': self.pdf,
                'vehicle': self.vehicle.json_rest(),
                'user': users,
                'packages': [package.json_rest_delivery() for package in self.packages]
                }


    def json_rest_vehicle(self):
        users = [user.json_rest() for user in self.users] if self.users else []
        locations = [location.json_rest()
                     for location in self.locations] if self.locations else []

        return {'url': f"{os.getenv('API_PATH')}/delivery/{self.id}",
                'id': self.id,
                'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'roadmap': self.roadmap,
                'pdf': self.pdf,
                'user': users,
                'locations': locations,
                'packages': [package.json_rest_delivery() for package in self.packages]
                }


    def json_rest_package(self):
        users = [user.json_rest() for user in self.users] if self.users else []
        locations = [location.json_rest()
                     for location in self.locations] if self.locations else []

        return {'url': f"{os.getenv('API_PATH')}/delivery/{self.id}",
                'id': self.id,
                'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                'roadmap': self.roadmap,
                'pdf': self.pdf,
                'vehicle': self.vehicle.json_rest(),
                'user': users,
                'locations': locations,
                }
    

delivers_to_location = db.Table('delivers_to_location', db.metadata,
                                db.Column('location_id', db.Integer, db.ForeignKey(
                                    'location.id'), primary_key=True),
                                db.Column('delivery_id', db.Integer, db.ForeignKey(
                                    'delivery.id'), primary_key=True)
                                )

user_delivers = db.Table('user_delivers', db.metadata,
                         db.Column('user_id', db.Integer, db.ForeignKey(
                             'user.id'), primary_key=True),
                         db.Column('delivery_id', db.Integer, db.ForeignKey(
                             'delivery.id'), primary_key=True)
                         )

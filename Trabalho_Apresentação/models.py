from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Medicos(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Kit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kit_id = db.Column(db.Integer, db.ForeignKey('kit.id'), nullable=False)
    data = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)  # 'ON' ou 'OFF'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Event {self.event_type} at {self.timestamp}>'
    
class MQTTMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<MQTTMessage {self.topic} {self.message} at {self.timestamp}>'
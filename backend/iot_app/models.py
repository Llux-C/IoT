from sqlalchemy import Integer

from backend.iot_app import db
from sqlalchemy.dialects.mysql import INTEGER

UnsignedInt = Integer()
UnsignedInt = UnsignedInt.with_variant(INTEGER(unsigned=True), 'mysql')


class User(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)


class Device(db.Model):
    __tablename__ = 'device_info'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code = db.Column(db.String(128), default='', nullable=False)
    name = db.Column(db.String(128), default='', nullable=False)
    description = db.Column(db.UnicodeText)
    create_time = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(128), default='', nullable=False)


class Message(db.Model):
    __tablename__ = 'device_message'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    alert = db.Column(db.Integer, default=0, nullable=False)
    clientId = db.Column(db.String(128), default='', nullable=False)
    info = db.Column(db.String(128), default='', nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Integer, default=0, nullable=False)

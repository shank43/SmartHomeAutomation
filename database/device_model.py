from database.db import db

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="OFF")
    room_id = db.Column(
    db.Integer,
    db.ForeignKey('room.id'),
    nullable=False
)
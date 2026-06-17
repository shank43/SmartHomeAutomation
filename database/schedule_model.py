from database.db import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(db.String(10), nullable=False)

    schedule_time = db.Column(db.String(20), nullable=False)

    device_id = db.Column(
        db.Integer,
        db.ForeignKey("device.id"),
        nullable=False
    )
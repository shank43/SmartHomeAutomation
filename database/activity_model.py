from datetime import datetime
from database.db import db


class Activity(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    device_id = db.Column(
        db.Integer,
        db.ForeignKey("device.id"),
        nullable=False
    )

    action = db.Column(
        db.String(10),
        nullable=False
    )

    source = db.Column(
        db.String(20),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


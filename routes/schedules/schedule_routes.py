from flask import Blueprint, render_template, request
from database.device_model import Device
from database.schedule_model import Schedule
from database.db import db

schedules = Blueprint("schedules", __name__)

@schedules.route("/schedules", methods=["GET", "POST"])
def view_schedules():

    if request.method == "POST":

        device_id = request.form["device_id"]
        action = request.form["action"]
        schedule_time = request.form["schedule_time"]

        new_schedule = Schedule(
            device_id=device_id,
            action=action,
            schedule_time=schedule_time
        )

        db.session.add(new_schedule)
        db.session.commit()

    all_devices = Device.query.all()
    all_schedules = Schedule.query.all()

    return render_template(
            "schedules.html",
            devices=all_devices,
            schedules=all_schedules
        )
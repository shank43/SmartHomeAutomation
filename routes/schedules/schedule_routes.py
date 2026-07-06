from flask import Blueprint, render_template, request, redirect, url_for, flash

from database.device_model import Device
from database.schedule_model import Schedule
from database.db import db

schedules = Blueprint("schedules", __name__)


# ==========================================
# View & Add Schedule
# ==========================================

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

        flash("✅ Schedule Added Successfully", "success")

        return redirect(url_for("schedules.view_schedules"))

    all_devices = Device.query.all()

    all_schedules = Schedule.query.all()

    return render_template(
        "schedules.html",
        devices=all_devices,
        schedules=all_schedules
    )


# ==========================================
# Edit Schedule
# ==========================================

@schedules.route("/edit_schedule/<int:id>", methods=["GET", "POST"])
def edit_schedule(id):

    schedule = Schedule.query.get_or_404(id)

    if request.method == "POST":

        schedule.device_id = request.form["device_id"]
        schedule.action = request.form["action"]
        schedule.schedule_time = request.form["schedule_time"]

        db.session.commit()

        flash("✏️ Schedule Updated Successfully", "success")

        return redirect(url_for("schedules.view_schedules"))

    all_devices = Device.query.all()

    return render_template(
        "edit_schedule.html",
        schedule=schedule,
        devices=all_devices
    )


# ==========================================
# Delete Schedule
# ==========================================

@schedules.route("/delete_schedule/<int:id>")
def delete_schedule(id):

    schedule = Schedule.query.get_or_404(id)

    db.session.delete(schedule)
    db.session.commit()

    flash("🗑️ Schedule Deleted Successfully", "danger")

    return redirect(url_for("schedules.view_schedules"))
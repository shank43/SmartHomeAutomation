from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_

from database.device_model import Device
from database.db import db
from database.room_model import Room
from database.activity_model import Activity

devices = Blueprint("devices", __name__)


@devices.route("/devices", methods=["GET", "POST"])
def view_devices():

    if request.method == "POST":

        device_name = request.form["device_name"]
        device_type = request.form["device_type"]
        room_id = request.form["room_id"]

        new_device = Device(
            device_name=device_name,
            device_type=device_type,
            room_id=room_id
        )

        db.session.add(new_device)
        db.session.commit()

        flash("✅ Device Added Successfully", "success")

        return redirect(url_for("devices.view_devices"))

    search = request.args.get("search", "")
    room_filter = request.args.get("room", "")

    query = Device.query

    if search:

        query = query.filter(
            Device.device_name.ilike(f"%{search}%")
        )

    if room_filter:

        query = query.filter(
            Device.room_id == room_filter
        )

    all_devices = query.all()
    all_rooms = Room.query.all()

    return render_template(
        "devices.html",
        devices=all_devices,
        rooms=all_rooms,
        search=search,
        room_filter=room_filter
    )


# ====================================
# Edit Device
# ====================================

@devices.route("/edit_device/<int:id>", methods=["GET", "POST"])
def edit_device(id):

    device = Device.query.get_or_404(id)

    if request.method == "POST":

        device.device_name = request.form["device_name"]
        device.device_type = request.form["device_type"]
        device.room_id = request.form["room_id"]

        db.session.commit()

        flash("✏️ Device Updated Successfully", "success")

        return redirect(url_for("devices.view_devices"))

    rooms = Room.query.all()

    return render_template(
        "edit_device.html",
        device=device,
        rooms=rooms
    )


# ====================================
# Toggle Device
# ====================================

@devices.route("/toggle_device/<int:id>")
def toggle_device(id):

    device = Device.query.get_or_404(id)

    if device.status == "ON":

        device.status = "OFF"
        action = "OFF"

        flash("🔴 Device Turned OFF", "warning")

    else:

        device.status = "ON"
        action = "ON"

        flash("🟢 Device Turned ON", "success")

    activity = Activity(
        device_id=device.id,
        action=action,
        source="Manual"
    )

    db.session.add(activity)
    db.session.commit()

    return redirect(url_for("devices.view_devices"))


# ====================================
# Delete Device
# ====================================

@devices.route("/delete_device/<int:id>")
def delete_device(id):

    device = Device.query.get_or_404(id)

    db.session.delete(device)
    db.session.commit()

    flash("🗑️ Device Deleted Successfully", "danger")

    return redirect(url_for("devices.view_devices"))
from flask import Blueprint, render_template, request, redirect, url_for
from database.device_model import Device
from database.db import db
from database.room_model import Room

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

        return "Device Added Successfully"

    all_devices = Device.query.all()

    all_devices = Device.query.all()
    all_rooms = Room.query.all()

    return render_template(
    "devices.html",
    devices=all_devices,
    rooms=all_rooms
)

@devices.route("/toggle_device/<int:id>")
def toggle_device(id):

    device = Device.query.get(id)

    if device.status == "OFF":
        device.status = "ON"
    else:
        device.status = "OFF"

    db.session.commit()

    return redirect(url_for("devices.view_devices"))
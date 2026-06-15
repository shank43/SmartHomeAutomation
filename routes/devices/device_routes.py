from flask import Blueprint, render_template, request
from database.device_model import Device
from database.db import db

devices = Blueprint("devices", __name__)

@devices.route("/devices", methods=["GET", "POST"])
def view_devices():

    if request.method == "POST":

        device_name = request.form["device_name"]
        device_type = request.form["device_type"]

        new_device = Device(
            device_name=device_name,
            device_type=device_type
        )

        db.session.add(new_device)
        db.session.commit()

        return "Device Added Successfully"

    all_devices = Device.query.all()

    return render_template(
    "devices.html",
    devices=all_devices
)
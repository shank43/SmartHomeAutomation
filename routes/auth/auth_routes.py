from flask import Blueprint, render_template, request, redirect, url_for
from database.models import User
from database.db import db
from flask import Blueprint, render_template
from database.room_model import Room
from database.device_model import Device

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:
            return redirect(url_for("auth.dashboard"))

        return "Invalid Username or Password"

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return "User Registered Successfully"

    return render_template("register.html")


@auth.route("/dashboard")
def dashboard():

    total_rooms = Room.query.count()

    total_devices = Device.query.count()

    devices_on = Device.query.filter_by(status="ON").count()

    devices_off = Device.query.filter_by(status="OFF").count()

    return render_template(
        "dashboard.html",
        total_rooms=total_rooms,
        total_devices=total_devices,
        devices_on=devices_on,
        devices_off=devices_off
    )
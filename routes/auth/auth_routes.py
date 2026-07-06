from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from database.models import User
from database.db import db
from database.room_model import Room
from database.device_model import Device
from database.activity_model import Activity
from database.schedule_model import Schedule

auth = Blueprint("auth", __name__)


# ===========================
# LOGIN
# ===========================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["username"] = user.username

            flash("✅ Login Successful!", "success")

            return redirect(url_for("auth.dashboard"))

        flash("❌ Invalid Username or Password", "danger")

        return redirect(url_for("auth.login"))

    return render_template("login.html")


# ===========================
# LOGOUT
# ===========================

@auth.route("/logout")
def logout():

    session.clear()

    flash("👋 Logged Out Successfully", "info")

    return redirect(url_for("auth.login"))


# ===========================
# REGISTER
# ===========================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing = User.query.filter_by(username=username).first()

        if existing:

            flash("⚠ Username already exists.", "warning")

            return redirect(url_for("auth.register"))

        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        flash("🎉 Registration Successful!", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ===========================
# DASHBOARD
# ===========================

@auth.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        flash("Please login first.", "warning")

        return redirect(url_for("auth.login"))

    total_rooms = Room.query.count()
    total_devices = Device.query.count()

    devices_on = Device.query.filter_by(status="ON").count()
    devices_off = Device.query.filter_by(status="OFF").count()

    total_schedules = Schedule.query.count()

    total_activity = Activity.query.count()

    rooms = Room.query.all()

    room_names = []
    device_counts = []

    for room in rooms:

        room_names.append(room.room_name)
        device_counts.append(len(room.devices))

    recent_activity = Activity.query.order_by(
        Activity.timestamp.desc()
    ).limit(5).all()

    # Most Active Device

    most_active_device = (
        db.session.query(
            Device.device_name,
            db.func.count(Activity.id).label("count")
        )
        .select_from(Device)
        .join(Activity, Activity.device_id == Device.id)
        .group_by(Device.id)
        .order_by(db.desc("count"))
        .first()
    )

    # Most Active Room

    most_active_room = (
        db.session.query(
            Room.room_name,
            db.func.count(Activity.id).label("count")
        )
        .select_from(Room)
        .join(Device, Device.room_id == Room.id)
        .join(Activity, Activity.device_id == Device.id)
        .group_by(Room.id)
        .order_by(db.desc("count"))
        .first()
    )

    return render_template(

        "dashboard.html",

        username=session["username"],

        total_rooms=total_rooms,
        total_devices=total_devices,
        devices_on=devices_on,
        devices_off=devices_off,

        total_schedules=total_schedules,
        total_activity=total_activity,

        room_names=room_names,
        device_counts=device_counts,

        recent_activity=recent_activity,

        most_active_device=most_active_device,
        most_active_room=most_active_room

    )


# ===========================
# PROFILE
# ===========================

@auth.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:

        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":

        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if not check_password_hash(user.password, old_password):

            flash("Current Password is incorrect.", "danger")

            return redirect(url_for("auth.profile"))

        if new_password != confirm_password:

            flash("Passwords do not match.", "danger")

            return redirect(url_for("auth.profile"))

        user.password = generate_password_hash(new_password)

        db.session.commit()

        flash("Password Changed Successfully.", "success")

        return redirect(url_for("auth.profile"))

    return render_template(
        "profile.html",
        username=user.username
    )
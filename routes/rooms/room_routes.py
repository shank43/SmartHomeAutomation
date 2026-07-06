from flask import Blueprint, render_template, request, redirect, url_for, flash

from database.room_model import Room
from database.db import db

rooms = Blueprint("rooms", __name__)


@rooms.route("/rooms", methods=["GET", "POST"])
def view_rooms():

    if request.method == "POST":

        room_name = request.form["room_name"]

        new_room = Room(room_name=room_name)

        db.session.add(new_room)
        db.session.commit()

        flash("✅ Room Added Successfully", "success")

        return redirect(url_for("rooms.view_rooms"))

    all_rooms = Room.query.all()

    return render_template(
        "rooms.html",
        rooms=all_rooms
    )


@rooms.route("/edit_room/<int:id>", methods=["GET", "POST"])
def edit_room(id):

    room = Room.query.get_or_404(id)

    if request.method == "POST":

        room.room_name = request.form["room_name"]

        db.session.commit()

        flash("✏️ Room Updated Successfully", "success")

        return redirect(url_for("rooms.view_rooms"))

    return render_template(
        "edit_room.html",
        room=room
    )


@rooms.route("/delete_room/<int:id>")
def delete_room(id):

    room = Room.query.get_or_404(id)

    db.session.delete(room)
    db.session.commit()

    flash("🗑️ Room Deleted Successfully", "danger")

    return redirect(url_for("rooms.view_rooms"))
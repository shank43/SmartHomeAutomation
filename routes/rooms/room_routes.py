from flask import Blueprint, render_template, request
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

        return "Room Added Successfully"

    all_rooms = Room.query.all()

    return render_template(
    "rooms.html",
    rooms=all_rooms
)
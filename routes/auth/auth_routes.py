from flask import Blueprint, render_template, request, redirect, url_for
from database.models import User
from database.db import db
from flask import Blueprint, render_template

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
    return render_template("dashboard.html")
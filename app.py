from flask import Flask
from flask_mail import Mail

from config.config import Config
from flask import redirect, url_for

from database.db import db
from database.models import User
from database.room_model import Room
from database.device_model import Device
from database.schedule_model import Schedule
from database.activity_model import Activity

from routes.auth.auth_routes import auth
from routes.rooms.room_routes import rooms
from routes.devices.device_routes import devices
from routes.schedules.schedule_routes import schedules
from routes.activity_routes import activity

from scheduler import scheduler
from services.scheduler_service import run_schedules

app = Flask(__name__)

app.secret_key = "smarthomeautomation123"

app.config.from_object(Config)

db.init_app(app)

# -----------------------------
# Initialize Flask Mail
# -----------------------------
mail = Mail(app)

app.register_blueprint(auth)
app.register_blueprint(rooms)
app.register_blueprint(devices)
app.register_blueprint(schedules)
app.register_blueprint(activity)

@app.route("/")
def home():
    return redirect(url_for("auth.login"))

with app.app_context():
    db.create_all()


def scheduled_job():
    with app.app_context():
        run_schedules()


scheduler.add_job(
    scheduled_job,
    trigger="interval",
    minutes=1,
    id="device_scheduler",
    replace_existing=True
)


if not scheduler.running:
    scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
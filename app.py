from flask import Flask
from config.config import Config
from database.db import db
from database.models import User
from routes.auth.auth_routes import auth
from database.room_model import Room
from database.device_model import Device
from routes.rooms.room_routes import rooms
from routes.devices.device_routes import devices
from database.schedule_model import Schedule
from routes.schedules.schedule_routes import schedules
from scheduler import scheduler, run_schedules


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(rooms)
app.register_blueprint(devices)
app.register_blueprint(schedules)

@app.route("/")
def home():
    return "Smart Home Automation System"

with app.app_context():
    db.create_all()
    
    

def scheduled_job():

    with app.app_context():

        run_schedules()
        
scheduler.add_job(
    scheduled_job,
    "interval",
    minutes=1
)     
     
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
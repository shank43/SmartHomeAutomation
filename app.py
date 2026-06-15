from flask import Flask
from config.config import Config
from database.db import db
from database.models import User
from routes.auth.auth_routes import auth
from database.room_model import Room
from database.device_model import Device
from routes.rooms.room_routes import rooms



app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(rooms)

@app.route("/")
def home():
    return "Smart Home Automation System"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
from datetime import datetime

from database.schedule_model import Schedule
from database.device_model import Device
from database.db import db
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app

def run_schedules():
    
   

        current_time = datetime.now().strftime("%H:%M")

        schedules = Schedule.query.all()

        for schedule in schedules:

            if schedule.schedule_time == current_time:

                device = Device.query.get(schedule.device_id)

                if device:

                    device.status = schedule.action

        db.session.commit()
    
scheduler = BackgroundScheduler()


from datetime import datetime

from database.activity_model import Activity
from database.schedule_model import Schedule
from database.device_model import Device
from database.db import db


def run_schedules():

    current_time = datetime.now().strftime("%H:%M")

    print(f"Checking schedules at {current_time}")

    schedules = Schedule.query.all()

    for schedule in schedules:

        print(
            f"Schedule: {schedule.device_id} | "
            f"{schedule.action} | "
            f"{schedule.schedule_time}"
        )

        if schedule.schedule_time == current_time:

            print("MATCH FOUND")

            device = Device.query.get(schedule.device_id)

            if device:

                print(f"Updating {device.device_name}")

                device.status = schedule.action

                activity = Activity(
                    device_id=device.id,
                    action=schedule.action,
                    source="Scheduler"
                )

                db.session.add(activity)
    db.session.commit()
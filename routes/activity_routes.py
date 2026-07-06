from flask import Blueprint, render_template, send_file
from database.activity_model import Activity

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

activity = Blueprint("activity", __name__)


@activity.route("/activity")
def view_activity():

    activities = Activity.query.order_by(
        Activity.timestamp.desc()
    ).all()

    return render_template(
        "activity.html",
        activities=activities
    )


@activity.route("/activity/pdf")
def export_pdf():

    activities = Activity.query.order_by(
        Activity.timestamp.desc()
    ).all()

    filename = "activity_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>Smart Home Automation System</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Activity Report",
            styles["Heading2"]
        )
    )

    data = []

    data.append([
        "Device",
        "Action",
        "Source",
        "Date & Time"
    ])

    for activity in activities:

        data.append([

            activity.device.device_name,

            activity.action,

            activity.source,

            activity.timestamp.strftime(
                "%d-%m-%Y %I:%M %p"
            )

        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),10),

    ]))

    elements.append(table)

    doc.build(elements)

    return send_file(
        filename,
        as_attachment=True
    )
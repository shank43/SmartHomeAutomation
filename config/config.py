import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "smarthomeautomation123"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:8165#Sunny@localhost/smart_home"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USE_SSL = False

    MAIL_USERNAME = ""

    MAIL_PASSWORD = ""

    MAIL_DEFAULT_SENDER = ""
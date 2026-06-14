class Config:
    SECRET_KEY = "smart_home_secret_key"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:8165#Sunny@localhost/smart_home"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
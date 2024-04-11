import os

class DatabaseConfig:
    def __init__(self, app):
        # Path for our local SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")
        # To specify to track modifications of objects and emit signals
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

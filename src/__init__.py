
from flask import Flask, request 
import os
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# for password hashing
from flask_bcrypt import Bcrypt

from pymongo import MongoClient

# Set up MongoDB connection and collection 
client = MongoClient('mongodb://127.0.0.1:27017/') 
  
# Create database named demo if they don't exist already 
db = client['demo'] 

# Create collection named data if it doesn't exist already 
collection = db['data'] 

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)

# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# load the secret key defined in the .env file
app.secret_key = os.environ.get("SECRET_KEY")
bcrypt = Bcrypt(app)

# Path for our local sql lite database
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")

# To specify to track modifications of objects and emit signals
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# sql alchemy instance
#db = SQLAlchemy(app)


# Flask Migrate instance to handle migrations
#migrate = Migrate(app, db)

# import api blueprint to register it with app
from src.routes import api
app.register_blueprint(api, url_prefix="/api")

# import models to let the migrate tool know
from src.models.user_model import User



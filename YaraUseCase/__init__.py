"""
__init__ file
Created By: Jettin Joy
Created On: 06/13/2021
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from YaraUseCase.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
from YaraUseCase import routes, models

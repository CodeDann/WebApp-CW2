from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_admin import Admin
import logging


app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)
app.config.from_pyfile('config.py')
# app.config.from_object('config')
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap3')
# remove any unwanted handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


migrate = Migrate(app, db)

from app import views, models

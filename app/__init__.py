from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_admin import Admin


app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap3')


migrate = Migrate(app, db)

from app import views, models

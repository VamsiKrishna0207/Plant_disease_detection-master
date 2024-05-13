from keras.src.utils.generic_utils import default
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class History(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_email = db.Column(db.String(150))
    pre_date = db.Column(db.DateTime(timezone=True),default=func.now())
    img = db.Column(db.Text, unique=True, nullable=False)
    prediction = db.Column(db.String(150))
    mimetype = db.Column(db.Text, nullable=False)


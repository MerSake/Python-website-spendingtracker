import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(400))
    first_name = db.Column(db.String(50))
    notes = db.relationship('Note')

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.date.today())
    groceriesEx = db.Column(db.Integer, default=0)
    ordersEx = db.Column(db.Integer, default=0)
    HomeEx = db.Column(db.Integer, default=0)
    restaurantEx = db.Column(db.Integer, default=0)
    otherExpensesEx = db.Column(db.Integer, default=0)
    notes = db.Column(db.String(500))
    
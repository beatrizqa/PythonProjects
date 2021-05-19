# from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@35.234.144.82/miniblocksexhibitions"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

db = SQLAlchemy(app)


class Exhibitions(db.Model):
    exhibitionsID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    descriptions = db.Column(db.String(150), nullable=True)
    exhDuration = db.Column(db.Integer, nullable=True)
    exhLocation = db.Column(db.String(20), nullable=True)
    exhDate = db.Column(db.Date, nullable=True)
    itexh = db.relationship('Items', backref='builds')


class Items(db.Model):
    itemsID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    ageLevel = db.Column(db.Integer, nullable=True)
    difficultyLevel = db.Column(db.Integer, nullable=True)
    numberOfPieces = db.Column(db.Integer, nullable=True)
    dateBuilt = db.Column(db.DateTime(), nullable=True)
    photo = db.Column(db.String(100), unique=True, nullable=True)
    comments = db.Column(db.String(150), nullable=True)
    complete = db.Column(db.Boolean, default=False)
    exhid = db.Column(db.Integer, db.ForeignKey(
        'exhibitions.exhibitionsID'), nullable=False)


db.create_all()
newExhibition = Exhibitions(
    name="Buildings & Wonders",
    descriptions="Some skylines & wonders of the world",
    exhDuration=14,
    exhLocation="London",
    exhDate="2021-05-25"
)

newItem = Items(
    name="Big Ben",
    ageLevel=14,
    difficultyLevel=4,
    numberOfPieces=3600,
    dateBuilt="2019-01-1",
    photo=True,
    comments="My first building!",
    exhid=1
)


@ app.route('/')
def home():
    items = Items.query.first()
    return newItem.name


@ app.route('/add')
def add():
    return "Add a new item"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

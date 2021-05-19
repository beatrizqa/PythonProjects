# we need the db objects because we are using the db.drop_all() & db.create_all()
from app import db

db.drop_all()
db.create_all()

import pymongo, hashlib
from pymongo import MongoClient
client = MongoClient()

db = client.database

users = db.users
guides = db.guides
classes = db.classes

users.drop()
guides.drop()
classes.drop()

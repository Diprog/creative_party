from db import db


def save(updates):
    db.updates.drop()
    db.updates.insert_many(updates)
from db import db


def add(user_id):
    document = {
        '_id': user_id,
        'joined': [],
        'left': []
    }
    db.users.insert(document)

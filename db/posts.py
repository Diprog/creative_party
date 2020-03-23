from db import db


def drop():
    db.posts.drop()


def save(posts):
    db.posts.insert_many(posts)


def get():
    return list(db.posts.find({}))

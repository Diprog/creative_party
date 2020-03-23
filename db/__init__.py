from pymongo import MongoClient

import constants.db

client = MongoClient(port=constants.db.PORT)
db = client[constants.db.NAME]
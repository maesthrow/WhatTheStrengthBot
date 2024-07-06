import logging
import os

from pymongo import MongoClient

mongo_username = os.getenv("MONGO_ROOT_USERNAME")
mongo_password = os.getenv("MONGO_ROOT_PASSWORD")

# amvera
uri = f"mongodb://{mongo_username}:{mongo_password}@amvera-maesthrow-run-hk-mongo-db:27017"

# local:
# uri = "mongodb://localhost:27017"

client = MongoClient(uri)


try:
    client.admin.command('ping')
    logging.info("Pinged database. You successfully connected to MongoDB!")
except Exception as e:
    logging.error(e)

db = client["whats_the_strength"]


async def close_mongo_client():
    try:
        client.close()
    except Exception as e:
        logging.error(e)

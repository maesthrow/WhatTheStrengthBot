import logging

from pymongo import MongoClient

# local:
uri = "mongodb://localhost:27017"

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

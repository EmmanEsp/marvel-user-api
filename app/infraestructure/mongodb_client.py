import ssl

import pymongo

from app.settings.mongodb_settings import get_mongodb_settings


def get_client():
    mongodb_settings = get_mongodb_settings()
    return pymongo.MongoClient(
        mongodb_settings.mongodb_url,
        serverSelectionTimeoutMS=5000,
        ssl_cert_reqs=ssl.CERT_NONE,
    )

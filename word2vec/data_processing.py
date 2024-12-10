import os
import string

import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = pymongo.MongoClient(MONGO_URL)

db = client["wikipedia"]
collection = db["wikipedia_tr"]


def fetch_and_clean_data():
    corpus_cleaned = []

    for document in collection.find({}, {"text": 1}):
        text = document.get("text", "")

        text = text.translate(str.maketrans("", "", string.punctuation)).lower()

        tokens = text.split()
        corpus_cleaned.append(tokens)

    return corpus_cleaned

import os

from dotenv import load_dotenv
from pymongo import MongoClient
from xml_processor import extract_articles_from_dump

load_dotenv()


def connect_mongo():
    MONGO_URL = os.getenv("MONGO_URL")
    try:
        client = MongoClient(MONGO_URL)
        db = client["wikipedia"]
        print("Connected to MongoDB.")
        return client, db
    except Exception as e:
        print(f"Error: Could not connect to MongoDB! {e}")
        raise


def save_to_mongodb(db, file_path):
    collection = db["wikipedia_tr"]
    collection.create_index("title", unique=True)

    for bulk_operations in extract_articles_from_dump(file_path):
        try:
            collection.bulk_write(bulk_operations)
            print(f"{len(bulk_operations)} makale kaydedildi.")
        except Exception as e:
            print(f"Hata oluştu: {e}")

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# MongoDB bağlantı bilgileri
DATABASE_URL = os.getenv("DATABASE_URL").replace(
    "<db_password>", os.getenv("DATABASE_PASSWORD")
)

# MongoDB'ye bağlan
try:
    client = MongoClient(DATABASE_URL)
    db = client["wikipedia"]
    collection = db["wikipedia_tr"]
    print("Connected to MongoDB.")
except Exception as e:
    print(f"Error: Could not connect to MongoDB! {e}")


def insert_document(documents):
    """MongoDB'ye belge ekler. Aynı başlıkta bir belge varsa eklemez."""
    try:
        for document in documents:
            # Aynı başlıkta bir belge var mı kontrol et
            existing_document = collection.find_one({"title": document["title"]})
            if existing_document:
                print(
                    f"Document with title '{document['title']}' already exists, skipping."
                )
                continue  # Aynı başlık varsa bu belgeyi geç

            # Eğer aynı başlık yoksa ekle
            collection.insert_one(document)
            print(f"Document successfully added: {document['title']}")
    except Exception as e:
        print(f"Error: Could not insert document(s)! {e}")

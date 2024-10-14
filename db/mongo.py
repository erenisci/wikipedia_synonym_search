import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv
from utils.xml_processor import extract_articles_from_dump


load_dotenv()


def connect_mongo():
    DATABASE_URL = os.getenv("DATABASE_URL").replace(
        "<db_password>", os.getenv("DATABASE_PASSWORD")
    )
    try:
        client = MongoClient(DATABASE_URL)
        db = client["wikipedia"]
        print("Connected to MongoDB.")
        return client, db
    except Exception as e:
        print(f"Error: Could not connect to MongoDB! {e}")
        raise


# Verileri MongoDB'ye kaydet
def save_to_mongodb(db, file_path):
    collection = db["wikipedia_tr"]

    # Title alanını benzersiz kılmak için bir indeks ekleyelim
    collection.create_index("title", unique=True)

    for article in extract_articles_from_dump(file_path):
        # MongoDB'de aynı başlığa sahip veri var mı kontrol et
        if collection.find_one({"title": article["title"]}):
            print(f"Makale zaten var, atlanıyor: {article['title']}")
        else:
            try:
                collection.insert_one(article)
                print(f"Makale kaydedildi: {article['title']}")
            except DuplicateKeyError:
                print(f"Makale zaten var, atlanıyor: {article['title']}")

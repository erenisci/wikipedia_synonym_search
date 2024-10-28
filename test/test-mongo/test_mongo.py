import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Ortam değişkenlerini yükle
load_dotenv()

# MongoDB bağlantısını ayarla
MONGO_DB_URL = os.getenv("DATABASE_URL").replace(
    "<db_password>", os.getenv("DATABASE_PASSWORD")
) 

# MongoDB istemcisini oluştur
client = MongoClient(MONGO_DB_URL)
db = client["trtr"]  # Veritabanı adı
collection = db["trtrtr"]  # Koleksiyon adı

# Örnek veriyi ekleyin
sample_data = {
    "title": "Örnek Başlık",
    "text": "Bu bir örnek metindir.",
    "url": "http://ornek-url.com"
}

try:
    collection.insert_one(sample_data)
    print("Örnek veri eklendi.")
except DuplicateKeyError:
    print("Bu belge zaten mevcut.")

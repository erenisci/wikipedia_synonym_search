import os
import pymongo
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from gensim.models import Word2Vec
import numpy as np  # NumPy modülünü ekledik

# Ortam değişkenlerini yükle
load_dotenv()

# MongoDB bağlantısı
MONGO_DB_URL = os.getenv("DATABASE_URL").replace(
    "<db_password>", os.getenv("DATABASE_PASSWORD")
)
client = pymongo.MongoClient(MONGO_DB_URL)
db = client["wikipedia"]
collection = db["wikipedia_tr"]

# Elasticsearch bulut bağlantısı
ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

if not ELASTIC_CLOUD_ID or not ELASTIC_USERNAME or not ELASTIC_PASSWORD:
    raise ValueError("Elasticsearch bağlantı bilgileri ortam değişkenlerinde eksik.")

try:
    es = Elasticsearch(
        cloud_id=ELASTIC_CLOUD_ID, basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
    )
    if es.ping():
        print("Elasticsearch Bulut'a başarıyla bağlanıldı!")
    else:
        raise ConnectionError("Elasticsearch Bulut'a bağlanılamadı.")
except Exception as e:
    raise ConnectionError(f"Elasticsearch Bulut'a bağlanırken hata oluştu: {e}")

# Word2Vec modelini yükle
word_model = Word2Vec.load("w2v_custom.model")


# Elasticsearch indeks ayarları
def create_index():
    index_settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "turkish_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "turkish_stop", "turkish_stemmer"],
                    }
                },
                "filter": {
                    "turkish_stop": {
                        "type": "stop",
                        "stopwords": "_turkish_",
                    },
                    "turkish_stemmer": {
                        "type": "stemmer",
                        "language": "turkish",
                    },
                },
            }
        },
        "mappings": {
            "properties": {
                "title": {"type": "text", "analyzer": "turkish_analyzer"},
                "text": {"type": "text", "analyzer": "turkish_analyzer"},
                "url": {"type": "keyword"},
                "word_vector": {
                    "type": "dense_vector",
                    "dims": 100,  # Word2Vec modelinizin vektör boyutuyla eşleşmelidir.
                },
            }
        },
    }
    if not es.indices.exists(index="wikipedia"):
        es.indices.create(index="wikipedia", body=index_settings)
        print("Elasticsearch indeks oluşturuldu.")
    else:
        print("Elasticsearch indeksi zaten mevcut, oluşturma atlandı.")


# MongoDB'den makaleleri al ve Elasticsearch'e toplu ekle
def index_articles(batch_size=100):
    total_documents = collection.count_documents({})
    for skip in range(0, total_documents, batch_size):
        cursor = collection.find().skip(skip).limit(batch_size)
        actions = []

        for article in cursor:
            # Word2Vec modelinden vektör oluştur
            tokens = article["text"].split()
            vectors = [word_model.wv[word] for word in tokens if word in word_model.wv]
            if vectors:
                avg_vector = np.mean(
                    vectors, axis=0
                )  # NumPy ile ortalama vektör hesapla
            else:
                avg_vector = np.zeros(
                    100
                )  # Eğer uygun vektör bulunamazsa sıfır dolu bir NumPy array döndür

            action = {
                "_op_type": "index",
                "_index": "wikipedia",
                "_id": str(article["_id"]),
                "_source": {
                    "title": article["title"],
                    "text": article["text"],
                    "url": article.get("url", ""),
                    "word_vector": avg_vector.tolist(),  # NumPy array'i listeye çevirerek ekle
                },
            }
            actions.append(action)

        if actions:
            bulk(es, actions)
            print(f"İndekslendi: {len(actions)} belge - Kaydedildi")


if __name__ == "__main__":
    create_index()
    index_articles()

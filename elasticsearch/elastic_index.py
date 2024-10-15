from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from db.mongo import connect_mongo

# MongoDB ve Elasticsearch'e bağlan
client, db = connect_mongo()
collection = db["wikipedia_tr"]

es = Elasticsearch("http://localhost:9200")


# Elasticsearch indeks ayarları
def create_index():
    index_settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "turkish_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "asciifolding",
                            "turkish_stop",
                            "turkish_stemmer",
                        ],
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {"type": "text", "analyzer": "turkish_analyzer"},
                "text": {"type": "text", "analyzer": "turkish_analyzer"},
            }
        },
    }
    # Eğer indeks varsa geç, yoksa oluştur
    if not es.indices.exists(index="wikipedia"):
        es.indices.create(index="wikipedia", body=index_settings)


# MongoDB'den makaleleri al ve Elasticsearch'e ekle
def index_articles():
    actions = []
    for article in collection.find():
        action = {
            "_index": "wikipedia",
            "_id": str(article["_id"]),
            "_source": {"title": article["title"], "text": article["text"]},
        }
        actions.append(action)
    bulk(es, actions)


create_index()
index_articles()

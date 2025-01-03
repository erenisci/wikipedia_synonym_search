import os
from multiprocessing import Pool

import numpy as np
import pymongo
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from gensim.models import Word2Vec

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = pymongo.MongoClient(MONGO_URL)

db = client["wikipedia"]
collection = db["wikipedia_tr"]

ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_PORT = os.getenv("ELASTIC_PORT")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

try:
    es = Elasticsearch(
        hosts=[ELASTIC_URL],
        http_auth=((ELASTIC_USERNAME, ELASTIC_PASSWORD)),
        timeout=60,
        max_retries=10,
        retry_on_timeout=True,
    )
    if es.ping():
        print("Elasticsearch sunucusuna başarıyla bağlanıldı!")
    else:
        raise ConnectionError("Elasticsearch sunucusuna bağlanılamadı.")
except Exception as e:
    raise ConnectionError(f"Elasticsearch bağlantı hatası: {e}")

try:
    word_model = Word2Vec.load("model/gensim_w2v_model.model")
    print("Word2Vec modeli başarıyla yüklendi.")
except FileNotFoundError:
    raise FileNotFoundError(
        "Word2Vec modeli bulunamadı! Lütfen doğru dosyayı kontrol edin."
    )


def get_zero_vector():
    return np.zeros(100)


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
            "dynamic": "strict",
            "properties": {
                "title": {"type": "text", "analyzer": "turkish_analyzer"},
                "text": {"type": "text", "analyzer": "turkish_analyzer"},
                "url": {"type": "keyword"},
                "keywords": {
                    "type": "nested",
                    "properties": {
                        "word": {"type": "text", "analyzer": "turkish_analyzer"},
                        "frequency": {"type": "integer"},
                    },
                },
                "word_vector": {
                    "type": "dense_vector",
                    "dims": 100,
                },
            },
        },
    }

    try:
        if not es.indices.exists(index="wikipedia"):
            es.indices.create(index="wikipedia", body=index_settings)
            print("Elasticsearch indeksi başarıyla oluşturuldu.")
        else:
            print("Elasticsearch indeksi zaten mevcut, oluşturma atlandı.")
    except Exception as e:
        print(f"İndeks oluşturulurken hata oluştu: {e}")


def process_batch(batch_range):
    skip, batch_size = batch_range
    cursor = collection.find().skip(skip).limit(batch_size)
    actions = []

    for article in cursor:
        tokens = article.get("text", "").split()
        vectors = []

        if "keywords" in article:
            for keyword in article["keywords"]:
                word = keyword.get("word", "")
                if word in word_model.wv:
                    vectors.append(word_model.wv[word])
                else:
                    vectors.append(get_zero_vector())

        if vectors:
            avg_vector = np.mean(vectors, axis=0)
        else:
            avg_vector = get_zero_vector()

        action = {
            "_op_type": "index",
            "_index": "wikipedia",
            "_id": str(article["_id"]),
            "_source": {
                "title": article.get("title", "Belirtilmemiş"),
                "text": article.get("text", ""),
                "url": article.get("url", ""),
                "word_vector": avg_vector.tolist(),
            },
        }
        actions.append(action)

    if actions:
        try:
            success, failed = bulk(es, actions, raise_on_error=False)
            print(f"İndekslendi: {success} belge - Hatalı belge sayısı: {len(failed)}")
        except Exception as e:
            pass


def index_articles(batch_size=1000, processes=4):
    total_documents = collection.count_documents({})
    print(f"Toplam belgeler: {total_documents}")

    batch_ranges = [
        (skip, batch_size) for skip in range(0, total_documents, batch_size)
    ]

    with Pool(processes=processes) as pool:
        pool.map(process_batch, batch_ranges)

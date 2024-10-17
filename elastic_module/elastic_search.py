# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import numpy as np
from gensim.models import Word2Vec

# Ortam değişkenlerini yükle
load_dotenv()

# Elasticsearch bulut bağlantısı
ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

# Elasticsearch bağlantısı
es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID, basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

model = Word2Vec.load("word2vec.model")

def get_vector_from_word(word):
    try:
        return model.wv[word].tolist()
    except KeyError:
        return np.zeros(model.vector_size).tolist()

def search_similar_words(query):
    query_vector = get_vector_from_word(query)
    
    if all(v == 0 for v in query_vector):
        print("Verilen kelime için vektör bulunamadı.")
        return

    try:

        response = es.search(
            index="wikipedia",
            body={
                "query": {
                    "script_score": {
                        "query": {
                            "match_all": {}
                        },
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'vector_field') + 1.0",
                            "params": {
                                "query_vector": query_vector
                            }
                        }
                    }
                }
            }
        )

        for hit in response["hits"]["hits"]:
            print(f"Başlık: {hit['_source']['title']}, Skor: {hit['_score']}")
    except Exception as e:
        print(f"Arama işlemi sırasında hata oluştu: {e}")

if __name__ == "__main__":
    query = input("Bir kelime girin: ")
    search_similar_words(query)


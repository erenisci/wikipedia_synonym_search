# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

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


def search_articles(query):
    try:
        response = es.search(
            index="wikipedia", body={"query": {"match": {"text": query}}}
        )
        for hit in response["hits"]["hits"]:
            print(f"Başlık: {hit['_source']['title']}, Skor: {hit['_score']}")
    except Exception as e:
        print(f"Arama işlemi sırasında hata oluştu: {e}")
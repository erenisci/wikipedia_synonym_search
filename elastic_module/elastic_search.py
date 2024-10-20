# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID, basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

def search_articles(query):
    try:
        response = es.search(
            index="wikipedia", 
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["text", "synonyms"],  
                        "type": "best_fields"  
                    }
                }
            }
        )
        return [(hit['_source']['title'], hit['_score']) for hit in response["hits"]["hits"]]
    except Exception as e:
        print(f"Arama işlemi sırasında hata oluştu: {e}")
        return []

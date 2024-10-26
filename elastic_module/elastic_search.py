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
                        "fields": ["title", "text"],
                        "type": "best_fields",
                    }
                }
            },
        )

        return [
            {
                "title": hit["_source"]["title"],
                "url": hit["_source"].get("url", "#"),
                "text": hit["_source"]["text"],
            }
            for hit in response["hits"]["hits"]
        ]
    except Exception as e:
        print(f"Error during search: {e}")
        return []

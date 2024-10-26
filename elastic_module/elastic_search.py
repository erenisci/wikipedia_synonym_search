from elasticsearch import Elasticsearch
from gensim.models import Word2Vec
from tabulate import tabulate
from nltk.tokenize import word_tokenize
import string
from dotenv import load_dotenv
import os

load_dotenv()

ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID, basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

model = Word2Vec.load("w2v_.model")


def fetch_data_from_elastic(index_name, size=1000):
    results = []
    try:
        response = es.search(
            index=index_name, body={"query": {"match_all": {}}, "size": size}
        )
        for hit in response["hits"]["hits"]:
            results.append(hit["_source"]["text"])
    except Exception as e:
        print(f"Elasticsearch'ten veri çekme hatası: {e}")
    return results


def clean_and_tokenize(corpus):
    corpus_cleaned = []
    for text in corpus:
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = text.lower()
        tokens = word_tokenize(text)
        corpus_cleaned.append(tokens)
    return corpus_cleaned


def get_synonyms(word):
    try:
        return [syn[0] for syn in model.wv.most_similar(word)]
    except KeyError:
        return []


def search_articles_with_synonyms(query):
    synonyms = get_synonyms(query)
    all_queries = [query] + synonyms


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

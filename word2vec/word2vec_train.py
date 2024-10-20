from elasticsearch import Elasticsearch
from gensim.models import Word2Vec
import string
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv
import os

load_dotenv()

ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

es = Elasticsearch(cloud_id=ELASTIC_CLOUD_ID, basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD))

def fetch_data_from_elastic(index_name, size=1000):
    results = []
    try:
        response = es.search(index=index_name, body={
            "query": {
                "match_all": {}
            },
            "size": size  # size'ı burada veriyoruz
        })
        for hit in response['hits']['hits']:
            results.append(hit['_source']['text'])
    except Exception as e:
        print(f"Elasticsearch'ten veri çekme hatası: {e}")
    return results

def clean_and_tokenize(corpus):
    corpus_cleaned = []
    for text in corpus:
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.lower()
        tokens = word_tokenize(text)
        corpus_cleaned.append(tokens)
    return corpus_cleaned

if __name__ == "__main__":
    data = fetch_data_from_elastic('wikipedia')
    cleaned_data = clean_and_tokenize(data)
    word_model = Word2Vec(sentences=cleaned_data, vector_size=100, min_count=7, window=5, epochs=3, workers=12)
    word_model.save("new_w2v_model.model")

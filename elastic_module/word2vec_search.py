# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import numpy as np
from gensim.models import Word2Vec

load_dotenv()

ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID, basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
)

model = Word2Vec.load("word2vec.model")

def find_synonyms(word, topn=10):

    try:

        similar_words = model.wv.most_similar(word, topn=topn)
        for similar_word, score in similar_words:
            print(f"Eş Anlamlı: {similar_word}, Skor: {score}")
    except KeyError:
        print(f"'{word}' kelimesi modelde bulunamadı.")

if __name__ == "__main__":
    query = input("Bir kelime girin: ")
    find_synonyms(query)

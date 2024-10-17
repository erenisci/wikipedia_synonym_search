# -*- coding: utf-8 -*-

import gensim
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
import pymongo
from dotenv import load_dotenv
import os

nltk.download('punkt')

load_dotenv()

MONGO_DB_URL = os.getenv("DATABASE_URL").replace(
    "<db_password>", os.getenv("DATABASE_PASSWORD")
)
client = pymongo.MongoClient(MONGO_DB_URL)
db = client["wikipedia"]
collection = db["wikipedia_tr"]

sentences = []
for article in collection.find():
    text = article.get("text", "")
    tokenized_text = word_tokenize(text.lower())
    sentences.append(tokenized_text)

model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=1, workers=4)

model.save("word2vec.model")

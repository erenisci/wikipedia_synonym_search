# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
from elastic_search import search_articles
from gensim.models import Word2Vec

app = Flask(__name__)

word_model = Word2Vec.load("w2v_custom_from_db.model")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    results = search_articles(query)
    return jsonify(results)

@app.route("/word2vec", methods=["GET"])
def word2vec():
    query = request.args.get("query", "").lower() 
    synonyms = []

    if query:
        try:
            similar_words = word_model.wv.most_similar(query, topn=10)  
            synonyms = [word for word, _ in similar_words]
        except KeyError:
            synonyms = []

    return jsonify(synonyms)


if __name__ == "__main__":
    app.run(debug=True)
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from elastic_search import search_articles_with_synonyms  

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    synonyms = []  # Eş anlamlılar için bir liste oluştur
    query = ""  # query değişkenini burada başlatıyoruz

    if request.method == 'POST':
        query = request.form['query']
        results, synonyms = search_articles_with_synonyms(query)  # İki değeri unpack ediyoruz

    return render_template('index.html', results=results, synonyms=synonyms, query=query)


if __name__ == "__main__":
    app.run(debug=True)

# app.py
from flask import Flask, request, jsonify
from gensim.models import Word2Vec

app = Flask(__name__)

model = Word2Vec.load("word2vec.model")

@app.route('/find-synonyms', methods=['POST'])
def find_synonyms():
    data = request.json
    word = data.get('word')
    if not word:
        return jsonify({"message": "Kelime gerekli."}), 400
    try:
        similar_words = model.wv.most_similar(word, topn=10)
        synonyms = [{"word": similar_word, "score": float(score)} for similar_word, score in similar_words]
        return jsonify({"synonyms": synonyms})
    except KeyError:
        return jsonify({"message": f"'{word}' kelimesi modelde bulunamadı."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

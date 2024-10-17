# -*- coding: utf-8 -*-
# 
import gensim
from gensim.models import KeyedVectors

model_path = '/Users/zcengiz/Downloads/wikipedia_synonym_search/resources/cc.tr.300.vec' 
word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=False)

def find_automatic_synonyms(word, topn=10, similarity_threshold=0.7):
    try:

        if word not in word_vectors:
            print(f"'{word}' kelimesi modelde bulunamadı.")
            return

        similar_words = word_vectors.most_similar(word, topn=topn)

        print(f"'{word}' kelimesine benzer olabilecek kelimeler:")
        for similar_word, score in similar_words:

            if word in similar_word or '-' in similar_word:
                continue

            if score >= similarity_threshold:
                print(f"Eş Anlamlı: {similar_word}, Skor: {score}")
            else:
                print(f"Benzer Ama Eşik Altı: {similar_word}, Skor: {score}")

    except KeyError:
        print(f"'{word}' kelimesi modelde bulunamadı.")

if __name__ == "__main__":
    query = input("Bir kelime girin: ")
    find_automatic_synonyms(query)
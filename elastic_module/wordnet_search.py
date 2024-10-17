# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')
nltk.download('omw-1.4')

def find_true_synonyms(word):

    synonyms = set()  

    for syn in wn.synsets(word, lang='tur'):
        for lemma in syn.lemmas(lang='tur'):
            synonyms.add(lemma.name())

    if synonyms:
        print(f"'{word}' kelimesinin eş anlamlıları:")
        for synonym in synonyms:
            print(synonym)
    else:
        print(f"'{word}' kelimesi için eş anlamlı bulunamadı.")

if __name__ == "__main__":
    query = input("Bir kelime girin: ")
    find_true_synonyms(query)

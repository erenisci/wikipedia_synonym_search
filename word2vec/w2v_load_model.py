# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from tabulate import tabulate

model = Word2Vec.load("w2v_.model")

q = input("Bir kelime girin: ")
print(f"\n{q.capitalize()} kelimesine en yakın 10 kelime:\n")
print(tabulate(model.wv.most_similar(q), headers=["Kelime", "Benzerlik Skoru"]))

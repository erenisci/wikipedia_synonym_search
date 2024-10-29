from gensim.models import Word2Vec

# Eğitilen modeli yükle
model = Word2Vec.load("test_w2v.model")

# Örneğin 'school' kelimesinin olup olmadığını kontrol edelim
test_word = "school"
if test_word in model.wv:
    print(f"Uyarı: '{test_word}' kelimesi modelde mevcut.")
else:
    print(f"'{test_word}' kelimesi modelde mevcut değil.")

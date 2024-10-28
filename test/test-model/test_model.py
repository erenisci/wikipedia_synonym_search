from gensim.models import Word2Vec

# Eğitilen modeli yükle
model_path = "/Users/zcengiz/Desktop/son/test/w2v_custom_from_file.model"
model = Word2Vec.load(model_path)

# Kullanıcıdan kelimeyi al
test_word = input("Yakın anlamlısını bulmak istediğiniz kelimeyi girin: ")

# Girilen kelimenin modelde olup olmadığını kontrol et
if test_word in model.wv:
    closest_word = model.wv.most_similar(test_word, topn=1)[0][0]
    print(f"'{test_word}' kelimesine en yakın anlam: '{closest_word}'")
else:
    print(f"'{test_word}' kelimesi modelde mevcut değil.")

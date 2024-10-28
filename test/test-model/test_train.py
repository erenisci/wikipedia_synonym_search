import string
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

# Test dosyasını oku ve temizle
def fetch_and_clean_data(file_path):
    corpus_cleaned = []

    # Dosyayı oku
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Satırdaki noktalama işaretlerini temizle ve küçük harfe çevir
            text = line.translate(str.maketrans("", "", string.punctuation)).lower()

            # Tokenizasyon işlemi
            tokens = word_tokenize(text)
            corpus_cleaned.append(tokens)

    return corpus_cleaned

if __name__ == "__main__":
    # test.txt dosyasından veriyi al ve temizle
    file_path = "/Users/zcengiz/Desktop/son/test/test.txt"
    cleaned_data = fetch_and_clean_data(file_path)

    # Word2Vec modelini sıfırdan başlat ve eğit
    word_model = Word2Vec(
        sentences=cleaned_data,
        vector_size=100,
        min_count=1,
        window=5,
        epochs=10,
        workers=4,
    )

    # Eğitilen modeli kaydet
    word_model.save("/Users/zcengiz/Desktop/son/test/w2v_custom_from_file.model")

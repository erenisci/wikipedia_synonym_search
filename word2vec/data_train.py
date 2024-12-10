from data_processing import fetch_and_clean_data
from gensim.models import Word2Vec


def train_model():
    print("Veriler işleniyor...")
    cleaned_data = fetch_and_clean_data()

    print("Model oluşturuluyor ve eğitiliyor...")
    model = Word2Vec(
        sentences=cleaned_data,
        vector_size=100,
        min_count=5,
        window=5,
        sg=1,
        workers=4,
        epochs=10,
    )

    model.save("model/gensim_w2v_model.model")
    print("Model başarıyla kaydedildi!")

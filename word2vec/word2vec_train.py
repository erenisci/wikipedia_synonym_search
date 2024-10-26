import pymongo
import string
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from dotenv import load_dotenv
import os

# Ortam değişkenlerini yükle
load_dotenv()

# MongoDB bağlantısı
MONGO_DB_URL = os.getenv("DATABASE_URL").replace(
    "<db_password>", os.getenv("DATABASE_PASSWORD")
)
client = pymongo.MongoClient(MONGO_DB_URL)
db = client["wikipedia"]
collection = db["wikipedia_tr"]


# MongoDB'deki verileri temizle ve tokenize et
def fetch_and_clean_data():
    corpus_cleaned = []

    # Veritabanındaki her makaleyi al
    for document in collection.find({}, {"text": 1}):
        text = document.get("text", "")

        # Noktalama işaretlerini temizle ve küçük harfe çevir
        text = text.translate(str.maketrans("", "", string.punctuation)).lower()

        # Tokenizasyon işlemi
        tokens = word_tokenize(text)

        corpus_cleaned.append(tokens)

    return corpus_cleaned


if __name__ == "__main__":
    # Veritabanından veriyi al ve temizle
    cleaned_data = fetch_and_clean_data()

    # Word2Vec modelini sıfırdan başlat ve eğit
    word_model = Word2Vec(
        sentences=cleaned_data,
        vector_size=100,
        min_count=7,
        window=5,
        epochs=10,
        workers=12,
    )

    # Eğitilen modeli kaydet
    word_model.save("w2v_custom_from_db.model")

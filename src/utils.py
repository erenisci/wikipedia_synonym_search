import re

import fasttext

# FastText modelini yükle
model = fasttext.load_model("models/cc.tr.300.bin")


def get_synonyms(word):
    """Verilen kelimenin eş anlamlılarını döner."""
    try:
        synonyms = model.get_nearest_neighbors(word, k=10)
        return [synonym[1] for synonym in synonyms]
    except Exception as e:
        print(f"Error getting synonyms for '{word}': {e}")
        return []


def clean_text(text):
    """Metni temizler ve düzenler."""
    try:
        text = re.sub(r"<ref>.*?</ref>", "", text)  # <ref> etiketlerini kaldır
        text = re.sub(r"\[\[.*?\]\]", "", text)  # [[...]] etiketlerini kaldır
        text = text.replace("{", "").replace("}", "")
        text = text.replace("&lt;", "<").replace("&gt;", ">")
        text = re.sub(r"[^\w\s]", "", text)  # Noktalama işaretlerini kaldır
        return text.strip()
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return text  # Hata durumunda orijinal metni döndür

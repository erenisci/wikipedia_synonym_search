import re
import xml.etree.ElementTree as ET
from collections import Counter

from pymongo import InsertOne
from snowballstemmer import TurkishStemmer

turkStem = TurkishStemmer()


def clean_and_stem_title(title):
    """
    Başlıkları temizler ve her kelimenin kökünü bulur.
    """
    cleaned_title = re.sub(r"[^\wçğıöşüÇĞİÖŞÜ\s]", "", title.lower())

    if not cleaned_title.strip():
        return [], []

    title_words = cleaned_title.split()
    stemmed_title = [turkStem.stemWord(word) for word in title_words]

    return title_words, stemmed_title


def clean_and_stem_word(word):
    """
    Kelimeyi özel karakterlerden arındırır ve kök bulur.
    """
    cleaned_word = re.sub(r"[()]", "", word)
    cleaned_word = re.sub(r"^[^\wçğıöşüÇĞİÖŞÜ]+|[^\wçğıöşüÇĞİÖŞÜ]+$", "", word)

    if not cleaned_word.strip():
        return ""

    root = turkStem.stemWord(cleaned_word)
    return root


def extract_articles_from_dump(file_path):
    bulk_operations = []
    with open(file_path, "r", encoding="utf-8") as file:
        context = ET.iterparse(file, events=("end",))

        for event, elem in context:
            if elem.tag.endswith("page"):
                title = elem.find(".//{http://www.mediawiki.org/xml/export-0.11/}title")
                text = elem.find(".//{http://www.mediawiki.org/xml/export-0.11/}text")

                if title is not None and text is not None:
                    title_text = title.text
                    text_content = text.text
                    if title_text and text_content:
                        clean_text = clean_wiki_text(text_content)

                        keywords = []
                        title_words, stemmed_title = clean_and_stem_title(
                            title_text.lower()
                        )

                        if not title_words:
                            print(f"Boş başlık bulundu, atlanıyor: {title_text}")
                            continue

                        for title_word, title_root in zip(title_words, stemmed_title):
                            keywords.append(
                                {
                                    "word": title_word,
                                    "root": title_root,
                                    "frequency": 1,
                                    "relevance": 1,
                                }
                            )

                        words = re.findall(r"[^\s]+", clean_text.lower())
                        word_counts = Counter(words)

                        max_frequency = max(word_counts.values(), default=1)

                        for word, count in word_counts.items():
                            root = clean_and_stem_word(word)

                            relevance = calculate_relevance(count, max_frequency)

                            keywords.append(
                                {
                                    "word": word,
                                    "root": root,
                                    "frequency": count,
                                    "relevance": relevance,
                                }
                            )

                        base_url = "https://tr.wikipedia.org/wiki/"
                        formatted_title = title_text.replace(" ", "_")
                        url = base_url + formatted_title

                        article = {
                            "title": title_text,
                            "text": clean_text,
                            "url": url,
                            "keywords": keywords,
                        }

                        bulk_operations.append(InsertOne(article))

                        if len(bulk_operations) >= 1000:
                            yield bulk_operations
                            bulk_operations = []

                elem.clear()

        if bulk_operations:
            yield bulk_operations


def clean_wiki_text(text):
    # Bilgi kutusu ve şablonları temizle: {{...}}
    text = re.sub(r"\{\{(?:[^{}]|\{[^{}]*\})*?\}\}", "", text, flags=re.DOTALL)

    # ''' veya '' gibi kalın ve italik yazım işaretlerini kaldır
    text = re.sub(r"'{2,}", "", text)

    # HTML etiketlerini temizle: <...>
    text = re.sub(r"<.*?>", "", text, flags=re.DOTALL)

    # [[Linkler|bağlantı]] veya [[bağlantı]] şeklindeki linklerin içeriğini al
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", text)

    # Dipnot ve açıklama gibi özel şablonları temizle: {{efn|...}} veya {{sfn|...}}
    text = re.sub(r"\{\{efn.*?\}\}", "", text, flags=re.DOTALL)
    text = re.sub(r"\{\{sfn.*?\}\}", "", text, flags=re.DOTALL)

    # Fazlalıkları temizle: {{yaklaşık}}, {{dil|...}}, vb.
    text = re.sub(r"\{\{.*?\}\}", "", text, flags=re.DOTALL)

    # Bilgi kutusu parametrelerini temizle: | parametre = ... veya boş olan parametreler
    text = re.sub(r"\|\s*[\w\s]+=\s*[^|\n]*", "", text)

    # Boş |name= gibi kalan parametreleri temizle
    text = re.sub(r"\|\w+\s*=\s*[^|}]*", "", text)

    # Görsel veya resim açıklamalarını temizle: "küçükresim", "sağ", "sol", "right", "left", "yukarı", "aşağı" ve hizalama bilgileri
    text = re.sub(r"küçükresim[^\|]*\|?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"sağ\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"sol\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"right\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"left\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"yukarı\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"aşağı\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"upleft\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"upright\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"downleft\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"downright\|", "", text, flags=re.IGNORECASE)

    # Görsel parametreleri ve boyut bilgilerini temizle: "[[... 300px|...]]"
    text = re.sub(r"\[\[.*?\s+\d{2,4}px\|[^\]]*\]\]", "", text, flags=re.IGNORECASE)

    # Gereksiz kapanış işaretleri veya sembolleri temizle
    text = re.sub(r"\}\}", "", text)

    # Çift virgül veya fazla sembolleri temizle
    text = re.sub(r",,", ",", text)
    text = re.sub(r"\s*,\s*", ", ", text)  # Boşluklarla birlikte düzenle

    # Gereksiz tekrar eden kelimeleri veya sembolleri temizle
    text = re.sub(r"(\b\w+\b)( \1)+", r"\1", text)

    # Gereksiz boşlukları temizle
    text = re.sub(r"\s+", " ", text).strip()

    # Kategori başlıklarını kaldır: Kategori:xxx
    text = re.sub(r"\[\[Kategori:[^\]]+\]\]", "", text)

    # "==Başlık==" ve alt başlıkları kaldır
    text = re.sub(r"==.*?==", "", text)

    # URL'leri kaldır
    text = re.sub(r"http[s]?://[^\s]+", "", text)

    return text


def calculate_relevance(frequency, max_frequency):
    relevance = min(frequency / max_frequency, 1.0)
    return relevance

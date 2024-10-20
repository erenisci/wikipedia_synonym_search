import re
import xml.etree.ElementTree as ET

def extract_articles_from_dump(file_path, output_file):
    with open(file_path, "r", encoding="utf-8") as file, open(output_file, "w", encoding="utf-8") as out_file:
        context = ET.iterparse(file, events=("end",))
        for event, elem in context:
            if elem.tag.endswith("page"):
                title = elem.find(".//{http://www.mediawiki.org/xml/export-0.11/}title")
                text = elem.find(".//{http://www.mediawiki.org/xml/export-0.11/}text")
                revision = elem.find(
                    ".//{http://www.mediawiki.org/xml/export-0.11/}revision"
                )
                timestamp = (
                    revision.find(
                        ".//{http://www.mediawiki.org/xml/export-0.11/}timestamp"
                    )
                    if revision is not None
                    else None
                )

                if title is not None and text is not None:
                    title_text = title.text
                    text_content = text.text
                    if title_text and text_content:
                        clean_text = clean_wiki_text(text_content)

                        # URL oluşturma
                        base_url = "https://tr.wikipedia.org/wiki/"
                        formatted_title = title_text.replace(" ", "_")
                        url = base_url + formatted_title

                        article = {
                            "title": title_text,
                            "text": clean_text,
                            "url": url,
                            "timestamp": (
                                timestamp.text if timestamp is not None else None
                            ),
                        }
                        print(f"İşleniyor: Başlık - {title_text}, URL - {url}")
                        out_file.write(clean_text + "\n")  # Temizlenmiş metni dosyaya yaz

                elem.clear()

def clean_wiki_text(text):
    # Bilgi kutusu ve şablonları temizle: {{...}}
    text = re.sub(r"\{\{(?:[^{}]|\{[^{}]*\})*?\}\}", "", text, flags=re.DOTALL)

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

    # Görsel veya resim açıklamalarını temizle
    text = re.sub(r"küçükresim[^\|]*\|?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"sağ\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"sol\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"right\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"left\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"yukarı\|", "", text, flags=re.IGNORECASE)
    text = re.sub(r"aşağı\|", "", text, flags=re.IGNORECASE)

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

    return text

# Fonksiyonu çağırın
if __name__ == "__main__":
    extract_articles_from_dump('/Users/zcengiz/Desktop/sematic/word2vec/trwiki-latest-pages-articles.xml', 'cleanWikiText_.txt')

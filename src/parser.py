import xml.etree.ElementTree as ET

from src.database import insert_document
from src.utils import clean_text, get_synonyms


def parse_xml_and_store_in_mongo(file_path):
    """XML dosyasını oku ve veriyi MongoDB'ye kaydet."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        documents = []

        for page in root.findall(".//page"):
            title = page.find("title").text
            content = page.find("revision/text").text

            print(f"Processing title: {title}")  # Durum bilgisi

            # Temizleme işlemleri
            cleaned_content = clean_text(content)
            words = cleaned_content.split()

            # Eş anlamlıları bul
            synonyms = {word: get_synonyms(word) for word in set(words)}

            # Wikipedia URL'sini oluştur
            url = f"https://tr.wikipedia.org/wiki/{title}"

            # Veriyi MongoDB'ye ekle
            document = {
                "title": title,
                "content": cleaned_content,
                "words": words,
                "synonyms": synonyms,
                "url": url,
            }
            documents.append(document)

        # Belge listesini MongoDB'ye topluca ekle
        if documents:
            insert_document(documents)  # insert_many kullanılabilir

    except ET.ParseError as e:
        print(f"Error: Failed to parse XML file - {e}")
    except Exception as e:
        print(f"Error: An error occurred while processing {file_path} - {e}")

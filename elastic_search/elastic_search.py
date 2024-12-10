import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")


def connect_elasticsearch():
    try:
        es = Elasticsearch(
            hosts=[ELASTIC_URL],
            http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),
            timeout=60,
            max_retries=10,
            retry_on_timeout=True,
        )
        if es.ping():
            print("Elasticsearch sunucusuna başarıyla bağlanıldı!")
        else:
            raise ConnectionError("Elasticsearch sunucusuna bağlanılamadı.")
        return es
    except Exception as e:
        raise ConnectionError(f"Elasticsearch bağlantı hatası: {e}")


def search_articles(query, index="wikipedia"):
    es = connect_elasticsearch()

    search_body = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "title": {
                                "query": query,
                                "boost": 3.0,
                            }
                        }
                    },
                    {
                        "match": {
                            "text": {
                                "query": query,
                                "fuzziness": "AUTO",
                                "boost": 2.0,
                            }
                        }
                    },
                    {
                        "nested": {
                            "path": "keywords",
                            "query": {
                                "bool": {
                                    "should": [
                                        {
                                            "match": {
                                                "keywords.word": {
                                                    "query": query,
                                                    "fuzziness": "AUTO",
                                                    "boost": 1.5,
                                                }
                                            }
                                        },
                                    ]
                                }
                            },
                        }
                    },
                ],
                "minimum_should_match": 1,
            }
        }
    }

    try:
        response = es.search(index=index, body=search_body)
        total_hits = response["hits"]["total"]["value"]
        print(f"Toplam eşleşen belge sayısı: {total_hits}")

        results = []
        for hit in response["hits"]["hits"]:
            article = {
                "title": hit["_source"]["title"],
                "text": hit["_source"]["text"],
                "url": hit["_source"]["url"],
                "keywords": hit["_source"].get("keywords", []),
            }
            results.append(article)

        return results

    except Exception as e:
        print(f"Arama yapılırken hata oluştu: {e}")
        return []


def get_sentences_with_keyword(text, keyword):
    sentences = text.split(".")
    relevant_sentences = [
        sentence.strip()
        for sentence in sentences
        if keyword.lower() in sentence.lower()
    ]
    return relevant_sentences


def get_keyword_sentences_for_article(query, index="wikipedia"):
    articles = search_articles(query, index)

    for article in articles:
        title = article["title"]
        text = article["text"]
        print(f"Başlık: {title}")
        keyword_sentences = get_sentences_with_keyword(text, query)
        print(f"'{query}' kelimesinin geçtiği cümleler:")
        for sentence in keyword_sentences:
            print(f"- {sentence}")
        print("\n" + "-" * 50)

from elastic_search import search_articles, get_sentences_with_keyword

search_query = "veri madenciliği"

index_name = "wikipedia"

# Arama fonksiyonunu çağır
articles = search_articles(search_query, index=index_name)

# Arama sonuçlarını yazdır
if articles:
    print(f"Bulunan {len(articles)} belge:")
    for article in articles:
        print(f"Başlık: {article['title']}")
        print(f"URL: {article['url']}")
        print("İçerik (ilk 100 karakter):", article["text"][:100])
        print("-" * 50)
else:
    print("Eşleşen hiçbir belge bulunamadı.")

# Kullanıcı bir belgeyi tıkladığında, o belgeyi alıp kelimeyi içeren cümleleri gösterelim
if articles:
    # Örnek olarak, ilk belgedeki cümleleri alalım
    selected_article = articles[0]
    keyword = "veri madenciliği"  # Burada yine aradığınız kelimeyi kullanabilirsiniz
    sentences = get_sentences_with_keyword(selected_article["text"], keyword)

    if sentences:
        print("\nKelimenin geçtiği cümleler:")
        for sentence in sentences:
            print(f"- {sentence}")
    else:
        print(f"\n'{keyword}' kelimesinin geçtiği herhangi bir cümle bulunamadı.")

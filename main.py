# -*- coding: utf-8 -*-


from elastic_module.elastic_search import search_articles

if __name__ == "__main__":
    query = input("Aramak istediğiniz kelimeyi girin: ")  
    search_articles(query)  

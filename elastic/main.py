from elastic_config import create_index, index_articles

if __name__ == "__main__":
    create_index()
    index_articles(batch_size=1000, processes=4)

# Wikipedia Synonym Search

**Wikipedia Synonym Search** is a sophisticated project that integrates Wikipedia data extraction, text processing, and advanced indexing mechanisms to enhance search capabilities using semantic similarity. By leveraging machine learning models like Word2Vec and integrating Elasticsearch for indexing, this project enables efficient synonym-based search functionality within the Wikipedia corpus.

## Features

- **Wikipedia Data Extraction**: Efficiently extracts and processes articles from Wikipedia dump files in XML format.
- **Text Cleaning and Preprocessing**: Cleans and processes raw Wikipedia text by removing templates, links, and special characters. 
- **Synonym Search**: Uses a pre-trained Word2Vec model to compute word vectors and identify semantically similar words (synonyms).
- **Elasticsearch Integration**: Uses Elasticsearch for fast, full-text search and indexing. The model also stores word vectors and other metadata in Elasticsearch, enabling efficient search across large datasets.
- **Parallel Processing**: The application employs multiprocessing to handle large batches of data, speeding up the indexing process and reducing overall processing time.

## Project Structure

```
wikipedia-synonym-search/
├── elastic/
│   ├── elastic_config.py       # Configuration for Elasticsearch
│   └── main.py                 # Main script to interact with Elasticsearch
├── model/
│   └── model.txt               # Pre-trained Word2Vec model
├── mongo/
│   ├── main.py                 # MongoDB interaction script
│   ├── mongo_config.py         # MongoDB configuration
│   └── xml_processor.py        # Processes XML dumps for MongoDB
├── resources/
│   └── resources.txt           # Additional resources or configuration
├── word2vec/
│   ├── data_processing.py      # Processes data for Word2Vec
│   ├── data_train.py           # Script for training Word2Vec model
│   └── main.py                 # Main script to run Word2Vec
├── requirements.txt            # List of dependencies
└── README.md                   # Project documentation (this file)
```

## Requirements

- **Python 3.x**
- **Elasticsearch** (running locally or remotely)
- **MongoDB**
- **Pre-trained Word2Vec model** (or train your own)

## Setup

### 1. Install Dependencies

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/wikipedia-synonym-search.git
cd wikipedia-synonym-search
python3 -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file with the following content:

```env
MONGO_URL=mongodb://localhost:27017
ELASTIC_URL=http://localhost
ELASTIC_PORT=9200
ELASTIC_USERNAME=your_username
ELASTIC_PASSWORD=your_password
```

Make sure MongoDB and Elasticsearch are running.

### 3. Word2Vec Model

If you don’t have a pre-trained Word2Vec model, you can train one or download a pre-trained model. Place it in the `model/` directory and name it `model.txt`.

### 4. Run the Project

#### 4.1 Index Wikipedia Articles

To index articles and their data (title, text, and word vectors) into Elasticsearch:

```bash
python elastic/main.py
```

This will extract and index articles into Elasticsearch.

#### 4.2 Extract Articles from XML

To extract articles from a Wikipedia XML dump and save them to MongoDB:

```bash
python mongo/main.py
```

This will process and save data to MongoDB.

#### 4.3 Word2Vec Processing and Training

To preprocess data for Word2Vec or train your own model, run:

```bash
python word2vec/data_processing.py
python word2vec/data_train.py
```

#### 4.4 Perform Search Queries

You can search for synonyms or related terms using Elasticsearch. Example query:

```python
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])

response = es.search(
    index="wikipedia",
    body={"query": {"match": {"text": "Türkçe"}}}
)

for hit in response["hits"]["hits"]:
    print(hit["_source"]["title"])
```

## How It Works

1. **Data Extraction**: Wikipedia XML dump files are processed and saved in MongoDB.
2. **Text Cleaning & Preprocessing**: The text is cleaned, tokenized, and lemmatized.
3. **Word2Vec Embeddings**: The Word2Vec model generates word embeddings for keywords.
4. **Elasticsearch**: Elasticsearch indexes the data for fast search queries, including synonym search based on word vectors.

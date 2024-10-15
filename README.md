# Wikipedia Synonym Search

Wikipedia Synonym Search is a project aimed at finding synonyms in the Turkish language using Wikipedia data and enabling search over this data. This project uses MongoDB and Elasticsearch to provide efficient and fast search over large-scale data.

## Project Structure

The project is organized as follows:
```plaintext
wikipedia-nlp-project/
├── main.py
├── db/
│   ├── mongo.py
│   └── __init__.py
├── elasticsearch/
│   ├── elastic_index.py
│   └── __init__.py
├── resources/
│   ├── wiki_dump_1.xml
│   ├── wiki_dump_2.xml
│   └── ...
├── utils/
│   ├── xml_processor.py
│   └── __init__.py
├── requirements.txt
├── .env
└── README.md
```

- main.py: The main file of the project. Loads data into MongoDB and starts the Elasticsearch indexing process.

- db/: MongoDB connection and data storage operations.

  - mongo.py: Functions for connecting to MongoDB and saving data.

- elasticsearch/: Contains operations related to Elasticsearch.

  - elastic_index.py: Code to index data from MongoDB to Elasticsearch.

- resources/: Folder containing Wikipedia XML files.

- utils/: Contains utility functions.

  - xml_processor.py: Processes and cleans data from XML files.

## Installation and Requirements

The project requires the following to run:

- Python 3.7+

- MongoDB

- Elasticsearch

- Python packages (included in requirements.txt)

## Required Packages

The following command will install all the necessary Python packages:
` pip install -r requirements.txt`

Important packages included in requirements.txt:

- **pymongo**: For MongoDB connection and operations.

- **elasticsearch**: For Elasticsearch connection and operations.

- **python-dotenv**: To load environment variables from .env file.

## Running Steps

1. Set Up .env File: Fill in the required information in the .env file for MongoDB connection:

```
DATABASE_URL=mongodb+srv://<username>:<password>@your_cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_PASSWORD=your_database_password
```

2. Prepare Wikipedia Data: Add Wikipedia XML files to the resources/ folder.

3. Load Data and Index:
   Run the main file to load data into MongoDB and index it in Elasticsearch:

   ```s
   python main.py
   ```

   This command processes all XML files in the resources/ folder, saves them to MongoDB, and then indexes them in Elasticsearch.

## Elasticsearch Settings

Elasticsearch is configured with a custom analyzer (turkish_analyzer) suitable for Turkish language analysis. This analyzer performs stemming, lowercasing, and filtering of Turkish stop words to achieve more accurate and efficient search results.

## Project Functions

- Processing Wikipedia Data: utils/xml_processor.py processes Wikipedia XML files, cleans them, and extracts important information such as title, text, and URL.

- Saving Data: db/mongo.py manages MongoDB connection and saves data to the database.

- Elasticsearch Indexing: elasticsearch/elastic_index.py indexes data from MongoDB to Elasticsearch, allowing fast searches over this data.

## Use Cases

This project is used to facilitate synonym searches over Turkish Wikipedia data. For example, when you search for the word "büyük" (big), you can easily find a document containing the phrase "İstanbul Türkiye'nin en büyük şehridir" (Istanbul is Turkey's largest city). This allows users to quickly access information by performing meaning-based searches in Turkish Wikipedia content.

## Future Plans

- Enhancing Turkish Synonym Support: Improve synonym support in Elasticsearch and expand the analyzer.

- User Interface: Develop a web-based interface for users to use this search engine.

- Data Update Automation: Add scheduled jobs to automatically update Wikipedia data.

## License

This project is licensed under the MIT License. For more information, see the LICENSE file.

## Contact

If you have any questions or need support, feel free to contact the project developer. I would be happy to help! 💖

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo
from datetime import datetime
import logging


class Lab4ProjectPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:
    """Pipeline to save items to MongoDB"""
    
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://localhost:27017'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'chanhtuoi_db'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION', 'articles')
        )

    def open_spider(self, spider):
        """Open database connection when spider starts"""
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            self.collection = self.db[self.mongo_collection]
            self.logger.info(f"Connected to MongoDB: {self.mongo_db}.{self.mongo_collection}")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def close_spider(self, spider):
        """Close database connection when spider closes"""
        if hasattr(self, 'client'):
            self.client.close()
            self.logger.info("MongoDB connection closed")

    def process_item(self, item, spider):
        """Process item and save to MongoDB"""
        try:
            # Convert item to dict
            item_dict = dict(item)
            
            # Add timestamp
            item_dict['saved_at'] = datetime.now()
            
            # Check if item already exists (by URL)
            existing = self.collection.find_one({'url': item_dict.get('url')})
            
            if existing:
                # Update existing document
                self.collection.update_one(
                    {'url': item_dict.get('url')},
                    {'$set': item_dict}
                )
                self.logger.info(f"Updated article: {item_dict.get('title', 'No title')}")
            else:
                # Insert new document
                result = self.collection.insert_one(item_dict)
                self.logger.info(f"Inserted new article: {item_dict.get('title', 'No title')} (ID: {result.inserted_id})")
            
            return item
            
        except Exception as e:
            self.logger.error(f"Error processing item: {e}")
            return item


class DuplicatesPipeline:
    """Pipeline to filter out duplicate items"""
    
    def __init__(self):
        self.seen_urls = set()
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter.get('url')
        
        if url in self.seen_urls:
            self.logger.info(f"Duplicate item found: {url}")
            raise DropItem(f"Duplicate item found: {url}")
        else:
            self.seen_urls.add(url)
            return item

#!/usr/bin/env python3
"""
Script to test MongoDB connection and show basic operations
"""

import pymongo
from datetime import datetime
import json

def test_mongodb_connection():
    """Test MongoDB connection and show basic operations"""
    print("=" * 60)
    print("MONGODB CONNECTION TEST")
    print("=" * 60)
    
    # MongoDB configuration
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DATABASE = 'chanhtuoi_db'
    MONGO_COLLECTION = 'articles'
    
    try:
        # Connect to MongoDB
        print("Connecting to MongoDB...")
        client = pymongo.MongoClient(MONGO_URI)
        
        # Test connection
        client.admin.command('ping')
        print("✓ Successfully connected to MongoDB!")
        
        # Get database and collection
        db = client[MONGO_DATABASE]
        collection = db[MONGO_COLLECTION]
        
        print(f"✓ Connected to database: {MONGO_DATABASE}")
        print(f"✓ Using collection: {MONGO_COLLECTION}")
        
        # Count documents
        count = collection.count_documents({})
        print(f"✓ Total documents in collection: {count}")
        
        if count > 0:
            print("\n" + "=" * 40)
            print("SAMPLE DOCUMENTS")
            print("=" * 40)
            
            # Show first 3 documents
            documents = list(collection.find().limit(3))
            for i, doc in enumerate(documents, 1):
                print(f"\nDocument {i}:")
                print(f"  Title: {doc.get('title', 'N/A')}")
                print(f"  URL: {doc.get('url', 'N/A')}")
                print(f"  Author: {doc.get('author', 'N/A')}")
                print(f"  Crawled at: {doc.get('crawled_at', 'N/A')}")
                print(f"  Content length: {len(doc.get('content', ''))} characters")
        
        # Show MongoDB operations examples
        print("\n" + "=" * 40)
        print("MONGODB OPERATIONS EXAMPLES")
        print("=" * 40)
        
        print("\n1. Find all documents:")
        print("   db.articles.find()")
        
        print("\n2. Find documents with specific title:")
        print("   db.articles.find({'title': /keyword/})")
        
        print("\n3. Count documents:")
        print("   db.articles.countDocuments()")
        
        print("\n4. Find one document:")
        print("   db.articles.findOne()")
        
        print("\n5. Find documents by author:")
        print("   db.articles.find({'author': 'Author Name'})")
        
        print("\n6. Find documents with content containing keyword:")
        print("   db.articles.find({'content': /keyword/})")
        
        print("\n7. Update a document:")
        print("   db.articles.updateOne({'url': 'article_url'}, {'$set': {'updated': true}})")
        
        print("\n8. Delete a document:")
        print("   db.articles.deleteOne({'url': 'article_url'})")
        
        print("\n9. Delete all documents:")
        print("   db.articles.deleteMany({})")
        
        # Close connection
        client.close()
        print("\n✓ MongoDB connection closed successfully!")
        
    except pymongo.errors.ConnectionFailure as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MongoDB is running")
        print("2. Check if the connection string is correct")
        print("3. For MongoDB Atlas, ensure your IP is whitelisted")
        return False
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    return True

def show_mongodb_atlas_setup():
    """Show instructions for MongoDB Atlas setup"""
    print("\n" + "=" * 60)
    print("MONGODB ATLAS SETUP INSTRUCTIONS")
    print("=" * 60)
    
    print("""
1. Go to https://cloud.mongodb.com/
2. Create a free account or sign in
3. Create a new cluster (free tier available)
4. Go to Database Access:
   - Add New Database User
   - Set username and password
   - Set role to "Atlas admin" or "Read and write to any database"
5. Go to Network Access:
   - Add IP Address
   - Add Current IP Address (or 0.0.0.0/0 for all IPs)
6. Go to Database:
   - Click "Connect"
   - Choose "Connect your application"
   - Copy the connection string
7. Update mongodb_config.py with your connection string:
   MONGO_URI = 'mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority'
""")

if __name__ == "__main__":
    success = test_mongodb_connection()
    
    if not success:
        show_mongodb_atlas_setup()

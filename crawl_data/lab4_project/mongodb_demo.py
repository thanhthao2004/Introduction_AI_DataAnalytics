#!/usr/bin/env python3
"""
MongoDB Demo Script - Demonstrates CRUD operations on ChanhTuoi data
Based on the MongoDB guide provided
"""

import pymongo
from datetime import datetime
import json

def connect_to_mongodb():
    """Connect to MongoDB and return collection"""
    MONGO_URI = 'mongodb://localhost:27017'
    MONGO_DATABASE = 'chanhtuoi_db'
    MONGO_COLLECTION = 'articles'
    
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]
    
    return client, collection

def demo_mongodb_operations():
    """Demonstrate MongoDB operations as shown in the guide"""
    print("=" * 60)
    print("MONGODB OPERATIONS DEMO")
    print("=" * 60)
    
    client, collection = connect_to_mongodb()
    
    try:
        # 1) Liệt kê tất cả dữ liệu
        print("\n1) Liệt kê tất cả dữ liệu:")
        print("   db.articles.find()")
        all_docs = list(collection.find())
        print(f"   Kết quả: {len(all_docs)} documents")
        for i, doc in enumerate(all_docs, 1):
            print(f"   Document {i}: {doc.get('title', 'No title')}")
        
        # 2) Liệt kê giới hạn phạm vi dữ liệu
        print("\n2) Liệt kê giới hạn phạm vi dữ liệu:")
        print("   db.articles.find().limit(1)")
        limited_docs = list(collection.find().limit(1))
        print(f"   Kết quả: {len(limited_docs)} document")
        if limited_docs:
            print(f"   Document: {limited_docs[0].get('title', 'No title')}")
        
        # 3) Tìm theo id
        print("\n3) Tìm theo id:")
        if all_docs:
            doc_id = all_docs[0]['_id']
            print(f"   db.articles.find({{'_id': ObjectId('{doc_id}')}})")
            found_doc = collection.find_one({'_id': doc_id})
            if found_doc:
                print(f"   Kết quả: {found_doc.get('title', 'No title')}")
        
        # 4) Đếm số lượng documents
        print("\n4) Đếm số lượng documents:")
        print("   db.articles.countDocuments()")
        count = collection.count_documents({})
        print(f"   Kết quả: {count} documents")
        
        # 5) Tạo 1 db chứa 1 dòng dữ liệu
        print("\n5) Tạo 1 db chứa 1 dòng dữ liệu:")
        print("   db.articles.insertOne({...})")
        test_doc = {
            'title': 'Test Article',
            'url': 'https://example.com/test',
            'content': 'This is a test article for demonstration',
            'author': 'Demo User',
            'publish_date': '2025-09-16',
            'category': 'Test',
            'tags': ['test', 'demo'],
            'crawled_at': datetime.now().isoformat(),
            'likes': 1
        }
        
        # Check if test document already exists
        existing = collection.find_one({'url': test_doc['url']})
        if not existing:
            result = collection.insert_one(test_doc)
            print(f"   Kết quả: Inserted document with ID {result.inserted_id}")
        else:
            print(f"   Kết quả: Document already exists with ID {existing['_id']}")
        
        # 6) Tìm dữ liệu với điều kiện
        print("\n6) Tìm dữ liệu với điều kiện:")
        
        # Tìm những dòng có likes >= 1
        print("   db.articles.find({'likes': {$gte: 1}})")
        docs_with_likes = list(collection.find({'likes': {'$gte': 1}}))
        print(f"   Kết quả: {len(docs_with_likes)} documents có likes >= 1")
        
        # Tìm những dòng có likes <= 2
        print("   db.articles.find({'likes': {$lte: 2}})")
        docs_with_likes_lte = list(collection.find({'likes': {'$lte': 2}}))
        print(f"   Kết quả: {len(docs_with_likes_lte)} documents có likes <= 2")
        
        # Tìm những dòng có likes = 1
        print("   db.articles.find({'likes': 1})")
        docs_with_likes_eq = list(collection.find({'likes': 1}))
        print(f"   Kết quả: {len(docs_with_likes_eq)} documents có likes = 1")
        
        # 7) Cập nhật dữ liệu
        print("\n7) Cập nhật dữ liệu:")
        print("   db.articles.updateOne({'likes': 1}, {$set: {'updated': true}})")
        update_result = collection.update_one(
            {'likes': 1}, 
            {'$set': {'updated': True, 'updated_at': datetime.now().isoformat()}}
        )
        print(f"   Kết quả: Updated {update_result.modified_count} document(s)")
        
        # 8) Xóa dữ liệu (demo - không thực sự xóa)
        print("\n8) Xóa dữ liệu (demo - không thực sự xóa):")
        print("   db.articles.deleteOne({'url': 'https://example.com/test'})")
        # Uncomment the line below to actually delete
        # delete_result = collection.delete_one({'url': 'https://example.com/test'})
        # print(f"   Kết quả: Deleted {delete_result.deleted_count} document(s)")
        print("   Kết quả: Demo mode - no actual deletion performed")
        
        # Show final count
        final_count = collection.count_documents({})
        print(f"\nTổng số documents hiện tại: {final_count}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def show_advanced_queries():
    """Show advanced MongoDB queries for ChanhTuoi data"""
    print("\n" + "=" * 60)
    print("ADVANCED MONGODB QUERIES FOR CHANHTUOI DATA")
    print("=" * 60)
    
    client, collection = connect_to_mongodb()
    
    try:
        # Find articles with specific keywords in title
        print("\n1. Tìm bài viết có từ khóa trong tiêu đề:")
        print("   db.articles.find({'title': /Chanh/i})")
        chanh_articles = list(collection.find({'title': {'$regex': 'Chanh', '$options': 'i'}}))
        print(f"   Kết quả: {len(chanh_articles)} bài viết")
        
        # Find articles with content length > 1000 characters
        print("\n2. Tìm bài viết có nội dung dài hơn 1000 ký tự:")
        print("   db.articles.find({$expr: {$gt: [{$strLenCP: '$content'}, 1000]}})")
        long_articles = list(collection.find({
            '$expr': {'$gt': [{'$strLenCP': '$content'}, 1000]}
        }))
        print(f"   Kết quả: {len(long_articles)} bài viết")
        
        # Group by category
        print("\n3. Nhóm theo category:")
        print("   db.articles.aggregate([{$group: {_id: '$category', count: {$sum: 1}}}])")
        category_stats = list(collection.aggregate([
            {'$group': {'_id': '$category', 'count': {'$sum': 1}}}
        ]))
        for stat in category_stats:
            print(f"   {stat['_id'] or 'No category'}: {stat['count']} bài viết")
        
        # Find articles crawled today
        print("\n4. Tìm bài viết được crawl hôm nay:")
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"   db.articles.find({{'crawled_at': /{today}/}})")
        today_articles = list(collection.find({'crawled_at': {'$regex': today}}))
        print(f"   Kết quả: {len(today_articles)} bài viết")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    demo_mongodb_operations()
    show_advanced_queries()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED!")
    print("=" * 60)
    print("Bạn có thể sử dụng MongoDB Compass hoặc mongo shell để thực hiện các truy vấn này.")
    print("Hoặc sử dụng Python với PyMongo như trong script này.")

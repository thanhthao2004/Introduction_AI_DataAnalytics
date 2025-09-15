#!/usr/bin/env python3
"""
Script to run ChanhTuoi crawler
Usage: python3 run_chanhtuoi_crawler.py
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    """Main function to run the crawler"""
    print("=" * 60)
    print("CHANHTUOI CRAWLER")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('scrapy.cfg'):
        print("Error: scrapy.cfg not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if MongoDB is available (optional)
    try:
        import pymongo
        print("✓ PyMongo is installed")
    except ImportError:
        print("⚠ PyMongo not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pymongo'])
        print("✓ PyMongo installed")
    
    print()
    print("Starting ChanhTuoi crawler...")
    print("This will crawl articles from chanhtuoi.com and save them to MongoDB")
    print()
    
    # Run the crawler
    try:
        cmd = [
            sys.executable, '-m', 'scrapy', 'crawl', 'chanhtuoi',
            '-L', 'INFO'  # Set log level to INFO
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        print()
        
        result = subprocess.run(cmd, cwd=os.getcwd())
        
        if result.returncode == 0:
            print()
            print("=" * 60)
            print("CRAWLER COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            print("Next steps:")
            print("1. Check your MongoDB database 'chanhtuoi_db' collection 'articles'")
            print("2. Use MongoDB Compass or mongo shell to view the data")
            print("3. Run MongoDB queries to analyze the crawled data")
        else:
            print()
            print("=" * 60)
            print("CRAWLER FAILED!")
            print("=" * 60)
            print("Please check the error messages above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print()
        print("Crawler interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running crawler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

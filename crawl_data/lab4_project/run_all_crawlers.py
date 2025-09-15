#!/usr/bin/env python3
"""
Script to run all crawlers in the Lab4 project
Usage: python3 run_all_crawlers.py
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def run_command(command, description, cwd=None):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        if cwd:
            result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ SUCCESS!")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("✗ FAILED!")
            if result.stderr:
                print("Error:")
                print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    """Main function to run all crawlers"""
    print("=" * 80)
    print("LAB4 PROJECT - RUNNING ALL CRAWLERS")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('scrapy.cfg'):
        print("Error: scrapy.cfg not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    results = {}
    
    # 1. ChanhTuoi Crawler
    results['chanhtuoi'] = run_command(
        "python3 run_chanhtuoi_crawler.py",
        "1. CHANHTUOI CRAWLER"
    )
    
    # 2. Jobs Crawler
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results['jobs'] = run_command(
        f"scrapy crawl jobs -o jobs_output_{timestamp}.json",
        "2. JOBS CRAWLER (VietnamWorks + FPTJobs)"
    )
    
    # 3. IT Courses Crawler
    results['courses'] = run_command(
        "python3 selenium_scraper_it_courses.py --query 'information technology' --per-site 20 --headless",
        "3. IT COURSES CRAWLER",
        cwd="lab4_project/spiders"
    )
    
    # 4. Test MongoDB Connection
    results['mongodb_test'] = run_command(
        "python3 test_mongodb.py",
        "4. TESTING MONGODB CONNECTION"
    )
    
    # 5. Demo MongoDB Operations
    results['mongodb_demo'] = run_command(
        "python3 mongodb_demo.py",
        "5. DEMO MONGODB OPERATIONS"
    )
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print(f"Results: {success_count}/{total_count} crawlers completed successfully")
    print()
    
    for name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {name.replace('_', ' ').title()}: {status}")
    
    print()
    print("Output files:")
    print("- ChanhTuoi data: MongoDB database 'chanhtuoi_db' collection 'articles'")
    print("- Jobs data: jobs_output_*.json files")
    print("- IT Courses data: it_courses_*.csv files in lab4_project/spiders/")
    print()
    
    if success_count == total_count:
        print("🎉 All crawlers completed successfully!")
        print()
        print("Next steps:")
        print("1. Check MongoDB for ChanhTuoi articles")
        print("2. Review JSON files for jobs data")
        print("3. Review CSV files for IT courses data")
        print("4. Use MongoDB queries to analyze the data")
        print("5. Run data analysis scripts on the collected data")
    else:
        print("⚠️  Some crawlers failed. Please check the error messages above.")
        print("You can run individual crawlers:")
        print("  python3 run_chanhtuoi_crawler.py")
        print("  scrapy crawl jobs")
        print("  cd lab4_project/spiders && python3 selenium_scraper_it_courses.py --query 'programming' --per-site 20 --headless")

if __name__ == "__main__":
    main()

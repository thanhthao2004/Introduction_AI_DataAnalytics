#!/bin/bash

# Script to run all crawlers in the Lab4 project
# Usage: ./run_all_crawlers.sh

echo "============================================================"
echo "LAB4 PROJECT - RUNNING ALL CRAWLERS"
echo "============================================================"
echo "Started at: $(date)"
echo ""

# Check if we're in the right directory
if [ ! -f "scrapy.cfg" ]; then
    echo "Error: scrapy.cfg not found. Please run this script from the project root directory."
    exit 1
fi

# Function to run crawler with error handling
run_crawler() {
    local crawler_name=$1
    local command=$2
    local output_file=$3
    
    echo "Starting $crawler_name..."
    echo "Command: $command"
    echo ""
    
    if eval "$command"; then
        echo "✓ $crawler_name completed successfully!"
        if [ -n "$output_file" ] && [ -f "$output_file" ]; then
            echo "  Output saved to: $output_file"
        fi
    else
        echo "✗ $crawler_name failed!"
        echo "  Please check the error messages above."
    fi
    echo ""
}

# 1. ChanhTuoi Crawler
echo "1. CHANHTUOI CRAWLER"
echo "==================="
run_crawler "ChanhTuoi Crawler" "python3 run_chanhtuoi_crawler.py"

# 2. Jobs Crawler
echo "2. JOBS CRAWLER (VietnamWorks + FPTJobs)"
echo "========================================"
run_crawler "Jobs Crawler" "scrapy crawl jobs -o jobs_output_$(date +%Y%m%d_%H%M%S).json" "jobs_output_*.json"

# 3. IT Courses Crawler
echo "3. IT COURSES CRAWLER"
echo "====================="
echo "Changing to spiders directory..."
cd lab4_project/spiders

run_crawler "IT Courses Crawler" "python3 selenium_scraper_it_courses.py --query 'information technology' --per-site 20 --headless" "it_courses_*.csv"

echo "Returning to project root..."
cd ../..

# 4. Test MongoDB Connection
echo "4. TESTING MONGODB CONNECTION"
echo "============================="
run_crawler "MongoDB Test" "python3 test_mongodb.py"

# 5. Demo MongoDB Operations
echo "5. DEMO MONGODB OPERATIONS"
echo "=========================="
run_crawler "MongoDB Demo" "python3 mongodb_demo.py"

echo "============================================================"
echo "ALL CRAWLERS COMPLETED!"
echo "============================================================"
echo "Finished at: $(date)"
echo ""
echo "Summary of outputs:"
echo "- ChanhTuoi data: MongoDB database 'chanhtuoi_db' collection 'articles'"
echo "- Jobs data: jobs_output_*.json files"
echo "- IT Courses data: it_courses_*.csv files in lab4_project/spiders/"
echo "- MongoDB test and demo: Check console output above"
echo ""
echo "Next steps:"
echo "1. Check MongoDB for ChanhTuoi articles"
echo "2. Review JSON files for jobs data"
echo "3. Review CSV files for IT courses data"
echo "4. Use MongoDB queries to analyze the data"
echo "5. Run data analysis scripts on the collected data"

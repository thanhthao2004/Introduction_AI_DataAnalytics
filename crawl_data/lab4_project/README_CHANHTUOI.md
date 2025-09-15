# Lab4 Project - Web Crawling với MongoDB

Dự án này bao gồm 3 crawler chính:
1. **ChanhTuoi Crawler** - Crawl dữ liệu từ website ChanhTuoi và lưu trữ vào MongoDB
2. **Jobs Crawler** - Crawl việc làm từ VietnamWorks và FPTJobs
3. **IT Courses Crawler** - Crawl khóa học IT từ Edumall, Coursera, edX, DataCamp

Thực hiện theo hướng dẫn MongoDB + Syntax và hướng dẫn Crawl ChanhTuoi.

## Cấu trúc Project

```
lab4_project/
├── lab4_project/                                  # Scrapy project core
│   ├── spiders/
│   │   ├── chanhtuoi_spider.py                    # Spider crawl ChanhTuoi
│   │   ├── selenium_jobs_vietnamworks_fptjobs.py  # Spider crawl việc làm
│   │   ├── selenium_scraper_it_courses.py         # Spider crawl khóa học IT
│   │   └── it_courses.csv                         # Dữ liệu khóa học mẫu
│   ├── items.py                                   # Định nghĩa các Item classes
│   ├── pipelines.py                               # MongoDB pipeline và duplicate filter
│   ├── middlewares.py                             # Selenium middleware
│   └── settings.py                                # Cấu hình Scrapy và MongoDB
├── run_chanhtuoi_crawler.py                       # Script chạy ChanhTuoi crawler
├── run_all_crawlers.py                            # Script chạy tất cả crawlers (Python)
├── run_all_crawlers.sh                            # Script chạy tất cả crawlers (Bash)
├── test_mongodb.py                                # Test kết nối MongoDB
├── mongodb_demo.py                                # Demo các thao tác MongoDB
├── mongodb_config.py                              # Cấu hình MongoDB
├── scrapy.cfg                                     # Scrapy configuration
└── README_CHANHTUOI.md                            # File này
```

## Cài đặt

### 1. Cài đặt Dependencies

```bash
# Cài đặt các package cần thiết
pip3 install scrapy pymongo selenium pandas webdriver-manager

# Hoặc cài đặt từng package
pip3 install scrapy
pip3 install pymongo
pip3 install selenium
pip3 install pandas
pip3 install webdriver-manager
```

### 2. Cấu hình MongoDB

#### Option A: MongoDB Local
```bash
# Cài đặt MongoDB local
brew install mongodb-community
brew services start mongodb-community
```

#### Option B: MongoDB Atlas (Khuyến nghị)
1. Tạo tài khoản tại https://cloud.mongodb.com/
2. Tạo cluster miễn phí
3. Tạo database user với quyền admin
4. Thêm IP address hiện tại vào Network Access
5. Lấy connection string và cập nhật trong `mongodb_config.py`

## Sử dụng

### 1. ChanhTuoi Crawler

#### Cách 1: Sử dụng script tự động
```bash
python3 run_chanhtuoi_crawler.py
```

#### Cách 2: Chạy trực tiếp với Scrapy
```bash
scrapy crawl chanhtuoi
```

#### Cách 3: Chạy với output file
```bash
scrapy crawl chanhtuoi -o chanhtuoi_data.json
scrapy crawl chanhtuoi -o chanhtuoi_data.csv
```

### 2. Jobs Crawler (VietnamWorks + FPTJobs)

#### Cách 1: Chạy với Scrapy
```bash
scrapy crawl jobs
```

#### Cách 2: Chạy với output file
```bash
scrapy crawl jobs -o jobs_data.json
scrapy crawl jobs -o jobs_data.csv
```

#### Cách 3: Chạy với Selenium (headless)
```bash
scrapy crawl jobs -s SELENIUM_HEADLESS=True
```

### 3. IT Courses Crawler

#### Cách 1: Chạy script Python trực tiếp
```bash
cd lab4_project/spiders
python3 selenium_scraper_it_courses.py --query "information technology" --per-site 40 --headless
```

#### Cách 2: Chạy với các tham số khác nhau
```bash
# Crawl với query cụ thể
python3 selenium_scraper_it_courses.py --query "python programming" --per-site 20

# Crawl không headless (hiển thị browser)
python3 selenium_scraper_it_courses.py --query "data science" --per-site 30 --no-headless

# Crawl tất cả platforms
python3 selenium_scraper_it_courses.py --query "machine learning" --per-site 50 --headless
```

#### Cách 3: Chạy với Scrapy (nếu có spider)
```bash
scrapy crawl it_courses
```

### 4. Test và Demo

#### Test MongoDB Connection
```bash
python3 test_mongodb.py
```

#### Demo MongoDB Operations
```bash
python3 mongodb_demo.py
```

### 5. Chạy tất cả crawlers

#### Cách 1: Sử dụng script Python (Khuyến nghị)
```bash
python3 run_all_crawlers.py
```

#### Cách 2: Sử dụng script Bash
```bash
./run_all_crawlers.sh
```

#### Cách 3: Chạy từng crawler riêng biệt
```bash
# ChanhTuoi
python3 run_chanhtuoi_crawler.py

# Jobs
scrapy crawl jobs

# IT Courses
cd lab4_project/spiders
python3 selenium_scraper_it_courses.py --query "programming" --per-site 30 --headless
```

#### Cách 4: Chạy với output files cụ thể
```bash
# ChanhTuoi với JSON output
scrapy crawl chanhtuoi -o chanhtuoi_data.json

# Jobs với CSV output
scrapy crawl jobs -o jobs_data.csv

# IT Courses với custom parameters
cd lab4_project/spiders
python3 selenium_scraper_it_courses.py --query "python programming" --per-site 50 --headless
```

## Các thao tác MongoDB

### 1. Liệt kê tất cả dữ liệu
```javascript
db.articles.find()
```

### 2. Liệt kê giới hạn phạm vi dữ liệu
```javascript
db.articles.find().limit(1)
```

### 3. Tìm theo ID
```javascript
db.articles.find({'_id': ObjectId('68c8481b46c6ac84ef8a4481')})
```

### 4. Đếm số lượng documents
```javascript
db.articles.countDocuments()
```

### 5. Tìm dữ liệu với điều kiện
```javascript
// Tìm những dòng có likes >= 1
db.articles.find({'likes': {$gte: 1}})

// Tìm những dòng có likes <= 2
db.articles.find({'likes': {$lte: 2}})

// Tìm những dòng có likes = 1
db.articles.find({'likes': 1})
```

### 6. Cập nhật dữ liệu
```javascript
db.articles.updateOne({'likes': 1}, {$set: {'updated': true}})
```

### 7. Xóa dữ liệu
```javascript
// Xóa 1 document
db.articles.deleteOne({'url': 'article_url'})

// Xóa tất cả documents
db.articles.deleteMany({})
```

## Cấu trúc dữ liệu

### 1. ChanhTuoi Articles (MongoDB Collection: `articles`)

```json
{
  "_id": ObjectId("..."),
  "title": "Tiêu đề bài viết",
  "url": "https://chanhtuoi.com/article-url",
  "content": "Nội dung bài viết...",
  "author": "Tác giả",
  "publish_date": "Ngày xuất bản",
  "category": "Danh mục",
  "tags": ["tag1", "tag2"],
  "image_url": "URL hình ảnh",
  "summary": "Tóm tắt bài viết...",
  "crawled_at": "2025-09-16T00:08:43.372129",
  "saved_at": "2025-09-16T00:08:43.372129"
}
```

### 2. Jobs Data (Files: `jobs.csv`, `jobs_improved.json`)

```json
{
  "job_title": "Senior Python Developer",
  "company": "ABC Company",
  "location": "Ho Chi Minh City",
  "salary": "20-30 triệu",
  "experience": "3-5 năm",
  "skills": ["Python", "Django", "PostgreSQL"],
  "job_url": "https://vietnamworks.com/job/12345",
  "source": "vietnamworks.com",
  "crawled_at": "2025-09-16T00:08:43.372129"
}
```

### 3. IT Courses Data (Files: `it_courses.csv`, `courses_improved.csv`)

```json
{
  "platform": "Coursera",
  "course_name": "Python for Data Science",
  "instructor": "Dr. John Smith",
  "time_info": "4 weeks, 3-5 hours/week",
  "outcomes": "Learn Python programming for data analysis",
  "course_link": "https://coursera.org/learn/python-data-science",
  "learning_mode": "Self-paced",
  "price": "$49/month",
  "rating": "4.8",
  "crawled_at": "2025-09-16T00:08:43.372129"
}
```

### 4. Edumall Data (File: `edumall_better.json`)

```json
{
  "course_name": "Lập trình Python từ cơ bản đến nâng cao",
  "instructor": "Nguyễn Văn A",
  "price": "299,000 VNĐ",
  "rating": "4.5",
  "students": "1,234 học viên",
  "duration": "20 giờ",
  "level": "Cơ bản",
  "course_url": "https://edumall.vn/course/python-basic",
  "description": "Khóa học Python toàn diện...",
  "crawled_at": "2025-09-16T00:08:43.372129"
}
```

## Troubleshooting

### 1. Lỗi kết nối MongoDB
- Kiểm tra MongoDB có đang chạy không
- Kiểm tra connection string trong `mongodb_config.py`
- Với MongoDB Atlas, đảm bảo IP address được whitelist

### 2. ChanhTuoi Crawler Issues
- Website có thể đã thay đổi cấu trúc HTML
- Cần cập nhật CSS selectors trong `chanhtuoi_spider.py`
- Kiểm tra robots.txt của website

### 3. Jobs Crawler Issues
- VietnamWorks/FPTJobs có thể có anti-bot protection
- Cần tăng delay giữa các request
- Kiểm tra Selenium middleware hoạt động

### 4. IT Courses Crawler Issues
- Lỗi Selenium: Cài đặt ChromeDriver
- Cập nhật Chrome browser
- Kiểm tra network connection
- Một số website có thể block automated requests

### 5. Lỗi chung
- Kiểm tra internet connection
- Cài đặt đầy đủ dependencies
- Kiểm tra Python version (3.9+ recommended)

## Kết quả

Sau khi chạy thành công, bạn sẽ có:

### ChanhTuoi Crawler
- Dữ liệu được crawl từ ChanhTuoi lưu trong MongoDB
- File JSON backup (nếu cấu hình FEEDS)
- Log chi tiết về quá trình crawl

### Jobs Crawler
- File `jobs_output_*.json` với dữ liệu việc làm từ VietnamWorks và FPTJobs
- Thông tin chi tiết về job title, company, location, salary, skills
- Dữ liệu được lưu theo timestamp để tránh ghi đè

### IT Courses Crawler
- File `it_courses_*.csv` với dữ liệu khóa học IT
- Thông tin về platform, course name, instructor, price, rating
- Dữ liệu được lưu theo timestamp để tránh ghi đè

## Examples và Use Cases

### 1. Phân tích dữ liệu việc làm
```python
import pandas as pd
import json
import glob

# Đọc dữ liệu việc làm từ file JSON mới nhất
jobs_files = glob.glob('jobs_output_*.json')
if jobs_files:
    latest_jobs_file = max(jobs_files)
    with open(latest_jobs_file, 'r', encoding='utf-8') as f:
        jobs_data = json.load(f)
    
    jobs_df = pd.DataFrame(jobs_data)
    print(f"Tổng số việc làm: {len(jobs_df)}")
    print(f"Top 5 công ty tuyển dụng nhiều nhất:")
    print(jobs_df['company'].value_counts().head())
    
    # Phân tích lương
    print(f"Phân bố lương:")
    print(jobs_df['salary'].value_counts())
```

### 2. Phân tích khóa học IT
```python
import glob

# Đọc dữ liệu khóa học từ file CSV mới nhất
courses_files = glob.glob('lab4_project/spiders/it_courses_*.csv')
if courses_files:
    latest_courses_file = max(courses_files)
    courses_df = pd.read_csv(latest_courses_file)
    
    print(f"Tổng số khóa học: {len(courses_df)}")
    print(f"Phân bố theo platform:")
    print(courses_df['platform'].value_counts())
    
    # Tìm khóa học Python
    python_courses = courses_df[courses_df['course_name'].str.contains('Python', case=False, na=False)]
    print(f"Số khóa học Python: {len(python_courses)}")
```

### 3. Truy vấn MongoDB
```python
import pymongo

# Kết nối MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['chanhtuoi_db']
collection = db['articles']

# Tìm bài viết có từ khóa
articles = list(collection.find({'title': {'$regex': 'Chanh', '$options': 'i'}}))
print(f"Số bài viết về Chanh: {len(articles)}")

# Thống kê theo tác giả
pipeline = [
    {'$group': {'_id': '$author', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}}
]
author_stats = list(collection.aggregate(pipeline))
print("Top tác giả:")
for stat in author_stats[:5]:
    print(f"  {stat['_id']}: {stat['count']} bài viết")
```

## Mở rộng

Để mở rộng project:
1. Thêm các website khác vào `allowed_domains`
2. Cập nhật CSS selectors cho từng website
3. Thêm các field mới vào Item classes
4. Tạo pipeline xử lý dữ liệu khác (cleaning, analysis, etc.)
5. Tích hợp với các database khác (PostgreSQL, MySQL)
6. Tạo API để truy cập dữ liệu
7. Xây dựng dashboard để visualize dữ liệu

## Liên hệ và Hỗ trợ

Nếu có vấn đề, hãy kiểm tra:
1. Log của Scrapy
2. MongoDB connection
3. Network connectivity
4. Website structure changes
5. Dependencies installation
6. Python version compatibility

## Changelog

- **v1.0**: ChanhTuoi crawler với MongoDB integration
- **v1.1**: Thêm Jobs crawler (VietnamWorks + FPTJobs)
- **v1.2**: Thêm IT Courses crawler với Selenium
- **v1.3**: Cải thiện data processing và output formats

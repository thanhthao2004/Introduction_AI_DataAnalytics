import scrapy
from datetime import datetime
from urllib.parse import urljoin
from lab4_project.items import ChanhTuoiItem
import re


class ChanhTuoiSpider(scrapy.Spider):
    name = 'chanhtuoi'
    allowed_domains = ['chanhtuoi.com']
    start_urls = ['https://chanhtuoi.com/']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """Parse the main page to find article links"""
        self.logger.info(f'Parsing main page: {response.url}')
        
        # Find article links - try different selectors
        article_links = []
        
        # Try different selectors for article links
        selectors = [
            'article a::attr(href)',
            '.post-title a::attr(href)',
            '.entry-title a::attr(href)',
            'h2 a::attr(href)',
            'h3 a::attr(href)',
            '.title a::attr(href)',
            'a[href*="/bai-viet/"]::attr(href)',
            'a[href*="/tin-tuc/"]::attr(href)',
            'a[href*="/article/"]::attr(href)',
        ]
        
        for selector in selectors:
            links = response.css(selector).getall()
            if links:
                article_links.extend(links)
                self.logger.info(f'Found {len(links)} links with selector: {selector}')
        
        # Remove duplicates and convert to absolute URLs
        article_links = list(set(article_links))
        for link in article_links[:20]:  # Limit to first 20 articles for testing
            if link and not link.startswith('http'):
                link = urljoin(response.url, link)
            if 'chanhtuoi.com' in link and link not in self.start_urls:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_article,
                    meta={'original_url': link}
                )
        
        # Look for pagination
        next_page = response.css('a.next::attr(href)').get()
        if not next_page:
            next_page = response.css('.pagination a:last-child::attr(href)').get()
        if not next_page:
            next_page = response.css('a[rel="next"]::attr(href)').get()
            
        if next_page:
            next_page = urljoin(response.url, next_page)
            yield scrapy.Request(
                url=next_page,
                callback=self.parse
            )

    def parse_article(self, response):
        """Parse individual article page"""
        self.logger.info(f'Parsing article: {response.url}')
        
        item = ChanhTuoiItem()
        
        # Extract title
        title_selectors = [
            'h1::text',
            '.post-title::text',
            '.entry-title::text',
            '.article-title::text',
            'title::text',
        ]
        
        for selector in title_selectors:
            title = response.css(selector).get()
            if title:
                item['title'] = title.strip()
                break
        
        # Extract content
        content_selectors = [
            '.post-content',
            '.entry-content',
            '.article-content',
            '.content',
            'article',
        ]
        
        content = ""
        for selector in content_selectors:
            content_elements = response.css(f'{selector} p::text').getall()
            if content_elements:
                content = ' '.join([p.strip() for p in content_elements if p.strip()])
                break
        
        if not content:
            # Fallback: get all text from body
            content = ' '.join(response.css('body p::text').getall())
        
        item['content'] = content.strip()
        
        # Extract author
        author_selectors = [
            '.author::text',
            '.post-author::text',
            '.by-author::text',
            '[rel="author"]::text',
        ]
        
        for selector in author_selectors:
            author = response.css(selector).get()
            if author:
                item['author'] = author.strip()
                break
        
        # Extract publish date
        date_selectors = [
            '.date::text',
            '.post-date::text',
            '.published::text',
            'time::text',
            '[datetime]::attr(datetime)',
        ]
        
        for selector in date_selectors:
            date = response.css(selector).get()
            if date:
                item['publish_date'] = date.strip()
                break
        
        # Extract category
        category_selectors = [
            '.category::text',
            '.post-category::text',
            '.breadcrumb a:last-child::text',
        ]
        
        for selector in category_selectors:
            category = response.css(selector).get()
            if category:
                item['category'] = category.strip()
                break
        
        # Extract tags
        tags = response.css('.tags a::text').getall()
        if not tags:
            tags = response.css('.tag::text').getall()
        item['tags'] = [tag.strip() for tag in tags if tag.strip()]
        
        # Extract image
        image_selectors = [
            '.post-thumbnail img::attr(src)',
            '.featured-image img::attr(src)',
            'article img:first-child::attr(src)',
            '.content img:first-child::attr(src)',
        ]
        
        for selector in image_selectors:
            image = response.css(selector).get()
            if image:
                item['image_url'] = urljoin(response.url, image)
                break
        
        # Create summary from first 200 characters of content
        if content:
            item['summary'] = content[:200] + '...' if len(content) > 200 else content
        
        # Set other fields
        item['url'] = response.url
        item['crawled_at'] = datetime.now().isoformat()
        
        # Only yield if we have at least title and content
        if item.get('title') and item.get('content'):
            yield item
        else:
            self.logger.warning(f'Incomplete article data for {response.url}')
            # Log the page structure for debugging
            self.logger.debug(f'Page structure: {response.css("*").getall()[:10]}')

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Lab4ProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ChanhTuoiItem(scrapy.Item):
    """Item class for ChanhTuoi articles"""
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    image_url = scrapy.Field()
    summary = scrapy.Field()
    crawled_at = scrapy.Field()

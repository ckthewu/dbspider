# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DbgroupspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    groupname = scrapy.Field()
    groupid = scrapy.Field()
    membersnum = scrapy.Field()
    tags = scrapy.Field()
    bdgroupsid = scrapy.Field()


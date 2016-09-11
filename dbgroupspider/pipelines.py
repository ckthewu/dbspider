# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json,codecs

from scrapy.exceptions import DropItem


class DbgroupspiderPipeline(object):
    groups_to_filter = set()

    def __init__(self):
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if item['groupname'] in self.groups_to_filter:
            raise DropItem("Group already been crwaled")
        else:
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line.decode("unicode_escape"))
            self.groups_to_filter.add(item['groupname'])
            return item
    def spider_closed(self, spider):
        self.file.close()

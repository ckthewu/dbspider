# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json,codecs,re

from scrapy.exceptions import DropItem


class DbgroupspiderPipeline(object):

    def __init__(self):
        f = codecs.open('/home/ckthewu/scrapyproject/dbgroupspider/scraped_data_utf8.json', 'r', encoding='utf-8')
        gpid = re.findall(r'"groupid": "([^\"]+)"?',f.read())
        f.close()
        self.groups_to_filter = set(gpid)
        print "-------------------------------------------------\n\n\n"
        print "filter_group_count=%s" % len(self.groups_to_filter)
        print "\n\n\n-------------------------------------------------"

        self.file = codecs.open('scraped_data_utf8.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        if item['groupid'] in self.groups_to_filter:
            raise DropItem("Group already been crwaled")
        else:
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line.decode("unicode_escape"))
            self.groups_to_filter.add(item['groupid'])
            return item
    def spider_closed(self, spider):
        self.file.close()

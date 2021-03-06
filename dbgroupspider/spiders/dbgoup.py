# -*- coding: utf-8 -*-
import codecs,json

from scrapy.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
from scrapy import Request
from scrapy.selector import HtmlXPathSelector
import re
from dbgroupspider.items import DbgroupspiderItem
class DbgSpider(scrapy.Spider):
    def start_requests(self):
        yield Request("http://www.douban.com/group/ps-camp/",headers={'User-Agent': "215112855@qq.com"})
    name = 'dbgroup'
    allowed_domains =['www.douban.com/group/']
    # start_urls = [
    # "https://www.douban.com/group/litterature/","https://www.douban.com/group/yunnantour/","https://www.douban.com/group/dota22/",
    # "https://www.douban.com/group/toufa/","https://www.douban.com/group/DiyGril/","https://www.douban.com/group/ps-camp/",
    # ]
    start_urls = ["https://www.douban.com/group/ps-camp/",]
    mnre = re.compile(r'\((\d+)\)')
    def parse(self, response):
        groupname = response.xpath('/html/head/title/text()').extract()[0].strip()
        groupurl = response.xpath('//div[@class="rec-sec"]/span/a/@data-href').extract()[0]
        membersnum = int(self.mnre.findall(str(response.xpath('//div[@class="mod side-nav"]/p/a/text()').extract()))[0])
        tags = response.xpath('//div[@class="group-tags"]/a/text()').extract()
        bdgs = response.xpath\
            ('//div[@class="bd"]//div[@class="group-list"]//div[@class="group-list-item"]/div[@class="title"]/a')
        bdgroups = []
        for bdg in bdgs:
            bdgroup = {'bdgroupname':bdg.xpath('@title').extract()[0],'bdgroupurl':bdg.xpath('@href').extract()[0]}
            bdgroups.append(bdgroup)

        # print groupname,groupurl,membersnum,tags,bdgoups
        item = DbgroupspiderItem()
        item['groupname'] = groupname
        item['groupurl'] = groupurl
        item['membersnum'] = membersnum
        item['tags'] = tags
        item['bdgroups'] = bdgroups
        return item

class DbgCrawlSpider(CrawlSpider):
    name = 'dbspider'
    allowed_domains =['www.douban.com']
    start_urls = [
        "https://www.douban.com/group/explore/culture",
        "https://www.douban.com/group/explore/travel",
        "https://www.douban.com/group/explore/ent",
        "https://www.douban.com/group/explore/fashion",
        "https://www.douban.com/group/explore/life",
        "https://www.douban.com/group/explore/tech",
    ]
    # start_urls = ["https://www.douban.com/group/ps-camp/",]

    mnre = re.compile(r'\((\d+)\)')
    idre = re.compile(r'group/([^/]+)/$')


    rules = [
        Rule(SgmlLinkExtractor(allow=('/group/[^/]+/$',)), callback='parse_group'),
        Rule(SgmlLinkExtractor(allow=('/group/explore',)), follow=True),
    ]

    # file = codecs.open('/home/ckthewu/scrapyproject/dbgroupspider/scraped_data_utf8.json', 'r', encoding='utf-8')
    # gpid = re.findall(r'"groupid": "([^\"]+)"?',file.read())
    # filter_group = set(gpid)
    # print "-------------------------------------------------\n\n\n"
    # print "filter_group_count=%s" % len(filter_group)
    # print "\n\n\n-------------------------------------------------"

    def parse_group(self,response):
        # response.request.headers.get('Referrer', None)
        x = HtmlXPathSelector(response)
        membersnum = int(self.mnre.findall(str(x.select('//div[@class="mod side-nav"]/p/a/text()').extract()))[0])
        if membersnum>10000:
            groupname = x.select('/html/head/title/text()').extract()[0].strip()[:-2]
            groupid = self.idre.findall(str(x.select('//div[@class="rec-sec"]/span/a/@data-href').extract()[0]))[0]
            tags = x.select('//div[@class="group-tags"]/a/text()').extract()
            bdgs = x.select\
                ('//div[@class="bd"]//div[@class="group-list"]//div[@class="group-list-item"]/div[@class="title"]')
            bdgroupsid = []
            # for bdg in bdgs:
            #     if bdg:
            #         yield Request(bdg.select('a/@href').extract()[0], callback=self.parse_group)
            #         bdgroup = {'bdgroupname':bdg.select('a/@title').extract()[0],'bdgroupurl':bdg.select('a/@href').extract()[0]}
            #         bdgroups.append(bdgroup)

            for bdg in bdgs:
                bdgnum = int(self.mnre.findall(str(bdg.select('span/text()').extract()))[0])
                bdgid = self.idre.findall(str(bdg.select('a/@href').extract()[0]))[0]
                if bdg and bdgnum>10000:
                    bdgroupsid.append(bdgid)
                    yield Request(bdg.select('a/@href').extract()[0], callback=self.parse_group)
                        # bdgroup = {'bdgroupname':bdgnam,'bdgroupurl':bdg.select('a/@href').extract()[0],'bdgroupnum':bdgnum}



            # print groupname,groupurl,membersnum,tags,bdgoups
            item = DbgroupspiderItem()
            item['groupname'] = groupname
            item['groupid'] = groupid
            item['membersnum'] = membersnum
            item['tags'] = tags
            item['bdgroupsid'] = bdgroupsid
            yield item



    # def parse_startrequest(self, response):
    #     yield Request(response.url, headers={'User-Agent': "215112855@qq.com"})
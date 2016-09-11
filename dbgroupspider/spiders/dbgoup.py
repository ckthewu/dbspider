# -*- coding: utf-8 -*-
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
    # start_urls = [
    # "https://www.douban.com/group/litterature/","https://www.douban.com/group/yunnantour/","https://www.douban.com/group/dota22/",
    # "https://www.douban.com/group/toufa/","https://www.douban.com/group/DiyGril/","https://www.douban.com/group/ps-camp/",
    # ]
    start_urls = ["https://www.douban.com/group/ps-camp/",]
    mnre = re.compile(r'\((\d+)\)')
    rules = [
        Rule(SgmlLinkExtractor(allow=('/group/[^/]+/$',)), callback='parse_group'),
        Rule(SgmlLinkExtractor(allow=('/group/explore\?tag',)), follow=True),
    ]
    filter_group = set()
    def parse_group(self,response):
        # response.request.headers.get('Referrer', None)
        x = HtmlXPathSelector(response)
        groupname = x.select('/html/head/title/text()').extract()[0].strip()[:-2]
        groupurl = x.select('//div[@class="rec-sec"]/span/a/@data-href').extract()[0]
        membersnum = int(self.mnre.findall(str(x.select('//div[@class="mod side-nav"]/p/a/text()').extract()))[0])
        tags = x.select('//div[@class="group-tags"]/a/text()').extract()
        bdgs = x.select\
            ('//div[@class="bd"]//div[@class="group-list"]//div[@class="group-list-item"]/div[@class="title"]')
        bdgroups = []
        # for bdg in bdgs:
        #     if bdg:
        #         yield Request(bdg.select('a/@href').extract()[0], callback=self.parse_group)
        #         bdgroup = {'bdgroupname':bdg.select('a/@title').extract()[0],'bdgroupurl':bdg.select('a/@href').extract()[0]}
        #         bdgroups.append(bdgroup)

        for bdg in bdgs:
            bdgnum = int(self.mnre.findall(str(bdg.select('span/text()').extract()))[0])
            bdgnam = bdg.select('a/@title').extract()[0]
            if bdg and bdgnum>100:
                bdgroups.append(bdgnam)
                if (bdgnam not in self.filter_group):
                    yield Request(bdg.select('a/@href').extract()[0], callback=self.parse_group)
                    # bdgroup = {'bdgroupname':bdgnam,'bdgroupurl':bdg.select('a/@href').extract()[0],'bdgroupnum':bdgnum}
                    self.filter_group.add(bdgnam)


        # print groupname,groupurl,membersnum,tags,bdgoups
        item = DbgroupspiderItem()
        item['groupname'] = groupname
        item['groupurl'] = groupurl
        item['membersnum'] = membersnum
        item['tags'] = tags
        item['bdgroups'] = bdgroups
        yield item



    # def parse_startrequest(self, response):
    #     yield Request(response.url, headers={'User-Agent': "215112855@qq.com"})
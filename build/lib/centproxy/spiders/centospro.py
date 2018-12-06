# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

class CentosproSpider(RedisSpider):
    name = 'centospro'
    allowed_domains = ['zhipin.com']
    # start_urls = []
    redis_key = "zhipin"

    def parse(self, response):
        a_list = response.xpath("//div[@class='job-menu']//a/@href").extract()
        for a in a_list:
            yield scrapy.Request("https://www.zhipin.com"+a,callback=self.parse_nxt)

    def parse_nxt(self,response):
        job_li = response.xpath("//div[@class = 'job-list']//li")
        tag = response.xpath("//span[@class = 'label-text']/b/text()").extract_first()
        try:
            for job in job_li:
                item = {}
                item["tag"] = tag
                item["job_title"] = job.xpath(".//div[@class = 'info-primary']//div[@class = 'job-title']/text()").extract_first()
                item["salery"] = job.xpath(".//div[@class = 'info-primary']//span[@class = 'red']/text()").extract_first()
                item["info"]  = " ".join(job.xpath(".//div[@class = 'info-primary']/p/text()").extract())
                item["job_href"] = "https://www.zhipin.com"+job.xpath(".//div[@class = 'info-primary']//a/@href").extract_first()
                item["job_company_name"] = job.xpath(".//div[@class = 'company-text']//a/text()").extract_first()
                item["job_company_href"] = "https://www.zhipin.com"+job.xpath(".//div[@class = 'company-text']//a/@href").extract_first()
                item["job_company_info"] = " ".join(job.xpath(".//div[@class = 'company-text']/p/text()").extract())
                item["job_pub"] = job.xpath(".//div[@class = 'info-publis']/p/text()").extract_first()
                yield scrapy.Request(item["job_href"],callback=self.parse_com,meta = {"item":item},dont_filter=True)
                # yield item
            tmp = response.xpath("//div[@class='job-list']/div[@class='page']/a[last()]/@href").extract_first()
            # print(tmp)
            if tmp is not None:
                nxt_url = 'https://www.zhipin.com' + tmp
                yield scrapy.Request(nxt_url,callback=self.parse_nxt)
        except Exception as e:
            print(e)
            pass

    def parse_com(self,response):
        item = response.meta["item"]
        desc = response.xpath("//div[@class ='job-sec']/div[@class='text']").xpath('string(.)').extract()
        item["desc"] = ''.join(desc).replace(" ","").strip()
        avail = response.xpath("//a[@ka='job-detail-close']/text()").extract_first()
        if avail is None:
            item["if_available"] = "yes"
        else:
            item["if_available"] = avail
        # print(item)
        yield item






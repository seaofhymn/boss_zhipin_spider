# -*- coding: utf-8 -*-
from pymongo import MongoClient
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class CentproxyPipeline(object):
    def process_item(self, item, spider):
        uri = "mongo_uri"
        conn = MongoClient(uri)
        db = conn.zhipin
        my_set.insert(item)
        conn.close()
        return item

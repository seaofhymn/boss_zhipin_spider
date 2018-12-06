# -*- coding: utf-8 -*-
from pymongo import MongoClient

class CentproxyPipeline(object):
    def process_item(self, item, spider):
        uri = "youruri"
        conn = MongoClient(uri)
        db = conn.zhipin
        my_set = db.pin
        my_set.insert(item)
        conn.close()
        return item

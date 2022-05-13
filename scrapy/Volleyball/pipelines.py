# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class VolleyballPipeline:
    
    def __init__(self):
        self.conn = sqlite3.connect('Volleyball.db') # results are going to be stored in Volleyball.db sql database
        self.gen_iter = 0
       

    def process_item(self, item, spider): # Preprocessing and putting to SQL database
        
        item['data'][0]['Sesson'] = item['sesson'][0]
        item['data'][0].to_sql(item['team_name'][0], self.conn, if_exists='append', index=False)
        self.gen_iter += 1
        if self.gen_iter == 100 and bool(item['limit'][0]):
            spider.crawler.engine.close_spider(self, reason='finished')

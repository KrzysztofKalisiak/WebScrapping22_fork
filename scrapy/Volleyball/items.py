# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import pandas as pd
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

def add_ref_path(sub_path):
    return 'https://www.plusliga.pl'+sub_path


class ItemTeam(scrapy.Item): # infomrations on team name and link to all the results from starter page
    team_name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(input_processor=MapCompose(add_ref_path), output_processor=TakeFirst())

class ItemSesson(scrapy.Item): # inforamtion on sesson and link to table with results
    sesson = scrapy.Field()
    link = scrapy.Field()

class ItemStatistic(scrapy.Item): # html table extracted with last parser
    team_name = scrapy.Field()
    sesson = scrapy.Field()
    data = scrapy.Field(input_processor = MapCompose(pd.read_html))
    limit = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Join


class LeagueOfGraphsItem(scrapy.Item):
    match_id = scrapy.Field()
    winner = scrapy.Field()
    team_1 = scrapy.Field()
    team_2 = scrapy.Field()


class LeagueOfGraphsLoader(ItemLoader):
    match_id_out = TakeFirst()
    winner_out = TakeFirst()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicMessageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    漫画名 = scrapy.Field()             #名
    点击量 = scrapy.Field()         #总点击
    月投票 = scrapy.Field()    #总月票
    介绍 = scrapy.Field()     #文字的介绍
    pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HcrecipesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    recipe_title = scrapy.Field()
    recipe_cover = scrapy.Field()
    recipe_views = scrapy.Field()
    recipe_collection = scrapy.Field()
    recipe_materials = scrapy.Field()
    recipe_steps = scrapy.Field()
    recipe_hasvideo = scrapy.Field()
    recipe_videosrc = scrapy.Field()


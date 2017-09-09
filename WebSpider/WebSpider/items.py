#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    year = scrapy.Field()
    link=scrapy.Field()
    tomatometer=scrapy.Field()
    audience_score=scrapy.Field()
    runtime=scrapy.Field()
    genre=scrapy.Field()
    director=scrapy.Field()
    writer=scrapy.Field()
    cast=scrapy.Field()
    movie_info=scrapy.Field()



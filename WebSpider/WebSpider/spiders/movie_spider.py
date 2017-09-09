#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#爬取烂番茄上从2014-2017年评分在前1001的电影的信息
import scrapy
from WebSpider.items import WebSpiderItem
import re

class MovieSpider(scrapy.spiders.Spider):
    name='rottentomatoes'  #爬虫的名字，必须是唯一的
    allowed_domains=['www.rottentomatoes.com']  #限制爬虫爬取特定域名下的网页
    start_urls=["https://www.rottentomatoes.com/top/bestofrt/?year="+x for x in ['2014','2015','2016']] #初始爬取的url列表，后续的url都从初始url获取的数据中提取

    #去除掉空白符，使提取到的数据标准化
    def standard(self,raw_item):
        std_item=','.join(raw_item).strip().replace('\n','')
        return re.sub('\s{2,}', '', std_item)

    #获取每部电影的URL
    def parse(self,response):
        raw_urls=response.xpath('//td/a[@class="unstyled articleLink"]/@href').extract()
        urls=[]
        for raw_url in raw_urls:
            url='https://www.rottentomatoes.com'+raw_url
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url,callback=self.parse_movie)

    #解析页面
    def parse_movie(self, response):
        try:
            name =response.xpath('//meta[@name="movieTitle"]/@content').extract() #电影名称

            year=response.xpath('//title/text()').extract()
            year=re.search(r'\d{4}',year[0]).group()  #电影上映的年份

            link = response.url #电影的url

            tomatometer=response.xpath('//*[@id="tomato_meter_link"]/span[2]/span/text()').extract()[0]+'%'  #烂番茄评分

            audience_score=response.xpath('//*[@id="scorePanel"]/div[2]/div[1]/a/div/div[2]/div[1]/span/text()').extract()  #观众评分

            runtime=response.xpath('//time[@datetime]/text()').extract()[-1]
            runtime = re.sub('\s{2,}', '', runtime)  #电影时长
            try:
                runtime=int(runtime.split(' ')[0])
            except ValueError:
                runtime=None

            genre=self.standard(response.xpath('//ul[@class="content-meta info"]/li[2]/div[2]/a/text()').extract()) #电影类型

            director=self.standard(response.xpath('//ul[@class="content-meta info"]/li[3]/div[2]/a/text()').extract()) #导演

            writer = self.standard(response.xpath('//ul[@class="content-meta info"]/li[4]/div[2]/a/text()').extract())#编剧

            cast = self.standard(response.xpath('//div[@class="media-body"]/a[@class="unstyled articleLink"]/span[@title]/text()').extract()) #演员

            movie_info = self.standard(response.xpath('//*[@id="movieSynopsis"]/text()').extract()) #电影简介

        except:
            print('Error in URL' % response.url)
            return

        item = WebSpiderItem()
        item['name'] = name
        item['year'] = year
        item['link']=link
        item['tomatometer']=tomatometer
        item['audience_score'] = audience_score
        item['runtime'] = runtime
        item['genre'] = genre
        item['director'] = director
        item['writer'] = writer
        item['cast'] = cast
        item['movie_info'] =movie_info
        yield item




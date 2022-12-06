# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']

    user_agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/', headers={
            'User-Agent' : self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield{
            'title': response.xpath("//div[@class='sc-80d4314-1 fbQftq']/h1/text()").get(),
            'year': response.xpath("//div[@class='sc-80d4314-2 iJtmbR']/ul/li[1]/span/text()").get(),
            'duration': response.xpath("normalize-space(//div[@class='sc-80d4314-2 iJtmbR']/ul/li[3]/text())").get(),
            'genre': response.xpath("//div[@class='ipc-chip-list__scroller']/a/span/text()").get(),
            'movie_url': response.url,
            'user_agent': response.request.headers['User-Agent']
        }

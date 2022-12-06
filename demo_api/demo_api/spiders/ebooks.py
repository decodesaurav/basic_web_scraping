# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.exceptions import CloseSpider


class EbooksSpider(scrapy.Spider):
    INCREMENTED_BY = 12
    offset = 0
    name = 'ebooks'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12']

    def parse(self, response):

        if response.status == 500:
            raise CloseSpider('Reached last page...')

        resp = json.loads(response.body)
        ebooks = resp.get('works')

        for ebook in ebooks:
            yield{
                'title': ebook.get('title'),
                'subject': ebook.get('subject')
            }
        self.offset += self.INCREMENTED_BY
        yield scrapy.Request(
            url = f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}',
            callback=self.parse
        )

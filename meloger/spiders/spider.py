import json

import scrapy


class ImmoscoutSpider(scrapy.Spider):
    name = 'immoscout'
    allowed_domains = ['www.immoscout24.ch']
    start_urls = ['https://www.immoscout24.ch/fr/immobilier/acheter/canton-geneve?pn=1']

    def parse(self, response):
        data_js = response.xpath('//script[@id="state"]/text()').re(r'{.*')[0]
        data_js = data_js.replace(':undefined', ':""')
        data = json.loads(data_js)
        for listing in data['pages']['searchResult']['resultData']['listData']:
            yield {
                'rooms': listing.get('numberOfRooms', None),
                'area': listing.get('surfaceLiving', None),
                'price': listing.get('sellingPrice', None)
            }
        page_number_param_ix = response.url.find('pn=')
        page_number = int(response.url[page_number_param_ix + 3:])
        next_page_url = response.url[:page_number_param_ix] + 'pn=' + str(page_number + 1)
        yield response.follow(next_page_url, callback=self.parse)

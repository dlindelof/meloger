import json

import scrapy


class ImmoscoutSpider(scrapy.Spider):
    name = 'immoscout'
    allowed_domains = ['www.immoscout24.ch']
    start_urls = [
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-appenzell-re?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-appenzell-ri?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-argovie?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-bale-campagne?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-bale-ville?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-berne?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-fribourg?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-geneve?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-glaris?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-grisons?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-jura?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-lucerne?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-neuchatel?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-nidwald?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-obwald?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-st-gall?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-schaffhouse?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-schwyz?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-soleure?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-tessin?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-turgovie?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-uri?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-valais?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-vaud?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-zoug?pn=1',
        'https://www.immoscout24.ch/fr/immobilier/acheter/canton-zurich?pn=1',
    ]

    def parse(self, response):
        data_js = response.xpath('//script[@id="state"]/text()').re(r'{.*')[0]
        data_js = data_js.replace(':undefined', ':""')
        data = json.loads(data_js)
        for listing in data['pages']['searchResult']['resultData']['listData']:
            yield {
                'rooms': listing.get('numberOfRooms', None),
                'area': listing.get('surfaceLiving', None),
                'price': listing.get('sellingPrice', None),
                'city': listing.get('cityName', None),
                'canton': listing.get('state', None)
            }
        page_number_param_ix = response.url.find('pn=')
        page_number = int(response.url[page_number_param_ix + 3:])
        next_page_url = response.url[:page_number_param_ix] + 'pn=' + str(page_number + 1)
        yield response.follow(next_page_url, callback=self.parse)

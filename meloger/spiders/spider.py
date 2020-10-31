import scrapy


class ImmoscoutSpider(scrapy.Spider):
    name = 'immoscout'
    allowed_domains = ['www.immoscout24.ch']
    start_urls = ['https://www.immoscout24.ch/fr/immobilier/acheter/canton-geneve']

    def parse(self, response):
        articles = response.xpath('//article')
        for article in articles:
            header = article.xpath('.//h3/a/text()').re(r'\d[\d,]*')
            price = article.xpath('.//h3/a/span/text()').re(r'\d[\d ]*')
            yield {
                'rooms': header[0].replace(',', '.') if header else None,
                'area': header[1] if header else None,
                'price': price[0].replace(' ', '')
            }

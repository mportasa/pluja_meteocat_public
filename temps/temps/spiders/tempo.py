# -*- coding: utf-8 -*-
import scrapy
from datetime import timedelta, date

#import scrapy-user-agents

class TempoSpider(scrapy.Spider):
    name = 'tempo'
    allowed_domains = ['www.meteo.cat/observacions/xema/dades?codi=MV&dia=2023-04-06T00:00Z']
    '''
    start_urls = [
        'https://www.meteo.cat/observacions/xema/dades?codi=MV&dia=2023-04-08T00:00Z',
        'https://www.meteo.cat/observacions/xema/dades?codi=MV&dia=2023-04-09T00:00Z',
        'https://www.meteo.cat/observacions/xema/dades?codi=MV&dia=2023-04-10T00:00Z']
    #start_urls = []
    #https://quotes.toscrape.com/
    '''
    start_urls = []
    def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)
    #https://stackoverflow.com/questions/62687877/scrapy-start-url-using-date-range
    start_date = date(2013, 4, 18)
    end_date = date(2023, 4, 18)
    start_urls = []
    start_url='https://www.meteo.cat/observacions/xema/dades?codi=MV&dia='
    end_url='T00:00Z'
    for single_date in daterange(start_date, end_date):
        start_urls.append(single_date.strftime(start_url+"%Y-%m-%d"+end_url))

    print(start_urls)

    def parse(self, response):
        #https://www.simplified.guide/scrapy/scrape-table
        table=response.xpath('//table')[0]
        rows=table.xpath('//tr')
        fetxa=response.css('div')[24]

        yield {
                'precipitacio': rows.xpath('td//text()')[6].extract().strip(),
                'dia': fetxa.css('input')[2].xpath('@value').extract(),
                #'last': row.xpath('td[2]//text()').extract_first(),
                #'handle' : row.xpath('td[3]//text()').extract_first(),
            }

        #response.xpath('//ttitle')
        #yield {'titulo': title}


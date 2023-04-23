# -*- coding: utf-8 -*-
import scrapy
from datetime import timedelta, date


# import scrapy-user-agents

class TempoSpider(scrapy.Spider):
    name = 'tempo'
    allowed_domains = ['www.meteo.cat/observacions/xema/dades?codi=MV&dia=']

    start_urls = []

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    # https://stackoverflow.com/questions/62687877/scrapy-start-url-using-date-range
    start_date = date(2013, 4, 17)
    end_date = date(2023, 4, 18)
    start_urls = []
    start_url = 'https://www.meteo.cat/observacions/xema/dades?codi=MV&dia='
    end_url = 'T00:00Z'  # Mitjanit
    for single_date in daterange(start_date, end_date):
        start_urls.append(single_date.strftime(start_url + "%Y-%m-%d" + end_url))

    print(start_urls)

    def parse(self, response):
        # https://www.simplified.guide/scrapy/scrape-table
        # Seleccionem la taula de la pàgina que conté les dades i les seves files (rows)
        table = response.xpath('//table[caption[text()="Dades diàries de l\'estació meteorològica"]]')
        rows = table.xpath('//tr')
        # Seleccionem l'etiqueta div.data per seleccionar la data
        data = response.css('div.data input#datepicker').xpath('../..')

        # Definim totes les variables que volem obtenir, posant condicions en cas que no existeixin:

        temp_mitj_row = rows.xpath('//tr[th[text()="Temperatura mitjana"]]/td[1]')
        temp_mitj = temp_mitj_row.xpath('.//text()').get().strip() if temp_mitj_row else None

        temp_max_row = rows.xpath('//tr[th[text()="Temperatura màxima"]]/td[1]')
        temp_max = temp_max_row.xpath('.//text()').get().strip() if temp_max_row else None

        temp_min_row = rows.xpath('//tr[th[text()="Temperatura mínima"]]/td[1]')
        temp_min = temp_min_row.xpath('.//text()').get().strip() if temp_min_row else None

        hum_rel_row = rows.xpath('//tr[th[text()="Humitat relativa mitjana"]]/td[1]')
        hum_rel = hum_rel_row.xpath('.//text()').get().strip() if hum_rel_row else None

        precipitacio_row = rows.xpath('//tr[th[text()="Precipitació acumulada"]]/td[1]')
        precipitacio = precipitacio_row.xpath('.//text()').get().strip() if precipitacio_row else None

        # Obtenim les dades
        yield {
            'dia': data.css('input')[2].xpath('@value').extract(),
            'Temperatura mitjana': temp_mitj,
            'Temperatura màxima': temp_max,
            'Temperatura mínima': temp_min,
            'Humitat relativa mitjana': hum_rel,
            'Precipitacio': precipitacio,
            # 'last': row.xpath('td[2]//text()').extract_first(),
            # 'handle' : row.xpath('td[3]//text()').extract_first(),
        }

        # response.xpath('//ttitle')
        # yield {'titulo': title}

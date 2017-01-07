#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from regelwikiparser.items import SpellItem


class Magic(CrawlSpider):
    name = "magic"
    start_urls = ["http://www.ulisses-regelwiki.de/index.php/zauber.html"]
    allowed_domains = ["ulisses-regelwiki.de"]
    rules = (
        Rule(LinkExtractor(allow=('za_rituale\.html',
                                  'za_zaubersprueche\.html',
                                  'Zauber_Zaubertricks\.html'))),
        Rule(LinkExtractor(allow=('Rit_.*\.html')), callback='parse_spell'),
        Rule(LinkExtractor(allow=('ZT_.*\.html')), callback='parse_spell'),
        Rule(LinkExtractor(allow=('ZS_.*\.html')), callback='parse_spell')
    )

    def parse_spell(self, response):

        item = SpellItem()
        item['properties'] = {}
        properties = [
            "Probe",
            "Wirkung",
            "Ritualdauer",
            "Zauberdauer",
            "AsP-Kosten",
            "Reichweite",
            "Wirkungsdauer",
            "Zielkategorie",
            "Merkmal",
            "Verbreitung",
            "Steigerungsfaktor",
            "Anmerkung"
        ]

        name_query = "//div/h1/text()"
        selector = response.xpath(name_query)
        name = selector.extract_first()
        item['name'] = name
        item['link'] = response.url

        short_url = response.url.rsplit('/', 1)[-1]
        if short_url.startswith('Rit_'):
            item['spellclass'] = 'Ritual'
        elif short_url.startswith('ZT_'):
            item['spellclass'] = 'Zaubertrick'
        elif short_url.startswith('ZS_'):
            item['spellclass'] = 'Zauberspruch'
        else:
            print("\nERROR\n")
            print(short_url)

        for p in properties:
            p_query = "//p/strong[contains(.,'" + p + \
                "')]/following-sibling::text()[1]"
            selector = response.xpath(p_query)
            s = selector.extract()
            if s:
                if p == "Anmerkung":
                    p = "Verbreitung"
                item['properties'][p] = s[0].lstrip()
        return item

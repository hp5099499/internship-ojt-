import scrapy
from pathlib import Path
from urllib.parse import urljoin
import csv

class EciSpider(scrapy.Spider):
    name = "eci"
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/PcResultGenJune2024/index.htm"]
    count = 0
    finalData = []

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
    headers = {
        'authority': 'results.eci.gov.in',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        state_options = response.xpath('//select[@id="ctl00_ContentPlaceHolder1_Result1_ddlState"]/option[position() > 1]')
        for state_option in state_options:
            state_value = state_option.xpath('./@value').get()
            state_name = state_option.xpath('text()').get()
            state_url = f"https://results.eci.gov.in/PcResultGenJune2024/partywiseresult-{state_value}.htm"
            yield scrapy.Request(state_url, headers=self.headers, callback=self.parse_party, meta={'state_name': state_name})

    def parse_party(self, response):
        state_name = response.meta['state_name']
        party_urls = response.xpath('//table[@class="table"]/tbody/tr/td[2]/a/@href').getall()
        for party in party_urls:
            abs_party = urljoin(response.url, party)
            yield scrapy.Request(abs_party, headers=self.headers, callback=self.parse_constituency, meta={'state_name': state_name})

    def parse_constituency(self, response):
        state_name = response.meta['state_name']
        constituency_urls = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[2]/a/@href').getall()
        for cons in constituency_urls:
            abs_constit_url = urljoin(response.url, cons)
            constit_name = response.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr/td[2]/a/text()').get()
            yield scrapy.Request(abs_constit_url, headers=self.headers, callback=self.parse_candidate, meta={'state_name': state_name, 'constituency_name': constit_name})

    def parse_candidate(self, response):
        state_name = response.meta['state_name']
        constituency_name = response.meta['constituency_name']
        candidate_cards = response.xpath('//div[@class="cand-info"]')
        for card in candidate_cards:
            self.count += 1
            finalData = {
                'ref': str(self.count),
                'state': state_name,
                'constituency': constituency_name,
                'won status': card.xpath('.//div/div[1]/text()').get(default='').strip(),
                'votes': card.xpath('.//div/div[2]/text()').get(default='').strip(),
                '(votes)': card.xpath(".//div/div[2]/span/text()").get(default='').strip(),
                'Name': card.xpath('.//div[@class="nme-prty"]/h5/text()').get(default=''),
                'Party Name': card.xpath('.//div[@class="nme-prty"]/h6/text()').get(default=''),
            }
            self.finalData.append(finalData)

    def close(self, reason):
        with open('election.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['ref', 'state', 'constituency', 'won status', 'votes', '(votes)', 'Name', 'Party Name']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.finalData)

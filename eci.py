import scrapy
from urllib.parse import urljoin
import csv

class EciSpider(scrapy.Spider):
    name = "eci"
    brand_name = 'election'
    spider_type = 'chain'
    spider_chain_id = '1509'
    user = 'useyouremail@hotmail.com'
    allowed_domains = ["results.eci.gov.in"]
    start_urls = ["https://results.eci.gov.in/PcResultGenJune2024/index.htm"]
    count = 0

    
    headers = {
        'authority': 'www.aspendental.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        state_urls = response.xpath('//div[@id="gatsby-focus-wrapper"]/div[9]/ul/li/a/@href').getall()
        for state_url in state_urls:
            absolute_state_url = urljoin(response.url, state_url)
            yield scrapy.Request(absolute_state_url, callback=self.parse_state)

    def parse_state(self, response):
        city_urls = response.xpath('//li[@class="MuiListItem-root MuiListItem-gutters MuiListItem-padding css-5r3rdl"]/a/@href').getall()
        for city_url in city_urls:
                absolute_city_url = urljoin(response.url, city_url)
                yield scrapy.Request(absolute_city_url, callback=self.parse_store)


    def parse_store(self, response):
        finalData = {}
        self.count += 1
        finalData['ref'] = str(self.count)
        finalData["address"] = response.xpath('//div[@id="gatsby-focus-wrapper"]/div[3]/div/div/div[4]/div[1]/a/span/button/text()').get(default='')

        with open('aspen.csv', mode='a', newline='') as csv_file:
            fieldnames = ['ref', 'address']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if csv_file.tell() == 0:
                writer.writeheader()
            writer.writerow(finalData)

        yield finalData

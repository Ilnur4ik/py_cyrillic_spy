import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse
from scrapy import Request
import re


class CyrillicSpider(scrapy.Spider):
    name = 'cyrillic_spider'

    custom_settings = {
        'LOG_LEVEL': 'ERROR',
    }

    def __init__(self, url_file=None, *args, **kwargs):
        super(CyrillicSpider, self).__init__(*args, **kwargs)
        self.file_output = open('output.txt', 'w', encoding='utf-8')

        with open(url_file, 'r', encoding='utf-8') as file:
            self.start_urls = [line.strip() for line in file]

        self.allowed_domains = [
            urlparse(url).netloc for url in self.start_urls]

    def parse(self, response):
        # Используем регулярное выражение для поиска кириллического текста
        cyrillic_text = re.findall(r'\b[а-яА-ЯЁё]+\b', response.text)
        if cyrillic_text:
            print(f'Кириллица найдена на {response.url}')
            print(f'Текст: {" ".join(cyrillic_text)}')
            self.file_output.write(f'Кириллица найдена на {response.url}\n')
            self.file_output.write(f'Текст: {" ".join(cyrillic_text)}\n')

        # Поиск ссылок для перехода на другие страницы
        requests = []
        for next_page in response.css('a::attr(href)').getall():
            if next_page is not None and next_page.startswith(('http://', 'https://')):
                requests.append(Request(next_page, callback=self.parse))
        return requests


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(CyrillicSpider, url_file='urls.txt')
    process.start()

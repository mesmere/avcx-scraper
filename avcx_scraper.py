import argparse
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.crawler import CrawlerProcess

class AutoFilenameFilesPipeline(FilesPipeline):
    """Use the Content-Disposition header (if available) to determine the filename for download."""
    def file_path(self, request, response=None, info=None, *, item=None):
        try:
            if response is not None:
                headers = response.headers.to_unicode_dict()
                if 'Content-Disposition' in headers:
                    from email import message
                    m = message.EmailMessage()
                    m.add_header('content-disposition', headers['Content-Disposition'])
                    filename = m.get_filename()
                    if filename is not None:
                        return filename
        except:
            pass
        return super().file_path(request, response, info, item=item) 

class AVCXHeadersMiddleware:
    """Add X-headers that the the site frontend adds."""
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        if 'PA_AUS' in request.cookies:
            request.headers['X-Auth-Key'] = request.cookies['PA_AUS']
        if 'PA_ATOK' in request.cookies:
            request.headers['X-Auth-Token'] = request.cookies['PA_ATOK']

class AVCXScraper(scrapy.Spider):
    name = 'avcx-scraper'
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'FILES_STORE': 'out/',
        'MEDIA_ALLOW_REDIRECTS': True,
        'ITEM_PIPELINES': {'avcx_scraper.AutoFilenameFilesPipeline': 300},
        'DOWNLOADER_MIDDLEWARES': {'avcx_scraper.AVCXHeadersMiddleware': 701},
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def start_requests(self):
        return [scrapy.FormRequest('https://avxwords.com/log-in/',
                                   formdata={'email': self.email, 'password': self.password},
                                   callback=self.page_logged_in)]

    def page_logged_in(self, response):
        return scrapy.Request('https://avxwords.com/your-account/?v=puzzles', callback=self.page_year)

    def page_year(self, response):
        for puzzle_anchor in response.css('#account-puzzle-calendar .month-events a.list-group-item'):
            yield scrapy.Request(puzzle_anchor.attrib['href'], callback=self.page_download, priority=10)

        prev_year_anchor = response.css('#account-puzzle-calendar > nav > .nav-item:first-child')
        if 'puzzles_by_year=2005' not in prev_year_anchor.attrib['href']:
            yield scrapy.Request(prev_year_anchor.attrib['href'], callback=self.page_year, priority=0)

    def page_download(self, response):
        file_urls = []
        for download_link in response.css('#puzzle-download .download-link'):
            if "acrosslite" in download_link.get().lower():
                file_urls.append(download_link.attrib['href'])
        return {'file_urls': file_urls}

parser = argparse.ArgumentParser(prog='avcx_scraper.py', description='Download the entire AVCX crossword library.')
parser.add_argument('--email', required=True)
parser.add_argument('--password', required=True)
args = parser.parse_args()

# The twisted reactor doesn't exit gracefully without this line. (???)
if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'TELNETCONSOLE_ENABLED': False,
    })
    process.crawl(AVCXScraper, email=args.email, password=args.password)
    process.start()

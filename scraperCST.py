import scrapy
import os
import re
from urllib.parse import urljoin

class CSTSpider(scrapy.Spider):
    name = "CSTSpider"
    count = 0
    start_urls = [
        "https://www.gov.uk/search/news-and-communications?organisations[]=council-for-science-and-technology&parent=council-for-science-and-technology",
        "https://www.gov.uk/search/research-and-statistics?organisations[]=council-for-science-and-technology&parent=council-for-science-and-technology",
        "https://www.gov.uk/search/policy-papers-and-consultations?organisations[]=council-for-science-and-technology&parent=council-for-science-and-technology",
        "https://www.gov.uk/search/transparency-and-freedom-of-information-releases?organisations[]=council-for-science-and-technology&parent=council-for-science-and-technology",
        "https://www.gov.uk/search/all?organisations[]=council-for-science-and-technology&order=updated-newest&parent=council-for-science-and-technology",
        "https://www.gov.uk/search/guidance-and-regulation?organisations[]=council-for-science-and-technology&parent=council-for-science-and-technology",
    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Set download delay to 2 seconds
        'AUTOTHROTTLE_ENABLED': True,  # Enable autothrottle
    }

    def parse(self, response):
        for title in response.css("li.gem-c-document-list__item, li.gem-c-document-list-child"):
            if self.count < 400:  # Increase limit to 400
                relative_url = title.css("a::attr(href)").get()
                absolute_url = urljoin("https://www.gov.uk", relative_url)
                yield scrapy.Request(absolute_url, callback=self.parse_details, meta={'url': absolute_url})
                self.count += 1
                print('PAGE COUNT '+str(self.count))
        
        # Get the link to the next page
        next_page = response.css('a.govuk-link.govuk-pagination__link::attr(href)').get()
        if next_page is not None and self.count < 400:
            yield response.follow(next_page, self.parse)

    def parse_details(self, response):
        url = response.meta['url']
        title = response.css("h1::text").get()
        content = ' '.join(response.css("div.govspeak").getall())
        content = re.sub('<.*?>', '', content)
    
        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Join the directory with the output file name
        output_file = os.path.join(dir_path, 'cst.txt')

        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f'Title: {title}\n')
            f.write(f'URL: {url}\n')
            f.write(f'Content: {content}\n\n')

# Run the spider
if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess()
    process.crawl(CSTSpider)
    process.start()
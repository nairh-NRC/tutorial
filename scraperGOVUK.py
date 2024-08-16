import scrapy
import os
from urllib.parse import urljoin

class GOVUKSpider(scrapy.Spider):
    name = "GOVUKSpider"
    count = 0
    start_index = 0
    start_urls = [
        "https://www.gov.uk/search/news-and-communications?keywords=investment&public_timestamp%5Bfrom%5D=01/01/2023&order=relevance",
        "https://www.gov.uk/search/research-and-statistics?content_store_document_type=all_research_and_statistics&world_locations%5B%5D=germany&world_locations%5B%5D=japan&world_locations%5B%5D=uk-and-the-commonwealth&world_locations%5B%5D=uk-delegation-to-council-of-europe&world_locations%5B%5D=uk-delegation-to-organization-for-security-and-co-operation-in-europe&world_locations%5B%5D=uk-joint-delegation-to-nato&world_locations%5B%5D=uk-mission-to-asean&world_locations%5B%5D=uk-mission-to-the-eu&world_locations%5B%5D=uk-mission-to-the-united-nations&world_locations%5B%5D=uk-mission-to-the-united-nations-new-york&world_locations%5B%5D=uk-mission-to-the-wto-un-and-other-international-organisations-geneva&world_locations%5B%5D=the-uk-permanent-delegation-to-the-oecd-organisation-for-economic-co-operation-and-development&order=updated-newest",
        "https://www.gov.uk/search/policy-papers-and-consultations?world_locations%5B%5D=germany&world_locations%5B%5D=japan&world_locations%5B%5D=united-kingdom&world_locations%5B%5D=uk-and-the-commonwealth&world_locations%5B%5D=uk-delegation-to-council-of-europe&world_locations%5B%5D=uk-delegation-to-organization-for-security-and-co-operation-in-europe&world_locations%5B%5D=uk-joint-delegation-to-nato&world_locations%5B%5D=uk-mission-to-asean&world_locations%5B%5D=uk-mission-to-the-eu&world_locations%5B%5D=uk-mission-to-the-united-nations&world_locations%5B%5D=uk-mission-to-the-united-nations-new-york&world_locations%5B%5D=uk-mission-to-the-wto-un-and-other-international-organisations-geneva&world_locations%5B%5D=the-uk-permanent-delegation-to-the-oecd-organisation-for-economic-co-operation-and-development&order=updated-newest",

    ]
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Set download delay to 2 seconds
    }

    def parse(self, response):
        for title in response.css("li.gem-c-document-list__item"):
            if self.count < 100:  # Increase limit to 500
                relative_url = title.css("a::attr(href)").get()
                absolute_url = urljoin("https://www.gov.uk", relative_url)
                yield scrapy.Request(absolute_url, callback=self.parse_details, meta={'url': absolute_url})
                self.count += 1
                print('PAGE COUNT '+str(self.count))
        
        # Get the link to the next page
        next_page = response.css('a.govuk-link.govuk-pagination__link::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_details(self, response):
        url = response.meta['url']
        title = response.css("h1::text").get()
        content = ' '.join(response.css("div.govuk-grid-row *::text").getall())
    
        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Join the directory with the output file name
        output_file = os.path.join(dir_path, 'govuk.txt')

        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f'Title: {title}\n')
            f.write(f'URL: {url}\n')
            f.write(f'Content: {content}\n\n')

# Run the spider
if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    
    process = CrawlerProcess()
    process.crawl(GOVUKSpider)
    process.start()
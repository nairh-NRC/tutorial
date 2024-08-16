import scrapy


class UKRISpider(scrapy.Spider):
    name = "title"
    start_urls = [
        "https://www.ukri.org/?st=NRC",
        "https://www.ukri.org/?st=Investment",
        #"https://www.digicatapult.org.uk/?s=NRC"
    ]
    count = 0

    def parse(self, response):
        for title in response.css("div.search-result"):
            if self.count < 50:
                yield {
                "title": title.css("a::text").getall(),
                "url": title.css("p::text").getall(),
                }
                self.count+=1

        if self.count < 50:
        # Get the link to the next page
            next_page = response.css('a.next.page-numbers::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)

    # def closed(self, reason):
    #     # Save the data as text
    #     with open("titles.txt", "w") as txt_file:
    #         for item in self.parse(response=None):
    #             txt_file.write(f"Title: {', '.join(item['title'])}\n")
    #             txt_file.write(f"URL: {', '.join(item['url'])}\n\n")


# Run the spider
if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(UKRISpider)
    process.start()
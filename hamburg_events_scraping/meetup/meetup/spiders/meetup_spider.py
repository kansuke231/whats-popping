import scrapy
from scrapy_splash import SplashRequest


class HamburgMeetupSpider(scrapy.Spider):
    name = "hamburg_meetup"
    BASE_URL = 'https://www.meetup.com/find/?suggested=true&source=EVENTS&location=de--Hamburg&eventType=inPerson&dateRange=today&distance=twentyFiveMiles&sortField=RELEVANCE'
    
    start_urls = [
        BASE_URL
    ]


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 3})

    def parse(self, response):
        for event in response.xpath('//div[@data-recommendationid]'):

            yield {
                'title': event.xpath('.//h2/text()').get(),                
                'time': event.xpath('.//time/text()').get(), # or xs[0].xpath('//time/@datetime') or xs[0].xpath('//time/@title')
                'link': event.xpath('.//a[@id="event-card-in-search-results"]/@href').get(),
                'image': event.xpath('.//img/@src').get(),
            }
        
        
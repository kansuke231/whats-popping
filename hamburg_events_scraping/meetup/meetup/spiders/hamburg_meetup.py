import scrapy
import pendulum

class HamburgMeetupSpider(scrapy.Spider):
    name = "hamburg_meetup"
    BASE_URL = 'https://www.meetup.com/find/?suggested=true&source=EVENTS&location=de--Hamburg&eventType=inPerson&dateRange=today&distance=twentyFiveMiles&sortField=RELEVANCE'
    
    start_urls = [
        BASE_URL
    ]


    def __init__(self, *args, **kwargs):
        super(HamburgMeetupSpider, self).__init__(*args, **kwargs)
        self.custom_time = pendulum.now("Europe/Berlin").to_date_string()

    def parse(self, response):
        for event in response.xpath('//div[@data-recommendationid]'):

            yield {
                'title': event.xpath('.//h2/text()').get(),                
                'time': event.xpath('.//time/text()').get(), # or xs[0].xpath('//time/@datetime') or xs[0].xpath('//time/@title')
                'link': event.xpath('.//a[@id="event-card-in-search-results"]/@href').get(),
                'image': event.xpath('.//img/@src').get(),
            }
        
        
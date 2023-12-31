import scrapy
import pendulum

class MeetupSpider(scrapy.Spider):
    name = "meetup"
    TODAY = pendulum.now("Europe/Berlin").to_date_string()
    DATE_RANGE = f'customStartDate={TODAY}T00%3A00%3A00-04%3A00&customEndDate={TODAY}T23%3A59%3A00-04%3A00'
    BASE_URL = f'https://www.meetup.com/find/?suggested=true&source=EVENTS&location=de--{{city}}&eventType=inPerson&distance=twentyFiveMiles&sortField=RELEVANCE&{DATE_RANGE}'



    def __init__(self, *args, **kwargs):
        super(MeetupSpider, self).__init__(*args, **kwargs)
        self.custom_time =  self.TODAY
        self.city_url = self.BASE_URL.format(city=self.city)
        self.start_urls.append(self.city_url)


    def parse(self, response):
        for event in response.xpath('//div[@data-recommendationid]'):

            yield {
                'title': event.xpath('.//h2/text()').get(),                
                'time': event.xpath('.//time/text()').get(), # or xs[0].xpath('//time/@datetime') or xs[0].xpath('//time/@title')
                'link': event.xpath('.//a[@id="event-card-in-search-results"]/@href').get(),
                'image': event.xpath('.//img/@src').get(),
            }
        
        
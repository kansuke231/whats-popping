import scrapy
import pendulum
import json
    


class EventbriteSpider(scrapy.Spider):
    name = "eventbrite"

    BASE_URL = 'https://www.eventbrite.de/d/germany--hamburg/events--today/?page=1'

    start_urls = [
       BASE_URL
    ]

    def __init__(self, *args, **kwargs):
        super(EventbriteSpider, self).__init__(*args, **kwargs)
        self.custom_time = pendulum.now("Europe/Berlin").to_date_string()

    def parse(self, response):
        events = response.css('script[type="application/ld+json"]::text').getall()
        for event in events:
            data = json.loads(event)
            yield {
                'title': data.get('name'),
                'time': data.get('startDate'),
                'location': data.get('location').get('address').get('streetAddress'),
                'link': data.get('url'),
                'description': data.get('description'),
                'image': data.get('image'),
            }
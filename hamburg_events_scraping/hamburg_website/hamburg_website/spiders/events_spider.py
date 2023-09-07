import scrapy
import pendulum

    

def format_date(date):
    day  = str(date.day).zfill(2)
    month = str(date.month).zfill(2)
    year = date.year
    return f'{day}.{month}.{year}'

def today() -> str:
    now = pendulum.now("Europe/Berlin")
    return format_date(now)

def next_week() -> str:
    now = pendulum.now("Europe/Berlin").add(weeks=1)
    return format_date(now)


class HamburgEventsSpider(scrapy.Spider):
    name = "hamburg_events"

    BASE_URL = 'https://www.hamburg-travel.com'
    API_ENDPOINT = f'{BASE_URL}/see-explore/events/events-calendar/js.api'

    page = 1

    start_urls = [
        f'{API_ENDPOINT}?filter%5Bdate%5D%5B0%5D={today()}&filter%5Bdate%5D%5B1%5D={next_week()}&filter%5Bdistance%5D=15&filter%5Bdistrict%5D=hh_all&filter%5Bsearchword%5D=&pageDate={today()}&page={page}'
    ]


    def parse(self, response):
        if len(response.css("div.teaserList-inline__page article.listTeaser-event")) == 0 :
            return
        for article in response.css("div.teaserList-inline__page article.listTeaser-event"):

            calendar = article.xpath('.//span[@class="icon-calendar"]/following-sibling::text()').get().strip()
            hour = article.xpath('//span[@class="icon-clock"]/following-sibling::text()').get().strip()
            yield {
                'title': article.css("div.listTeaser-event__text h3::text").get(),
                'location': article.xpath('.//span[@class="icon-located"]/following-sibling::text()').get().strip(),
                'time': f'{calendar} {hour}',
                'description': "".join(article.css("div.listTeaser-event__text p::text").getall()).strip(),
                'link': f'{self.BASE_URL}{article.css("a.listTeaser-event__link::attr(href)").get()}',
                'image': f"{self.BASE_URL}{article.xpath('.//img/@src').get()}",
            }
        
        
        self.page = self.page + 1
        next_url = f"{self.start_urls[0].split('page=')[0]}page={self.page}"

        yield scrapy.Request(next_url, callback=self.parse)
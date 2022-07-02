import scrapy


class NewenglandSpider(scrapy.Spider):
    name = 'newengland'
    allowed_domains = ['crossfitnewengland.com']
    start_urls = ['https://crossfitnewengland.com/wod-and-schedule/']

    def parse(self, response):
        for link in response.css('link[rel="canonical"]::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_wods)

        previous_page = response.css('.top-wod-nav.bg-primary.text-white a::attr(href)').get()
        if previous_page is not None:
            yield response.follow(previous_page, callback=self.parse)

    def parse_wods(self, response):
        workouts = response.css('.wodwrap')
        for wod in workouts:
            yield {
                'workout_date': wod.css('.wod-nav-title ::text').get(),
                'title': wod.css('.text-primary ::text').get(),
                'workout': wod.css('.workout-description ::text').getall(),
            }

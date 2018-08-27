import scrapy

class QuoteData(scrapy.Item):
	quote = scrapy.Field()
	author = scrapy.Field()
	tags = scrapy.Field()

class QuoteDataSpider(scrapy.Spider):
	name = "quotes"

	start_urls = ['http://quotes.toscrape.com/login']

	def parse(self, response):
		return scrapy.FormRequest.from_response(response, formdata={'username': 'user', 'password': 'pass'}, callback=self.after_login)
		
	def after_login(self, response):

		quoteData = QuoteData()
		quoteBlocks = response.css('div.quote')

		for block in quoteBlocks:
			quoteData['quote'] = block.css('span.text::text').extract_first()
			quoteData['author'] = block.css('span small::text').extract_first()
			quoteData['tags'] = block.css('div.tags a.tag::text').extract()

			yield quoteData	

		# follow pagination links
		for a in response.css('li.next a'):
			yield response.follow(a, callback=self.after_login)
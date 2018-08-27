import scrapy
import json

class QuoteData(scrapy.Item):
	quote = scrapy.Field()
	author = scrapy.Field()
	tags = scrapy.Field()

class QuoteDataSpider(scrapy.Spider):
	name = "quotes"

	quotes_start_url = 'http://spidyquotes.herokuapp.com/api/quotes?page=%s'
	start_urls = [quotes_start_url % 1]
	download_delay = 1

	def parse(self, response):

		quoteData = QuoteData()
		data = json.loads(response.body)
		
		for item in data.get('quotes', []):
			quoteData['quote'] = item.get('text')
			quoteData['author'] = item.get('author', {}).get('name')
			quoteData['tags'] = item.get('tags')

			yield quoteData

		if data['has_next']:
			next_page = data['page'] + 1
			yield scrapy.Request(self.quotes_start_url % next_page)
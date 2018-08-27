import scrapy
import json
import re
from scrapy_splash import SplashRequest

class QuoteData(scrapy.Item):
	quote = scrapy.Field()
	author = scrapy.Field()
	tags = scrapy.Field()

class QuoteDataSpider(scrapy.Spider):
	name = "quotes"

	start_urls = ['http://quotes.toscrape.com/js/page/1/']

	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url, self.parse, endpoint='render.html',args={'wait': 0.5},)

	def parse(self, response):

		quoteData = QuoteData()
		data = re.findall("var data =(.+?);\n", response.body.decode("utf-8"), re.S)

		dataJSON = []
		if data:
			dataJSON = json.loads(data[0])

		for item in dataJSON:
			quoteData['quote'] = item.get('text')
			quoteData['author'] = item.get('author', {}).get('name')
			quoteData['tags'] = item.get('tags')

			yield quoteData

		# follow pagination links
		for a in response.css('li.next a'):
			yield response.follow(a, callback=self.parse)
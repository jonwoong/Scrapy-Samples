import scrapy

class QuoteData(scrapy.Item):
	quote = scrapy.Field()
	author = scrapy.Field()
	tags = scrapy.Field()

class QuoteDataSpider(scrapy.Spider):
	name = "quotes"

	start_urls = ['http://quotes.toscrape.com/tableful/']

	def parse(self, response):

		quoteData = QuoteData()
		quotes = response.xpath('//*[contains(@style,"border-bottom")]/*[contains(@style,"top")]/text()')
		tags = response.xpath('//*[contains(@style,"padding-bottom")]')
		
		for quote, tag in zip(quotes, tags):
			quoteData['quote'] = quote.extract().split(" Author: ")[0]	
			quoteData['author'] = quote.extract().split(" Author: ")[1]
			quoteData['tags'] = tag.css('a::text').extract()
			yield quoteData	

		# follow pagination links
		for a in response.xpath('//*[contains(@href, "tableful/page/")]'):
			yield response.follow(a, callback=self.parse)
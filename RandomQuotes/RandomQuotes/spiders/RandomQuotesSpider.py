import scrapy

class QuoteData(scrapy.Item):
	quote = scrapy.Field()
	author = scrapy.Field()
	tags = scrapy.Field()

class QuoteDataSpider(scrapy.Spider):
	name = "quotes"

	start_urls = ['http://quotes.toscrape.com/random']

	def parse(self, response):

		quoteData = QuoteData()
		quoteBlocks = response.css('div.quote')
		
		for block in quoteBlocks:
			quoteData['quote'] = block.css('span.text::text').extract_first()
			quoteData['author'] = block.css('span small::text').extract_first()
			quoteData['tags'] = block.css('div.tags a.tag::text').extract()

			yield quoteData	
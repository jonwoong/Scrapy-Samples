import scrapy

class QuoteData(scrapy.Item):
	quote = scrapy.Field()
	author = scrapy.Field()
	tags = scrapy.Field()

class QuoteDataSpider(scrapy.Spider):
	name = "quotes"

	start_urls = ['http://quotes.toscrape.com/search.aspx']

	def parse(self, response):
		for author in response.css('select#author > option::attr(value)').extract():
			yield scrapy.FormRequest('http://quotes.toscrape.com/filter.aspx', formdata = {'author':author, '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first()}, callback=self.parse_tags)

	def parse_tags(self, response):
		for tag in response.css('select#tag > option::attr(value)').extract():
			yield scrapy.FormRequest('http://quotes.toscrape.com/filter.aspx', formdata={'author': response.css('select#author > option[selected]::attr(value)').extract_first(), 'tag':tag, '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first()},callback=self.parse_results)

	def parse_results(self, response):
		quoteData = QuoteData()
		for quote in response.css('div.quote'):
			quoteData['quote'] = quote.css('span.content::text').extract_first()
			quoteData['author'] = quote.css('span.author::text').extract_first()
			quoteData['tags'] = quote.css('span.tag::text').extract_first()
			yield quoteData



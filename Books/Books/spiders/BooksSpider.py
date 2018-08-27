import scrapy

numbers = {
	'One': '1',
	'Two': '2',
	'Three': '3',
	'Four': '4',
	'Five': '5'
}

class Book(scrapy.Item):
	title = scrapy.Field()
	upc = scrapy.Field()
	productType = scrapy.Field()
	priceNoTax = scrapy.Field()
	priceTax = scrapy.Field()
	tax = scrapy.Field()
	availability = scrapy.Field()
	reviews = scrapy.Field()
	rating = scrapy.Field()

class BooksSpider(scrapy.Spider):
	name = "books"

	start_urls = ['http://books.toscrape.com/catalogue/category/books_1/index.html']

	def parse(self, response):

		# follow links to book pages
		for href in response.css('h3 a::attr(href)'):
			yield response.follow(href, self.parse_book)

		# follow pagination links
		for href in response.css('li.next a::attr(href)'):
			yield response.follow(href, self.parse)

	def parse_book(self, response):
		
		book = Book()

		product_info = response.xpath('//table[@class="table table-striped"]//td/text()')

		book['title'] = response.xpath('////h1/text()').extract_first()
		book['upc'] = product_info.extract_first()
		book['productType'] = product_info[1].extract()
		book['priceNoTax'] = product_info[2].extract()[1:]
		book['priceTax'] = product_info[3].extract()[1:]
		book['tax'] = product_info[4].extract()[1:]
		book['availability'] = product_info[5].extract().strip()
		book['reviews'] = product_info[6].extract()
		book['rating'] = numbers[response.css('.star-rating').xpath("@class").extract_first().split()[1]]

		yield book
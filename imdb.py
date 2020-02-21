import scrapy

class ImdbSpider(scrapy.Spider):
	name = 'scores'

	start_urls = ['https://www.imdb.com/list/ls057823854/?sort=list_order,asc&st_dt=&mode=detail&page=1&ref_=ttls_vm_dtl']

	def parse(self, response):
		for movie in response.xpath("//div[@class='lister-item mode-detail']"):
			yield {
				'Title': movie.xpath(".//h3[@class='lister-item-header']/a/text()").extract_first(),
				'Imdb Score': movie.xpath(".//div[@class ='ipl-rating-star small']/span[@class = 'ipl-rating-star__rating']/node()").extract_first(),
				'Metascore': movie.xpath(".//div[@class= 'inline-block ratings-metascore']/span/text()").extract_first()

			}

		next_page = response.xpath("//a[@class = 'flat-button lister-page-next next-page']/@href").extract_first()
		if next_page is not None:
			next_page_link = response.urljoin(next_page)
			yield scrapy.Request(url=next_page_link, callback=self.parse)
import scrapy
import json


class ProductSpider(scrapy.Spider):
    name = "prod_imgs"
    # start_urls = ["https://wizaz.pl"+prod["href"] for prod in json.load(open("products.json")) if not prod["href"] is None]
    start_urls = json.load((open("lostLinks.json")))

    def parse(self, response):

        productConcat = {
            "img": response.css('.product-gallery.gallery img[itemprop="image"]::attr(src)').get(),
            "imgAlt": response.css('.product-gallery.gallery img[itemprop="image"]::attr(alt)').get(),
            "href": response.url,

        }

        yield productConcat

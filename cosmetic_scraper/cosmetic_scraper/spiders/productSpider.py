import scrapy
import json

param_labels = {
    "Cena": "price",
    "Pojemność": "volume",

}


class ProductSpider(scrapy.Spider):
    name = "products"
    start_urls = json.load((open("_categories_urls.json")))
    # start_urls = ["https://wizaz.pl/kosmetyki/produkt,310005,basiclab-dermocosmetics-famillias-krem-nawilzajacy-do-twarzy-bogata-konsystencja.html"]

    def parse(self, response):
        products_links = response.css("div.products-listing-element a.product-tile")
        yield from response.follow_all(products_links, self.parse_product)

    def parse_product(self, response):
        product = {}
        prod_desc_extras = response.css('div.product-description > div.product-extras')
        for extra in prod_desc_extras:
            columns = extra.css(".column")
            for column in columns:
                label = column.css("span.label::text").get()
                if label == "Pojemność" or label == "Cena":
                    value = column.css("span.value::text").get()
                    product[param_labels[label]] = value

        productConcat = {**product, **{
            "name": response.css('h1[itemprop="name"]::text').get(),
            "ratingValue": response.css('div.product-rating meta[itemprop="ratingValue"]::attr(content)').get(),
            "ratingCount": response.css('div.product-rating meta[itemprop="ratingCount"]::attr(content)').get(),
            "category": response.css('div.product-description div[itemprop="category"] span[itemprop="name"]::text').get(),
            "brand": response.css('div.product-description div[itemprop="brand"] span[itemprop="name"]::text').get(),
            "descriptionHTML": response.css('article.readmore p[itemprop="description"]::text').get(),
            "ingredients": response.css("div#sklad div:last-of-type::text").get(),
            "img": response.css('.product-gallery.gallery img[itemprop="image"]::attr(src)').get(),
            "imgAlt": response.css('.product-gallery.gallery img[itemprop="image"]::attr(alt)').get(),
            "href": response.url,
        }}

        yield productConcat

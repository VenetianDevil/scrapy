import scrapy
import json

param_labels = {
    "Cena": "price",
    "Pojemność": "volume",

}
param_link_labels = {
    "Kategoria": "category",
    "Marka": "brand",
}


class ProductSpider(scrapy.Spider):
    name = "products"
    # start_urls = json.load((open("startUrls/_categories_urls.json")))
    # start_urls = json.load((open("startUrls/catHrefs.json")))
    start_urls = ["https://wizaz.pl/kosmetyki/marka-anwen?page="+str(idx) for idx in range(1, 5)]

    avoid_urls = [prod["href"] for prod in json.load(open("prods_pandas_joined.json")) if
                  not prod["href"] is None] + json.load(open("startUrls/doneLinks.json"))

    def parse(self, response):
        products_links = response.css("div.products-listing-element a.product-tile")
        to_scrape = [prodLink for prodLink in products_links if ("https://wizaz.pl"+prodLink.css("::attr(href)").get())
                     not in self.avoid_urls]
        yield from response.follow_all(to_scrape, self.parse_product)

    def parse_product(self, response):
        if response.url not in self.avoid_urls:
            product = {}
            prod_desc_extras = response.css('div.product-description > div.product-extras')
            for extra in prod_desc_extras:
                columns = extra.css(".column")
                for column in columns:
                    label = column.css("span.label::text").get()
                    if label in param_labels.keys():
                        value = column.css("span.value::text").get()
                        product[param_labels[label]] = value
                    if label in param_link_labels.keys():
                        value = column.css("span.value span::text").get()
                        product[param_link_labels[label]] = value

            productConcat = {**product, **{
                # "name": response.css('h1[itemprop="name"]::text').get(),
                # "ratingValue": response.css('div.product-rating meta[itemprop="ratingValue"]::attr(content)').get(),
                # "ratingCount": response.css('div.product-rating meta[itemprop="ratingCount"]::attr(content)').get(),
                # "category": response.css('div.product-description div[itemprop="category"] span[itemprop="name"]::text').get(),
                # "brand": response.css('div.product-description div[itemprop="brand"] span[itemprop="name"]::text').get(),
                # "descriptionHTML": response.css('article.readmore p[itemprop="description"]::text').get(),
                # "ingredients": response.css("div#sklad div:last-of-type::text").get(),
                # "img": response.css('.product-gallery.gallery img[itemprop="image"]::attr(src)').get(),
                # "imgAlt": response.css('.product-gallery.gallery img[itemprop="image"]::attr(alt)').get(),
                # "href": response.url,
                "name": response.css('article.product-detail header > h1::text').get(),
                "ratingValue": response.css('div.product-rating > strong::text').get(),
                "ratingCount": response.css('div.product-rating small strong > span::text').get(),
                "descriptionHTML": response.css('article.readmore p::text').get(),
                "ingredients": response.css("div#sklad div:last-of-type::text").get(),
                "img": response.css('.product-gallery.gallery img::attr(src)').get(),
                "imgAlt": response.css('.product-gallery.gallery img::attr(alt)').get(),
                "href": response.url,
            }}

            self.avoid_urls.append(response.url)

            yield productConcat

    def closed(self, reason):
        with open("visited.json", "w", encoding="utf8") as outf:
            json.dump(self.avoid_urls, outf, ensure_ascii=False)

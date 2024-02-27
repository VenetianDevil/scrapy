import scrapy

print(scrapy.__version__)


class CategorySpider(scrapy.Spider):
    name = "categories"
    start_urls = [
        "https://wizaz.pl/kosmetyki/makijaz",
    ]
    visited = []

    def parse(self, response):
        mainCat = response.css("div.category-navigation-tree-segment.zero-level-element > a")
        yield from response.follow_all(mainCat, self.parse_subCategory)

    def parse_subCategory(self, response):
        cubCat_divs = response.css("div.category-navigation-tree-segment.zero-level-element div.category-navigation-tree-segment")
        cubCat_links = cubCat_divs.css("a")

        if cubCat_divs[0].css("a::text").get() not in self.visited:
            for subCat in cubCat_divs:
                print("--------------------MOJE SUPER 2 INFO:", subCat.css("a::text").get())
                self.visited.append(subCat.css("a::text").get())
                yield {
                    "name": subCat.css("a::text").get(),
                    "href": subCat.css("a::attr(href)").get(),
                }

            yield from response.follow_all(cubCat_links, self.parse_subCategory)

        print("-------------------ODWIEDZONYCH", len(self.visited))

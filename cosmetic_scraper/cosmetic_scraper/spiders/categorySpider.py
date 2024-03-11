import scrapy


class CategorySpider(scrapy.Spider):
    name = "categories"
    start_urls = [
        "https://wizaz.pl/kosmetyki/makijaz",
    ]
    visited = []

    def parse(self, response):
        depth = 0
        mainCats = response.css("div.category-navigation-tree-segment.zero-level-element > a")
        for mainCat in mainCats:
            self.visited.append(mainCat.css("a::text").get())
            yield {
                "name": mainCat.css("a::text").get(),
                "href": mainCat.css("a::attr(href)").get(),
                "depth": depth,
            }

        yield from response.follow_all(mainCats, self.parse_subCategory, cb_kwargs=dict(depth=depth+1))

    def parse_subCategory(self, response, depth):
        cubCat_divs = response.css(
            "div.category-navigation-tree-segment.zero-level-element div.category-navigation-tree-segment")
        cubCat_links = cubCat_divs.css("a")

        if cubCat_divs[0].css("a::text").get() not in self.visited:
            for subCat in cubCat_divs:
                print("--------------------MOJE SUPER 2 INFO:", subCat.css("a::text").get())
                self.visited.append(subCat.css("a::text").get())
                yield {
                    "name": subCat.css("a::text").get(),
                    "href": subCat.css("a::attr(href)").get(),
                    "parentURL": response.url,
                    "depth": depth,
                }

            yield from response.follow_all(cubCat_links, self.parse_subCategory, cb_kwargs=dict(depth=depth + 1))

        print("-------------------ODWIEDZONYCH", len(self.visited))

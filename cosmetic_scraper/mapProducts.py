import json
import re

categories = json.load(open("catMatchPaths.json", encoding="utf8"))
brands = json.load(open("brands_db.json", encoding="utf8"))
products = json.load(open("products.json", encoding="utf8"))
doneLinks = json.load(open("startUrls/doneLinks.json", encoding="utf8"))
missingLinks = json.load(open("startUrls/lostLinks.json", encoding="utf8")) or []
new_brands = []
new_categories = []
key_order = ["brand_id", "type_id", "category_id", "name", "descriptionHTML", "ingredients", "volume", "unit", "price",
             "currency", "period_of_validity", "img", "imgAlt", "ratingValue", "ratingCount"]


def parse_volume(prod):
    if prod['volume'] is not None:
        # print('volume', prod['volume'], [val for val in re.split(r'^(\d+\s\d+|\d+,\d+|\d+)\s', prod['volume']) if val not in ['', None]])
        volume, unit = [val for val in re.split(r'^(\d+\s\d+|\d+,\d+|\d+)\s', prod['volume']) if val not in ['', None]]
        try:
            prod['volume'] = int(re.sub(r',', '.', volume, count=1))
        except:
            prod['volume'] = float(re.sub(r'\s+', '', re.sub(r',', '.', volume, count=1), count=1))

        prod['unit'] = unit
    return prod


def parse_price(prod):
    if prod['price'] is not None:
        # print('price', [val for val in re.split(r'(^\d+\s\d+,\d+|\d+,\d{2})\s', prod['price']) if val not in ['', None]])
        price, currency = [val for val in re.split(r'(^\d+\s\d+,\d{2}|\d+,\d{2})\s', prod['price']) if val not in ['', None]]
        prod['price'] = float(re.sub(r'\s+', '', re.sub(r',', '.', price, count=1), count=1))
        prod['currency'] = currency
    return prod


def find_cat_id(prod):
    if prod['category'] is not None:
        prod['category'] = prod['category'].strip()
        categoryId = [cat['category_id'] for cat in categories if cat['category'].lower() == prod['category'].lower()]
        if len(categoryId) == 0 and prod['category'] not in new_categories:
            new_categories.append(prod['category'])
        elif len(categoryId) > 0:
            return categoryId[0]


def find_brand_id(prod):
    if prod['brand'] is not None:
        prod['brand'] = prod['brand'].strip()
        brand_id = [brand['brand_id'] for brand in brands if brand['brand'].lower() == prod['brand'].lower()]
        if len(brand_id) == 0 and prod['brand'] not in new_brands:
            new_brands.append(prod['brand'])
        elif len(brand_id) > 0:
            return brand_id[0]
            return brand_id[0]


def map_prods():
    toParse = [prod for prod in products if prod['name'] is not None]
    missingLinksInner = list(set(missingLinks + [prod['href'] for prod in products if prod['name'] is None]))
    prods_sql_ready = ''
    for prod in toParse:
        prod = parse_volume(prod)
        prod = parse_price(prod)
        prod['name'] = prod['name'].strip()
        try:
            prod['ingredients'] = prod['ingredients'].strip()
        except:
            pass

        prod['category_id'] = find_cat_id(prod) or None
        prod['brand_id'] = find_brand_id(prod) or None
        prod['ratingValue'] = float(re.sub(r',', '.', prod['ratingValue'], count=1))
        prod['ratingCount'] = int(prod['ratingCount'])
        if prod['href'] not in doneLinks:
            doneLinks.append(prod['href'])
        if prod['href'] in missingLinksInner:
            missingLinksInner.remove(prod['href'])

        sql_prod = {key: prod.get(key, None) for key in key_order}
        sql_prod['type_id'] = 1000
        split_name = re.split(r',\s', sql_prod['name'], 1)
        if len(split_name) > 1:
            sql_prod['name'] = split_name[1]

        prods_sql_ready += '(' + ", ".join([str(val) if not isinstance(val, str) else '"' + val + '"' for val in
                                            list(sql_prod.values())]) + '),'

    print('NCategories: ', new_categories)
    print('NBrands: ', new_brands)

    with open("parsedProds/batch4.json", "w", encoding="utf-8") as outf:
        json.dump(toParse, outf, ensure_ascii=False)

    with open("parsedProds/sql_batch4.json", "w", encoding="utf-8") as outf:
        json.dump(prods_sql_ready, outf, ensure_ascii=False)

    with open("startUrls/lostLinks.json", "w", encoding="utf-8") as outf:
        json.dump(missingLinksInner, outf, ensure_ascii=False)

    with open("startUrls/doneLinks.json", "w", encoding="utf-8") as outf:
        json.dump(doneLinks, outf, ensure_ascii=False)


map_prods()

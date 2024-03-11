import json


categories = json.load(open("catMatchIdxs.json", encoding="utf8"))


def getHrefArr():
    links = [x['href'] for x in categories]
    print(len(links))

    with open("startUrls/catHrefs.json", "w", encoding="utf-8") as outf:
        json.dump(links, outf, ensure_ascii=False)


getHrefArr()

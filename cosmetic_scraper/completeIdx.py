import json

categories = json.load(open("catMatch.json", encoding="utf8"))


def completeIdxs():
    lastIdx = max([cat['category_id'] for cat in categories if cat['category_id'] is not None])
    print(lastIdx)
    for cat in categories:
        if cat['category_id'] is None:
            lastIdx = lastIdx + 1
            cat['category_id'] = lastIdx

    with open("catMatchIdxs.json", "w", encoding="utf8") as outf:
        json.dump(categories, outf, ensure_ascii=False)


completeIdxs()

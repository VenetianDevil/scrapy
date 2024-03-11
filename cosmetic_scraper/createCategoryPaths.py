import json
# import pandas as pd

categories = json.load(open("catMatchParents.json", encoding="utf8"))


def generatePaths():
    byDepth = sorted(categories, key=lambda x: x['depth'])
    for cat in byDepth:
        if 'path' not in cat:
            cat['path'] = ''
        children = [child for child in categories if child['parent_id'] == cat['category_id']]
        # print(children)
        for child in children:
            child['path'] = cat['path'] + str(cat['category_id']) + "."

    with open("catMatchPaths.json", "w", encoding="utf-8") as outf:
        json.dump(categories, outf, ensure_ascii=False)


generatePaths()

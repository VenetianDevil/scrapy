import json
import itertools
import re

# str = "Lactic Acid, Benzyl Alcohol, Cl 19140 / Yellow 5, Cl 42090 / Blue 1.\r\n\r\n*Z upraw organicznych."
# str_splt = re.split(r",|\r\n", str)
# str_splt = re.sub(r"\.$", " ", str)
# print(len(str_splt), str_splt)

ingred_str = json.load((open("ingredients_str.json", encoding="utf8")))
ingredients = [re.split(r",|\r\n|;", ingStr) for ingStr in ingred_str]
ingredients = list(itertools.chain(*ingredients))
ingredients = [re.sub(r"\.$", "", ingred.strip()) for ingred in ingredients]
print(len(ingredients))

# ingredients = list(dict.fromkeys(ingredients))
ingred_unique = []
testSet = set()
for ing in ingredients:
    temp = ing.lower()
    if temp not in testSet:
        testSet.add(temp)
        ingred_unique.append(ing)

print(len(ingred_unique))

with open("ingredients.json", "w", encoding="utf8") as outf:
    json.dump(ingred_unique, outf, ensure_ascii=False)

# 5985
import json
from pprint import pprint

with open("data/shl_product_catalog_fixed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Type:", type(data))
print("Number of records:", len(data))

print("\nFirst record:")
pprint(data[0])
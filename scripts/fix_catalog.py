import re

input_file = "data/shl_product_catalog.json"
output_file = "data/shl_product_catalog_fixed.json"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Replace newline inside quoted strings like:
# "Microsoft
# 365 (New)"
# -> "Microsoft 365 (New)"
pattern = r'"([^"\n]*)\n([^"\n]*)"'

while re.search(pattern, text):
    text = re.sub(pattern, r'"\1 \2"', text)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed file saved as:", output_file)
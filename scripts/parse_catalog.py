import fitz

pdf_path = "data/shl_product_catalog.pdf"

doc = fitz.open(pdf_path)

print("Pages:", len(doc))

for page in doc:
    text = page.get_text()

    if text.strip():
        print("=" * 80)
        print(text[:800])
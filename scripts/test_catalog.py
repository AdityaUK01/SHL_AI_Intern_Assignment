from app.catalog import SHLCatalog

catalog = SHLCatalog("data/shl_product_catalog_fixed.json")

print("Total Assessments:", catalog.count())

print("\nFirst Assessment:")
print(catalog.get_all()[0]["name"])
from app.catalog import SHLCatalog
from app.retriever import SHLRetriever

catalog = SHLCatalog("data/shl_product_catalog_fixed.json")

retriever = SHLRetriever(
    catalog.get_all()
)

assessments, context = retriever.search(
    "Java developer"
)

print("\nTop Results:\n")

for i, assessment in enumerate(assessments, start=1):

    print("=" * 60)
    print(i)
    print(assessment["name"])
    print(assessment["link"])

print("\nContext Preview:\n")
print(context[:1000])  # print first 1000 characters
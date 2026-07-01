import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading catalog...")

with open("data/shl_product_catalog_fixed.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

documents = []

for assessment in assessments:

    text = f"""
Name: {assessment.get("name","")}

Description:
{assessment.get("description","")}

Categories:
{", ".join(assessment.get("keys", []))}

Duration:
{assessment.get("duration","")}

Job Levels:
{assessment.get("job_levels_raw","")}

Languages:
{assessment.get("languages_raw","")}
"""

    documents.append(text)

print(f"Loaded {len(documents)} assessments")

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True,
    batch_size=16
).astype("float32")

print("Creating FAISS index...")

index = faiss.IndexFlatIP(
    embeddings.shape[1]
)

index.add(embeddings)

faiss.write_index(
    index,
    "data/faiss.index"
)

np.save(
    "data/embeddings.npy",
    embeddings
)

print("\nDone!")

print("Saved:")
print("data/faiss.index")
print("data/embeddings.npy")
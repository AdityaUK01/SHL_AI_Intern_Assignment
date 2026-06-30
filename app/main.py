from fastapi import FastAPI

from app.catalog import SHLCatalog
from app.retriever import SHLRetriever
from app.agent import SHLAgent

from app.schemas import ChatRequest


app = FastAPI(
    title="SHL Assessment Recommender"
)

catalog = SHLCatalog(
    "data/shl_product_catalog_fixed.json"
)

retriever = SHLRetriever(
    catalog.get_all()
)

agent = SHLAgent(
    retriever
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = agent.chat(
        [m.model_dump() for m in request.messages]
    )

    return response
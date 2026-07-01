from fastapi import FastAPI

from app.catalog import SHLCatalog
from app.retriever import SHLRetriever
from app.agent import SHLAgent
from app.schemas import ChatRequest

app = FastAPI(
    title="SHL Assessment Recommender"
)

catalog = None
retriever = None
agent = None


def get_agent():
    global catalog, retriever, agent

    if agent is None:

        print("Initializing SHL Agent...")

        catalog = SHLCatalog(
            "data/shl_product_catalog_fixed.json"
        )

        retriever = SHLRetriever(
            catalog.get_all()
        )

        agent = SHLAgent(
            retriever
        )

        print("SHL Agent Ready!")

    return agent


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    agent = get_agent()

    response = agent.chat(
        [m.model_dump() for m in request.messages]
    )

    return response
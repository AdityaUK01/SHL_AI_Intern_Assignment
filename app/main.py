from fastapi import FastAPI

app = FastAPI(title="SHL Assessment Recommender")


@app.get("/health")
def health():
    return {"status": "ok"}
# SHL Conversational Assessment Recommender

A conversational AI API that recommends relevant SHL assessments based on hiring requirements.

The application uses a Retrieval-Augmented Generation (RAG) pipeline to understand hiring needs, retrieve relevant assessments from the SHL product catalog, and generate grounded recommendations using Google Gemini.

---

## Features

- Conversational hiring assistant
- Multi-turn conversation support
- Clarification questions
- SHL assessment recommendation
- Requirement refinement
- Assessment comparison
- Stateless REST API
- FastAPI + Swagger documentation
- Render deployment

---

## Tech Stack

- Python 3.11+
- FastAPI
- Google Gemini 2.5 Flash
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Render
- GitHub

---

## Project Structure

```
SHL-AI-AGENT
│
├── app
│   ├── agent.py
│   ├── catalog.py
│   ├── comparison.py
│   ├── config.py
│   ├── conversation.py
│   ├── gemini_client.py
│   ├── main.py
│   ├── prompts.py
│   ├── query_builder.py
│   ├── retriever.py
│   ├── schemas.py
│   └── state_extractor.py
│
├── data
│   ├── shl_product_catalog_fixed.json
│   └── shl_product_catalog.pdf
│
├── requirements.txt
├── README.md
└── .env
```

---

# System Architecture

```
User Request

        │

        ▼

Conversation Analyzer

        │

        ▼

Conversation State Extraction

        │

        ▼

Query Builder

        │

        ▼

TF-IDF Retrieval

        │

        ▼

Cosine Similarity Ranking

        │

        ▼

Relevant SHL Assessments

        │

        ▼

Google Gemini 2.5 Flash

        │

        ▼

Final Response
```

---

# API Endpoints

## Health Check

GET

```
/health
```

Example

```json
{
  "status": "ok"
}
```

---

## Chat Endpoint

POST

```
/chat
```

Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer who works with stakeholders"
    },
    {
      "role": "assistant",
      "content": "Sure. What is seniority level?"
    },
    {
      "role": "user",
      "content": "Mid-level, around 4 years"
    }
  ]
}
```

Example Response

```json
{
  "reply": "Based on your hiring requirements, here are the recommended SHL assessments.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://...",
      "test_type": "Knowledge"
    }
  ],
  "end_of_conversation": false
}
```

---

# Retrieval Pipeline

Instead of using a vector database, the final implementation uses a lightweight retrieval pipeline based on TF-IDF.

Steps:

1. Load SHL catalog
2. Build searchable documents
3. Generate TF-IDF vectors
4. Calculate cosine similarity
5. Retrieve top matching assessments
6. Pass retrieved context to Gemini
7. Generate grounded recommendations

This approach significantly reduces memory usage while maintaining relevant recommendations.

---

# Prompt Design

The LLM is instructed to:

- Recommend only assessments present in the SHL catalog
- Never invent assessment names
- Never invent URLs
- Explain why each recommendation fits
- Ask clarification questions when needed
- Compare only retrieved assessments
- Generate grounded responses

---

# Challenges Faced

## Initial Retrieval

The project initially used:

- SentenceTransformer
- FAISS

Although semantic retrieval produced good results, deployment on Render Free repeatedly failed because of memory limitations.

Common deployment errors included:

- Out of memory (512MB limit)
- No open ports detected
- Application startup failures

The retrieval system was redesigned using TF-IDF and cosine similarity to make deployment stable.

---

## Dependency Issues

During deployment several package installation issues occurred, including pandas metadata generation failures.

These were resolved by:

- updating dependency versions
- simplifying requirements
- rebuilding the deployment environment

---

## SHL Catalog Cleaning

The provided SHL catalog contained inconsistencies such as:

- duplicate entries
- missing values
- inconsistent formatting
- inconsistent URLs

The catalog was cleaned before building the retrieval pipeline.

---

## Gemini API Limits

Google Gemini Free Tier occasionally returned:

```
429 RESOURCE_EXHAUSTED
```

Graceful error handling was added so the application can continue returning retrieved recommendations instead of crashing.

---

# Running Locally

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

# Deployment

The application is deployed on Render.

Base URL

```
https://shl-ai-agent-pnkc.onrender.com
```

Swagger Documentation

```
https://shl-ai-agent-pnkc.onrender.com/docs
```

Health Endpoint

```
https://shl-ai-agent-pnkc.onrender.com/health
```

---

# Future Improvements

- Hybrid Retrieval (TF-IDF + Dense Embeddings)
- Better ranking model
- Conversation memory
- Vector database
- Caching
- Improved evaluation metrics
- Streaming responses

---

# Author

**Aditya Rawat**

GitHub

https://github.com/AdityaUK01

---

# License

This project was developed as part of the SHL AI Internship Assignment.
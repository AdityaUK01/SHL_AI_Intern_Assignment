# SHL Conversational Assessment Recommender

A conversational AI API that recommends relevant SHL assessments based on hiring requirements.

The project uses a lightweight Retrieval-Augmented Generation (RAG) pipeline to understand hiring needs, retrieve relevant assessments from the SHL product catalog, and generate grounded recommendations using Google Gemini.

The application supports multi-turn conversations, asks clarification questions when needed, and recommends only assessments available in the official SHL catalog.

---

## Features

- Conversational hiring assistant
- Multi-turn conversation support
- Requirement refinement through follow-up questions
- SHL assessment recommendations
- Assessment comparison
- Retrieval-Augmented Generation (RAG)
- Stateless REST API
- FastAPI with automatic Swagger documentation
- Deployable on Render

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| Framework | FastAPI |
| LLM | Google Gemini 2.5 Flash |
| Retrieval | TF-IDF |
| Similarity Search | Cosine Similarity |
| Machine Learning | Scikit-learn |
| Deployment | Render |
| Version Control | Git & GitHub |

---

## Project Structure

```text
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
        Conversation Analysis
                     │
                     ▼
      Conversation State Extraction
                     │
                     ▼
            Query Builder
                     │
                     ▼
          TF-IDF Vector Search
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
        Grounded AI Response
```

---

# How It Works

1. User sends hiring requirements.
2. Conversation history is analyzed.
3. Missing information is identified.
4. A search query is generated.
5. TF-IDF retrieves relevant assessments.
6. Cosine similarity ranks the best matches.
7. Retrieved assessments are provided to Gemini.
8. Gemini generates a grounded recommendation using only retrieved assessments.

---

# API Endpoints

## Health Check

**GET**

```
/health
```

Example Response

```json
{
  "status": "ok"
}
```

---

## Chat

**POST**

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
      "content": "Sure. What is the seniority level?"
    },
    {
      "role": "user",
      "content": "Mid-level with around 4 years of experience."
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

The application uses a lightweight Retrieval-Augmented Generation (RAG) pipeline without relying on a vector database.

### Retrieval Steps

1. Load the SHL assessment catalog
2. Build searchable documents
3. Generate TF-IDF vectors
4. Compute cosine similarity
5. Retrieve top matching assessments
6. Pass retrieved context to Gemini
7. Generate grounded recommendations

This approach provides fast retrieval while keeping memory usage low enough for deployment on Render's free tier.

---

# Prompt Design

The Gemini prompt is designed to ensure reliable recommendations by instructing the model to:

- Recommend only assessments available in the SHL catalog
- Never invent assessment names
- Never generate fake URLs
- Explain why each assessment matches the hiring requirements
- Ask clarification questions when information is incomplete
- Compare only retrieved assessments
- Generate grounded responses based on retrieved context

---

# Challenges Faced

## 1. Retrieval System

The initial implementation used:

- SentenceTransformers
- FAISS

Although semantic retrieval performed well, deployment on Render Free repeatedly failed due to the 512 MB memory limit.

Common issues included:

- Out-of-memory errors
- Startup failures
- No open ports detected

The retrieval pipeline was redesigned using TF-IDF and cosine similarity, resulting in a lightweight and stable deployment.

---

## 2. Dependency Management

Several deployment failures occurred because of package compatibility issues, including pandas metadata generation errors.

These were resolved by:

- Updating package versions
- Simplifying dependencies
- Rebuilding the deployment environment

---

## 3. SHL Catalog Cleaning

The provided SHL catalog required preprocessing before retrieval.

The cleaning process included:

- Removing duplicate entries
- Handling missing values
- Fixing inconsistent formatting
- Correcting invalid URLs

---

## 4. Gemini Rate Limits

The Google Gemini Free Tier occasionally returned:

```
429 RESOURCE_EXHAUSTED
```

Graceful fallback handling was implemented so that retrieved assessment recommendations are still returned even when Gemini is temporarily unavailable.

---

# Running Locally

## Clone the Repository

```bash
git clone https://github.com/AdityaUK01/SHL_AI_Intern_Assignment
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

## Run the Server

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# Deployment

### Base URL

```
https://shl-ai-agent-pnkc.onrender.com
```

### Swagger UI

```
https://shl-ai-agent-pnkc.onrender.com/docs
```

### Health Endpoint

```
https://shl-ai-agent-pnkc.onrender.com/health
```

---

# Future Improvements

- Hybrid retrieval (TF-IDF + dense embeddings)
- Better ranking models
- Conversation memory
- Vector database integration
- Response caching
- Retrieval evaluation metrics
- Streaming responses
- Authentication and rate limiting

---

# Author

**Aditya Rawat**

GitHub

https://github.com/AdityaUK01

---

# License

This project was developed as part of the SHL AI Internship Assignment.
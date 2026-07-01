# SHL AI Assessment Recommendation Agent

An AI-powered assistant that recommends SHL assessments based on job roles, skills, and hiring requirements using semantic search and Google Gemini.

## Features

- AI-powered assessment recommendations
- Multi-turn conversation support
- Assessment comparison
- Personality assessment recommendations
- Semantic search using FAISS
- FastAPI REST API
- Google Gemini integration

## Tech Stack

- Python
- FastAPI
- FAISS
- Sentence Transformers
- Google Gemini
- Uvicorn

## Installation

Clone the repository:

```bash
git clone https://github.com/AdityaUK01/shl-ai-agent.git
cd shl-ai-agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application:

```bash
uvicorn app.main:app --reload
```

## API

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

Health Check:

```
GET /health
```

Chat Endpoint:

```
POST /chat
```

## Project Structure

```
app/
data/
scripts/
requirements.txt
README.md
```

## Author

**Aditya Rawat**


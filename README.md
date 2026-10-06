# AI Trekking & Tourism Assistant

**Final Year Project | Amrit Science Campus (ASCOL), Tribhuvan University**

> A locally run, LLM-powered travel assistant that turns a simple question into a step-by-step, weather-aware trekking itinerary, grounded in a curated and updatable knowledge base.

**Repositories**

| Part | Repository |
|------|------------|
| Backend (LLM agent, RAG, tools) | https://github.com/niss21/FinalYearProject_ASCOL |
| Frontend (Next.js web app) | https://github.com/pasanglama14/Final-Year-Project |

---

## Table of Contents

1. [Overview](#overview)
2. [Problem Statement](#problem-statement)
3. [Objectives](#objectives)
4. [Key Features](#key-features)
5. [How It Works](#how-it-works)
6. [Tech Stack](#tech-stack)
7. [Project Structure](#project-structure)
8. [Getting Started](#getting-started)
9. [Example Usage](#example-usage)
10. [Project Status](#project-status)
11. [Roadmap](#roadmap)
12. [Team & Contributions](#team--contributions)
13. [Acknowledgements](#acknowledgements)

---

## Overview

Planning a trek in a mountainous region is hard. Trail conditions, weather, permits, lodges and costs change constantly, and reliable information is scattered across blogs, forums and outdated guidebooks.

This project is a web-based tourism assistant that brings these pieces together. A user asks a question in plain language, such as *"Plan a 10-day trek for me in October on a moderate budget"*. A locally running language model (**Phi-3 Mini**) understands the request, decides what information it needs, fetches **live weather data**, retrieves **up-to-date destination information** from a curated knowledge base, and produces a **personalised, step-by-step itinerary** with cost estimates and permit/visa guidance.

Because the language model runs **on-device**, the system keeps user queries private and does not depend on paid cloud LLM APIs, which makes it practical for low-resource and offline-first settings.

## Problem Statement

- Trekking information is **fragmented** across many sources and often **outdated** (routes get rerouted, lodges open and close, permit rules change).
- Generic chatbots tend to **hallucinate** specifics such as distances, prices and permit rules.
- Cloud-only AI tools require **constant connectivity** and send user data to third parties.
- Local guides, lodge owners and experienced trekkers hold **the freshest knowledge**, but have no simple way to contribute it.

## Objectives

1. Build an **AI travel assistant** that recommends destinations, generates itineraries and estimates budgets.
2. Ground the model's answers in a **maintained knowledge base** (RAG) to reduce hallucination.
3. Make plans **context-aware** by integrating **real-time weather** data.
4. Run the core language model **locally**, with no dependency on paid LLM APIs.
5. Provide a **clean, interactive web interface** for travellers.
6. *(Upcoming)* Create a **community-driven update system** where relevant people (guides, lodge owners, experienced trekkers) can keep the knowledge base current and earn **reward points**.

## Key Features

- **Conversational trip planning**: ask in natural language and receive a structured plan.
- **RAG-based destination recommendation**: Phi-3 Mini combined with a vector database (Chroma / FAISS) matches user queries to trekking data.
- **Agentic tool use**: the LLM decides *when* to call a tool. If weather matters, it calls the weather tool itself. Asking about two cities simply results in two calls, with no hard-coded path.
- **Live weather integration** via the Open-Meteo API.
- **Fine-tuned itinerary and budget planner** trained on scraped travel datasets, producing detailed day-by-day plans, cost breakdowns, and visa/permit requirement summaries.
- **Local-first LLM**: private and cost-free inference.
- **Interactive Next.js frontend** for a smooth user experience.

## How It Works

The backend follows an **agent loop** pattern: the LLM either answers directly or asks the harness to run a tool, receives the result, and continues until it can give a final answer.

<img width="817" height="343" alt="image" src="https://github.com/user-attachments/assets/6e148e54-fe63-4246-9b58-a33d8b17d30e" />


The knowledge base (Chroma / FAISS) sits alongside this loop. The LLM retrieves the latest route, stay, permit and cost information from it, in addition to calling the weather tool.

**Step by step**

1. The user submits a question through the Next.js frontend.
2. The backend passes it, along with a system prompt, to **Phi-3 Mini**.
3. The LLM decides what it needs:
   - **Knowledge base lookup**: relevant, recent destination information is retrieved from the vector store (RAG).
   - **Weather tool call**: `get_weather(city)` fetches forecasts from Open-Meteo.
4. Tool results are returned to the LLM, and the loop repeats if more information is required.
5. The LLM combines its reasoning, the weather data and the retrieved knowledge into a **final, tailored itinerary**.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language model** | Phi-3 Mini (run locally) |
| **Retrieval (RAG)** | Chroma / FAISS vector databases, embeddings model *(fill in)* |
| **Fine-tuning** | Fine-tuned on scraped travel datasets for itineraries & budgets *(add method, e.g. LoRA/QLoRA, if applicable)* |
| **Tools / APIs** | Open-Meteo Weather API |
| **Backend** | Python *(add framework, e.g. FastAPI / Flask)* |
| **Frontend** | Next.js (React), *(add styling lib, e.g. Tailwind CSS)* |
| **Data collection** | Web scraping for travel datasets *(add libraries)* |
| **Version control** | Git & GitHub |

## Project Structure

> Replace with your actual folder layout.

```
FinalYearProject_ASCOL/        # Backend
├── app/ or src/               # API & agent loop
├── tools/                     # get_weather and other tools
├── knowledge_base/            # destination data + vector store
├── data/                      # scraped / training datasets
├── finetune/                  # fine-tuning scripts & notebooks
├── requirements.txt
└── README.md

Final-Year-Project/            # Frontend
├── app/ or pages/             # Next.js routes
├── components/                # UI components
├── public/
├── package.json
└── README.md
```

## Getting Started

### Prerequisites

- **Python** and `pip`
- **Node.js** ` and `npm` / `yarn`
- **Git**
- A machine able to run Phi-3 Mini locally (recommended: `<RAM>` GB RAM, optional GPU)
- A local LLM runtime such as `<Ollama / llama.cpp / Hugging Face Transformers>`

### 1. Clone both repositories

```bash
git clone https://github.com/niss21/FinalYearProject_ASCOL.git
git clone https://github.com/pasanglama14/Final-Year-Project.git
```

### 2. Run the backend

```bash
cd FinalYearProject_ASCOL

# (optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# download / prepare the model
<command to pull or load Phi-3 Mini>

# build or load the knowledge base
<command to build the vector store>

# start the server
<command to start the backend, e.g. uvicorn app.main:app --reload>
```

The backend should now be running at `http://localhost:<PORT>`.

### 3. Run the frontend

```bash
cd Final-Year-Project

npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

### 4. Configuration

Create a `.env` file (see `.env.example` if provided):

```env
BACKEND_URL=http://localhost:<PORT>
# Open-Meteo does not require an API key for basic usage
```

## Example Usage

**User:**
> I want a 7-day trek in Nepal in late October with a medium budget. What should I pack and what permits do I need?

**Assistant (summarised output):**
- **Recommended route** based on knowledge-base entries and the season
- **Day-by-day itinerary** with distance/altitude and suggested stays
- **Weather outlook** for the trek dates from Open-Meteo
- **Estimated budget** broken down into accommodation, food, transport and permits
- **Permit & visa summary** with required documents

## Project Status

| Component | Status |
|-----------|--------|
| Local LLM integration (Phi-3 Mini) | ✅ Done |
| Prompting & agent loop (LLM → tool → result → answer) | ✅ Done |
| Weather tool integration (Open-Meteo) | ✅ Done |
| RAG pipeline with vector DB (Chroma / FAISS) | ✅ Done |
| Knowledge base of trekking destinations | ✅ Initial version |
| Fine-tuned itinerary & budget planner | ✅ Done |
| Visa / permit requirement summaries | ✅ Done |
| Next.js frontend (chat UI) | ✅ Done |
| Frontend ↔ backend integration | ✅ Done *(confirm)* |
| **Community knowledge-base updates** | 🚧 **Planned** |
| **Contributor reward points** | 🚧 **Planned** |
| Evaluation of answer quality | 🚧 Planned |

## Roadmap

The main remaining milestone is turning the knowledge base from a static dataset into a **living, community-maintained resource**.

- [ ] **Knowledge-base update interface**: a form/dashboard where authorised users can add or edit route changes, hotels and lodges, permit rules, prices and trail conditions.
- [ ] **Contributor roles & verification**: a review or moderation flow (guides, lodge owners, trekkers, admins) so only trustworthy updates are published.
- [ ] **Reward points system**: contributors earn points for accepted updates, encouraging fresh and accurate data.
- [ ] **Automatic re-indexing**: approved updates are embedded and added to the vector store without a full rebuild.
- [ ] **Timestamps & freshness scoring**: prefer the most recent information when generating itineraries.
- [ ] **Evaluation**: measure itinerary accuracy and hallucination rate with and without RAG.
- [ ] **More destinations & languages**: expand coverage beyond the initial regions.
- [ ] **Offline-friendly deployment**: package the app for use in low-connectivity areas.

## Team & Contributions

| Contributor | Role |
|-------------|------|
| **Pem Sherpa** ([@niss21](https://github.com/niss21)) | LLM integration, RAG pipeline, agent loop, weather tool, fine-tuning, backend |
| **Pasang Lama** ([@pasanglama14](https://github.com/pasanglama14)) | Frontend development (Next.js) |
| **Prabin Pokhrel** | Frontend development (Next.js) |


## Acknowledgements

- [Microsoft Phi-3](https://huggingface.co/microsoft) for the compact open language model
- [Open-Meteo](https://open-meteo.com/) for the free weather API
- [Chroma](https://www.trychroma.com/) and [FAISS](https://github.com/facebookresearch/faiss) for vector search
- Amrit Science Campus (ASCOL), Tribhuvan University, and our supervisors for their guidance on this final year project

**Related post:** [LinkedIn project announcement](https://www.linkedin.com/feed/update/urn:li:activity:7396907326051479552/)

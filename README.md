# 🌍 AI Trip Planner
https://ai-trip-planner-epjm.onrender.com/health
> An agentic AI travel-planning application built with **LangGraph, LangChain, FastAPI, Streamlit, and Groq**, with external tools for travel research, places discovery, and trip-related calculations.

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-orange.svg)](https://www.langchain.com/langgraph)
[![Groq](https://img.shields.io/badge/LLM-Groq-purple.svg)](https://groq.com/)
[![uv](https://img.shields.io/badge/Package_Manager-uv-blueviolet.svg)](https://docs.astral.sh/uv/)

---

## 📌 Overview

**AI Trip Planner** is an agentic travel-planning application that converts a natural-language travel request into an AI-generated travel plan.

Instead of implementing the application as a single LLM call, the project separates the system into:

* A **Streamlit conversational frontend**
* A **FastAPI backend**
* A **LangGraph-based agent workflow**
* Specialized external tools
* An LLM provider abstraction
* Prompt management
* Configuration and environment management
* Error handling and logging utilities

A typical request looks like:

```text
Plan a 5-day trip to Goa for two people.
```

The request flows through the system:

```text
User
  │
  ▼
Streamlit UI
  │
  │ POST /query
  ▼
FastAPI Backend
  │
  ▼
GraphBuilder
  │
  ▼
LangGraph Agent
  │
  ├── LLM
  ├── Search / Research Tools
  ├── Places Tools
  ├── Weather / Travel Tools
  └── Calculation Tools
  │
  ▼
Final Travel Plan
  │
  ▼
FastAPI JSON Response
  │
  ▼
Streamlit UI
```

The repository contains dedicated modules for the agent, tools, configuration, prompts, exceptions, logging, utilities, and the `ai_trip_planner` package.

---

# ✨ Key Features

## 🤖 Agentic Travel Planning

The application uses **LangGraph** to orchestrate the travel-planning workflow.

The backend constructs the graph through:

```python
graph = GraphBuilder(model_provider="groq")
react_app = graph()
```

The graph then processes the user request and returns the final response.

This allows the application to move beyond a simple:

```text
Prompt → LLM → Answer
```

architecture toward:

```text
Prompt
   ↓
Agent
   ↓
Reason about task
   ↓
Select appropriate tools
   ↓
Collect external information
   ↓
Synthesize results
   ↓
Generate final itinerary
```

---

# 🧠 LangGraph Architecture

The core orchestration layer is implemented around a graph-based agent architecture.

Conceptually:

```text
                 ┌───────────────────┐
                 │   User Question   │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   Agent / Graph   │
                 └─────────┬─────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Search        Places       Utilities
           Tools         Tools         Tools
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │  LLM Synthesis    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Travel Itinerary  │
                 └───────────────────┘
```

The generated graph is also exported to:

```text
my_graph.png
```

The FastAPI backend generates this graph visualization from the compiled LangGraph application.

---

# 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                              │
│                                                             │
│                    Streamlit Application                    │
│                    streamlit_app.py                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ HTTP POST /query
                               │ JSON
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                         API LAYER                            │
│                                                             │
│                       FastAPI                               │
│                       main.py                               │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ POST /query                                           │  │
│  │                                                       │  │
│  │ QueryRequest                                          │  │
│  │       ↓                                               │  │
│  │ GraphBuilder(model_provider="groq")                   │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      AGENT LAYER                            │
│                                                             │
│                       LangGraph                             │
│                                                             │
│              Agentic Workflow / Graph                      │
│                         │                                   │
│          ┌──────────────┼──────────────┐                   │
│          ▼              ▼              ▼                   │
│       Search          Places       Calculators             │
│        Tools           Tools          Tools                │
└──────────┬──────────────┬──────────────┬────────────────────┘
           │              │              │
           ▼              ▼              ▼
      External APIs   Google APIs    Local Utilities
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                        LLM LAYER                            │
│                                                             │
│                         Groq                                │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
                    Final AI Travel Plan
```

---

# 🧰 Technology Stack

| Technology     | Responsibility                        |
| -------------- | ------------------------------------- |
| Python 3.14+   | Application runtime                   |
| FastAPI        | Backend REST API                      |
| Uvicorn        | ASGI server                           |
| Streamlit      | Interactive frontend                  |
| LangChain      | LLM/tool integration                  |
| LangGraph      | Agent orchestration                   |
| LangChain Groq | Groq integration                      |
| Groq           | LLM inference                         |
| Tavily         | Web/search capabilities               |
| Google Places  | Location/place discovery              |
| Pydantic       | Request validation                    |
| python-dotenv  | Environment configuration             |
| uv             | Python package/environment management |

The current `pyproject.toml` declares Python `>=3.14` and dependencies including FastAPI, LangChain, LangChain Community, Google Places integration, LangChain Groq, LangChain OpenAI, LangChain Tavily, LangGraph, python-dotenv, Streamlit, and Uvicorn.

---

# 📁 Project Structure

```text
AI_Trip_planner/
│
├── agent/
│   └── agentic_workflow.py
│       └── LangGraph agent / workflow construction
│
├── config/
│   └── Application configuration
│
├── exception/
│   └── Custom exception handling
│
├── logger/
│   └── Application logging utilities
│
├── notebook/
│   └── Experiments and development notebooks
│
├── prompt_library/
│   └── Prompt templates / LLM instructions
│
├── src/
│   └── ai_trip_planner/
│       └── Python package
│
├── tools/
│   └── External and agent tools
│
├── utils/
│   └── Utility modules
│
├── main.py
│   └── FastAPI application
│
├── streamlit_app.py
│   └── Streamlit frontend
│
├── my_graph.png
│   └── Generated LangGraph visualization
│
├── pyproject.toml
│   └── Project metadata and dependencies
│
├── uv.lock
│   └── Locked dependency graph
│
├── requirements.txt
│   └── Alternative dependency installation file
│
├── setup.py
│   └── Package setup
│
├── .python-version
│   └── Python version configuration
│
├── .gitignore
│   └── Git exclusions
│
└── README.md
```

The current repository structure contains these modules and configuration files.

---

# 🔌 API Architecture

The application exposes a FastAPI endpoint:

```http
POST /query
```

The request schema is:

```json
{
  "question": "Plan a 5 day trip to Goa"
}
```

The backend validates the request using Pydantic:

```python
class QueryRequest(BaseModel):
    question: str
```

The endpoint then constructs the LangGraph workflow and invokes it.

---

# 📡 API Example

### Request

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Plan a 5-day trip to Goa for two people"
  }'
```

### Response

```json
{
  "answer": "## Goa 5-Day Travel Plan\n..."
}
```

The backend returns the final agent response under the `answer` field.

---

# 🖥️ Streamlit Frontend

The Streamlit application is implemented in:

```text
streamlit_app.py
```

The frontend:

1. Displays the travel-planning interface.
2. Accepts natural-language user input.
3. Sends the request to the FastAPI backend.
4. Displays a loading state.
5. Parses the JSON response.
6. Renders the generated itinerary as Markdown.

The frontend currently communicates with:

```text
http://localhost:8000
```

through:

```text
POST /query
```

---

# 🚀 Getting Started

## Prerequisites

Install:

* Python 3.14+
* Git
* `uv`
* API credentials for the configured external services

The project currently declares Python `>=3.14`.

---

# 1. Clone the Repository

```bash
git clone https://github.com/MadhuriTeli/AI_Trip_planner.git
cd AI_Trip_planner
```

---

# 2. Install `uv`

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal or reload your shell configuration.

Verify:

```bash
uv --version
```

### Alternative

```bash
pip install uv
```

Verify:

```bash
uv --version
```

---

# 3. Create the Virtual Environment

Because this project targets Python 3.14:

```bash
uv venv --python 3.14
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

---

# 4. Install Dependencies

Recommended:

```bash
uv sync
```

This uses:

```text
pyproject.toml
uv.lock
```

to construct the development environment.

Alternatively:

```bash
uv pip install -r requirements.txt
```

---

# 5. Verify Python

```bash
python --version
```

Expected:

```text
Python 3.14.x
```

Verify uv's environment:

```bash
uv pip list
```

---

# 🔐 Environment Configuration

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
GPLACES_API_KEY=your_google_places_api_key
```

Depending on the tools enabled in your current workflow, additional environment variables may be required.

The application loads environment variables using:

```python
from dotenv import load_dotenv

load_dotenv()
```

### Never commit `.env`

Make sure `.gitignore` contains:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```

---

# 🔑 Verify Environment Variables

You can verify that the variables are loaded without printing the secrets:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('GROQ:', bool(os.getenv('GROQ_API_KEY'))); print('TAVILY:', bool(os.getenv('TAVILY_API_KEY'))); print('GOOGLE PLACES:', bool(os.getenv('GPLACES_API_KEY')))"
```

Expected:

```text
GROQ: True
TAVILY: True
GOOGLE PLACES: True
```

Never print the full API keys.

---

# ▶️ Running the Application

The application consists of two processes:

```text
FastAPI Backend
      +
Streamlit Frontend
```

Both need to be running.

---

## Terminal 1 — Start FastAPI

Activate the environment:

```bash
source .venv/bin/activate
```

Then:

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

Alternative ReDoc:

```text
http://localhost:8000/redoc
```

The current backend uses FastAPI and exposes `POST /query`.

---

## Terminal 2 — Start Streamlit

Activate the same environment:

```bash
source .venv/bin/activate
```

Run:

```bash
streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

The current Streamlit application uses `http://localhost:8000` as its backend URL.

---

# 🧪 Health Check

Before opening Streamlit, verify that FastAPI is running:

```bash
curl http://localhost:8000/docs
```

Or open:

```text
http://localhost:8000/docs
```

Then test the API directly:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"Plan a 3-day trip to Pune"}'
```

If this returns an `answer`, the backend and agent pipeline are functioning.

---

# 🧠 Agent Workflow

The backend currently creates the graph for each query:

```python
graph = GraphBuilder(model_provider="groq")
react_app = graph()
```

The user's question is then converted into the graph input:

```python
messages = {
    "messages": [query.question]
}
```

and executed:

```python
output = react_app.invoke(messages)
```

The final message is extracted from the graph result.

Conceptually:

```text
User Question
      │
      ▼
QueryRequest
      │
      ▼
GraphBuilder
      │
      ▼
LangGraph
      │
      ├───────────────┐
      │               │
      ▼               ▼
    LLM             Tools
      │               │
      └───────┬───────┘
              ▼
        Agent reasoning
              │
              ▼
       Final AI response
```

---

# 🛠️ Tooling Layer

The repository has a dedicated:

```text
tools/
```

package for agent tools.

This allows the agent to interact with external systems instead of relying exclusively on LLM knowledge.

Typical responsibilities include:

```text
Search / web research
Places / location lookup
Travel information
Weather-related information
Expense calculations
```

This design provides a clean boundary:

```text
LLM
 ↓
Tool selection
 ↓
External system
 ↓
Tool result
 ↓
LLM synthesis
```

---

# 🌐 External Integrations

## Groq

Used as the LLM provider.

Environment variable:

```env
GROQ_API_KEY=...
```

The backend explicitly initializes the agent workflow with:

```python
GraphBuilder(model_provider="groq")
```

---

## Tavily

Tavily provides search capabilities for agent-driven web research.

Environment variable:

```env
TAVILY_API_KEY=...
```

The project declares `langchain-tavily` as a dependency.

---

## Google Places

The project includes LangChain's Google Community Places integration.

Environment variable:

```env
GPLACES_API_KEY=...
```

The dependency is declared as:

```text
langchain-google-community[places]
```

---

# 🧾 Error Handling

The FastAPI layer catches workflow errors and converts them into HTTP 500 responses:

```python
except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"error": str(e)}
    )
```

This prevents unhandled backend exceptions from directly crashing the API process.

The Streamlit layer should display frontend failures using:

```python
except Exception as e:
    st.error(f"The response failed due to: {e}")
    st.stop()
```

rather than:

```python
raise f"The response failed due to {e}"
```

A string cannot be raised as a Python exception.

---

# 🐛 Troubleshooting

## `TypeError: exceptions must derive from BaseException`

If you see:

```text
TypeError: exceptions must derive from BaseException
```

check `streamlit_app.py`.

Incorrect:

```python
raise f"The response failed due to {e}"
```

Correct:

```python
st.error(f"The response failed due to: {e}")
st.stop()
```

---

## `Connection refused`

If Streamlit reports that it cannot connect to:

```text
http://localhost:8000
```

start FastAPI:

```bash
uvicorn main:app --reload --port 8000
```

Then verify:

```bash
curl http://localhost:8000/docs
```

---

## `GROQ_API_KEY` missing

Check:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(bool(os.getenv('GROQ_API_KEY')))"
```

If it prints:

```text
False
```

check `.env`.

---

## `TAVILY_API_KEY` missing

Check:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(bool(os.getenv('TAVILY_API_KEY')))"
```

---

## Google Places API error

Verify:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(bool(os.getenv('GPLACES_API_KEY')))"
```

Also confirm that the required Google Places API is enabled for the associated project.

---

# 🧪 Testing the Backend Independently

Testing the backend separately from Streamlit makes debugging significantly easier.

Start FastAPI:

```bash
uvicorn main:app --reload --port 8000
```

Then:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"Plan a 5 day trip to Goa"}'
```

If the API works but Streamlit doesn't, the issue is likely in the frontend/API integration rather than the agent.

---

# 🔍 Debugging Strategy

When debugging the application, isolate the system layer by layer.

### Layer 1 — Environment

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(bool(os.getenv('GROQ_API_KEY')))"
```

### Layer 2 — Python imports

```bash
python -c "import fastapi, streamlit, langchain, langgraph; print('Imports OK')"
```

### Layer 3 — FastAPI

```bash
uvicorn main:app --reload --port 8000
```

### Layer 4 — API

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Plan a trip to Goa"}'
```

### Layer 5 — Streamlit

```bash
streamlit run streamlit_app.py
```

This isolates:

```text
Configuration
    ↓
Dependencies
    ↓
Backend
    ↓
Agent
    ↓
External tools
    ↓
Frontend
```

---

# 📦 Dependency Management

The project uses `pyproject.toml` and `uv.lock`.

The preferred workflow is:

```bash
uv sync
```

To add a dependency:

```bash
uv add <package>
```

Example:

```bash
uv add httpx
```

To remove one:

```bash
uv remove <package>
```

To inspect installed dependencies:

```bash
uv pip list
```

To inspect available Python versions:

```bash
uv python list
```

The project also contains `requirements.txt` and `setup.py` for compatibility with alternative Python workflows.

---

# 🔄 Rebuild the Environment

If the environment becomes corrupted:

```bash
rm -rf .venv
```

Recreate:

```bash
uv venv --python 3.14
```

Activate:

```bash
source .venv/bin/activate
```

Install:

```bash
uv sync
```

Run:

```bash
uvicorn main:app --reload --port 8000
```

and in another terminal:

```bash
streamlit run streamlit_app.py
```

---

# 🧹 Useful Development Commands

### Check Python

```bash
python --version
```

### Check uv

```bash
uv --version
```

### List packages

```bash
uv pip list
```

### Check project dependencies

```bash
uv tree
```

### Check Git state

```bash
git status
```

### View recent commits

```bash
git log --oneline --decorate --graph -10
```

### Find Python files

```bash
find . -name "*.py" -not -path "./.venv/*"
```

---

# 🧑‍💻 Recommended Development Workflow

```text
1. Create feature branch
        ↓
2. Update code
        ↓
3. Run backend
        ↓
4. Test /query directly
        ↓
5. Run Streamlit
        ↓
6. Test end-to-end flow
        ↓
7. Run static checks/tests
        ↓
8. Review secrets
        ↓
9. Commit
        ↓
10. Push branch
```

Create a feature branch:

```bash
git checkout -b feature/<feature-name>
```

Example:

```bash
git checkout -b feature/travel-budget-tool
```

Commit:

```bash
git add .
git commit -m "feat: add travel budget calculation"
```

Push:

```bash
git push origin feature/travel-budget-tool
```

---

# 🔐 Security Considerations

## Never commit API keys

Never put credentials directly in Python:

```python
GROQ_API_KEY = "gsk_..."
```

Use:

```env
GROQ_API_KEY=...
```

and:

```python
os.getenv("GROQ_API_KEY")
```

---

## CORS

The current FastAPI application allows all origins:

```python
allow_origins=["*"]
```

This is convenient during local development but should be restricted for production.

For example:

```python
allow_origins=[
    "https://your-production-domain.com"
]
```

The current repository itself notes that the wildcard configuration should be made specific in production.

---

# 🏭 Production Considerations

The current project is primarily a development/demo architecture.

For production, the following improvements would be recommended.

## API Layer

* Restrict CORS
* Add authentication
* Add request IDs
* Add structured logging
* Add request timeouts
* Add rate limiting
* Add API versioning
* Add health/readiness endpoints

---

## Agent Layer

* Compile the graph once rather than rebuilding it for every request
* Add explicit tool timeouts
* Add retries for transient API failures
* Add fallback models/providers
* Add structured agent state
* Add maximum iteration limits
* Add tracing/observability
* Add LLM evaluation

---

## Tool Layer

External APIs should have:

```text
Timeout
Retry policy
Rate-limit handling
Validation
Structured errors
Caching
```

A production tool interface could look like:

```text
Agent
  │
  ▼
Tool Router
  │
  ├── SearchTool
  ├── PlacesTool
  ├── WeatherTool
  └── ExpenseTool
          │
          ▼
     External APIs
```

---

# 📈 Observability

For a production-grade agentic system, track:

### Request metrics

```text
Request count
Request latency
Error rate
HTTP status
```

### LLM metrics

```text
Model
Prompt tokens
Completion tokens
Total tokens
Latency
Cost
Failures
```

### Agent metrics

```text
Graph execution time
Number of tool calls
Tool failures
Agent iterations
Final response latency
```

### Tool metrics

```text
API latency
API status
Timeouts
Retries
Rate limits
```

This makes debugging agentic workflows substantially easier than relying only on application logs.

---

# 🧪 Testing Strategy

A mature test suite should contain multiple layers.

## Unit Tests

Test individual tools:

```text
Search tool
Places tool
Expense calculator
Prompt construction
Configuration
```

---

## Integration Tests

Test:

```text
FastAPI
    ↓
GraphBuilder
    ↓
LangGraph
    ↓
Mocked tools
    ↓
Final response
```

External APIs should generally be mocked in CI.

---

## API Tests

Example:

```python
def test_query_endpoint():
    response = client.post(
        "/query",
        json={"question": "Plan a trip to Goa"}
    )

    assert response.status_code == 200
```

---

## End-to-End Test

The final workflow should validate:

```text
Streamlit
   ↓
FastAPI
   ↓
LangGraph
   ↓
Tools
   ↓
LLM
   ↓
Response
```

---

# 🧠 Engineering Design Principles

This project demonstrates several useful agentic-AI engineering patterns.

## 1. Separation of Concerns

```text
Frontend
   ↓
API
   ↓
Agent
   ↓
Tools
   ↓
External Services
```

Each layer has a defined responsibility.

---

## 2. Tool-Augmented Generation

The LLM does not need to know every piece of travel information.

Instead:

```text
LLM
 ↓
Tool selection
 ↓
Real-world data
 ↓
LLM synthesis
```

This reduces reliance on static model knowledge for information that changes frequently.

---

## 3. API Boundary

The Streamlit application does not directly own the agent implementation.

Instead:

```text
Streamlit
    ↓ HTTP
FastAPI
    ↓
Agent
```

This makes it possible to replace the frontend later without rewriting the agent backend.

---

## 4. Provider Abstraction

The backend constructs:

```python
GraphBuilder(model_provider="groq")
```

This creates a natural abstraction point for supporting additional LLM providers in the future.

---

# 🗺️ Roadmap

## Phase 1 — Reliability

* [ ] Add automated tests
* [ ] Add `/health` endpoint
* [ ] Add request timeout handling
* [ ] Add API retry policies
* [ ] Improve exception hierarchy
* [ ] Add structured logging

## Phase 2 — Agent Reliability

* [ ] Add graph execution limits
* [ ] Add tool timeouts
* [ ] Add retry/fallback policies
* [ ] Add structured agent state
* [ ] Add tool result validation
* [ ] Add LLM response validation

## Phase 3 — Production Architecture

* [ ] Restrict CORS
* [ ] Add authentication
* [ ] Add rate limiting
* [ ] Add Redis/cache layer
* [ ] Add persistent conversation state
* [ ] Add centralized observability
* [ ] Add CI/CD

## Phase 4 — AI Evaluation

* [ ] Create travel-planning evaluation dataset
* [ ] Evaluate factuality
* [ ] Evaluate tool selection
* [ ] Evaluate itinerary completeness
* [ ] Evaluate budget accuracy
* [ ] Evaluate hallucination rate
* [ ] Track regression across model versions

---

# 📊 Example Queries

Try requests such as:

```text
Plan a 5-day trip to Goa for two people.
```

```text
Plan a 7-day trip to Japan with a moderate budget.
```

```text
Plan a weekend trip to Mumbai including restaurants and attractions.
```

```text
Plan a family trip to Kerala with places to visit and estimated expenses.
```

```text
Plan a 4-day trip to Rajasthan and include major historical attractions.
```

The application accepts natural-language travel requests through the Streamlit interface.

---

# ⚠️ Known Limitations

The current implementation has several limitations that should be understood before treating it as a production travel platform.

### External Data

Travel information can change:

* Prices
* Hotel availability
* Restaurant hours
* Attraction timings
* Transportation schedules
* Weather
* Local regulations

The generated itinerary should therefore be independently verified.

### LLM Reliability

LLMs can produce:

* Incorrect information
* Missing information
* Unsupported assumptions
* Hallucinated recommendations

Tool-backed information should be preferred wherever available.

### API Dependencies

The application depends on external services including Groq, search, and places APIs.

Service outages, rate limits, invalid credentials, or network failures can affect the result.

### Backend Graph Construction

The current backend constructs the graph inside the `/query` request handler. For production, graph construction and model initialization should generally be moved into application startup/lifecycle management and reused where safe.

---

# 🚀 Production Architecture — Target State

A more production-oriented architecture could evolve toward:

```text
                         ┌───────────────┐
                         │    Client     │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ API Gateway   │
                         └───────┬───────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
                Auth/RBAC    Rate Limit    Request ID
                    │
                    ▼
              ┌───────────────┐
              │ FastAPI       │
              │ Service       │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ LangGraph     │
              │ Orchestrator  │
              └───────┬───────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
       Search       Places      Weather
        Tool         Tool         Tool
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
                 LLM Provider
                      │
                      ▼
                Response Guard
                      │
                      ▼
                 Final Plan
```

---

# 📜 License

No explicit open-source license is currently defined in the repository.

If you intend others to reuse or contribute to the project, add an appropriate license before treating the repository as an open-source project.

---

# 👩‍💻 Author

**Madhuri Teli**

GitHub:

https://github.com/MadhuriTeli

Project:

https://github.com/MadhuriTeli/AI_Trip_planner

---

# ⭐ Project Summary

**AI Trip Planner** demonstrates an end-to-end agentic AI application built with a modern Python stack.

The project combines:

```text
Python
   +
FastAPI
   +
Streamlit
   +
LangChain
   +
LangGraph
   +
Groq
   +
External Tools/APIs
```

The core engineering pattern is:

```text
Natural Language Request
          ↓
       FastAPI
          ↓
     LangGraph Agent
          ↓
     Tool Selection
          ↓
 External Information
          ↓
    LLM Reasoning
          ↓
  Structured Travel Plan
          ↓
      Streamlit UI
```

The project is intended to demonstrate practical engineering around **agent orchestration, tool calling, API integration, LLM applications, backend/frontend separation, environment management, and AI-assisted decision workflows**.

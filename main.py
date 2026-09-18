import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent.agentic_workflow import GraphBuilder

load_dotenv()

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Request / Response Models
# -----------------------------------------------------------------------------


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Travel planning question",
    )


class QueryResponse(BaseModel):
    answer: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


# -----------------------------------------------------------------------------
# Global graph instance
# -----------------------------------------------------------------------------

react_app = None


# -----------------------------------------------------------------------------
# Application lifespan
# -----------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    global react_app

    logger.info("Initializing AI Trip Planner agent...")

    try:
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()

        logger.info("AI Trip Planner agent initialized successfully")

    except Exception:
        logger.exception("Failed to initialize AI Trip Planner agent")
        raise

    yield

    logger.info("Shutting down AI Trip Planner agent")
    react_app = None


# -----------------------------------------------------------------------------
# FastAPI application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="AI Trip Planner API",
    description="AI-powered travel planning API using LangGraph and Groq",
    version="1.0.0",
    lifespan=lifespan,
)


# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:8501",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Health Check
# -----------------------------------------------------------------------------


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        service="ai-trip-planner",
        version="1.0.0",
    )


# -----------------------------------------------------------------------------
# Travel Agent
# -----------------------------------------------------------------------------


@app.post("/query", response_model=QueryResponse)
async def query_travel_agent(query: QueryRequest):

    if react_app is None:
        logger.error("Travel agent is not initialized")

        raise HTTPException(
            status_code=503,
            detail="Travel agent is not ready",
        )

    try:
        logger.info("Processing travel query")

        messages = {"messages": [query.question]}

        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return QueryResponse(answer=final_output)

    except Exception:
        logger.exception("Travel agent execution failed")

        raise HTTPException(
            status_code=500,
            detail="Trip planning request failed",
        )

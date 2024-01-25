from fastapi import FastAPI
from app.api.api_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(openapi_url="/openapi.json",  # Provide the path where the OpenAPI JSON is served
                docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/AI")

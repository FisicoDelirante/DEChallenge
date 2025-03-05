from fastapi import Depends, FastAPI
from api.ingestion import router as ingestion_router
from api.digestion import router as digestion_router
from api.querying import router as query_router
from security.authentication import authenticate_user

app = FastAPI(dependencies=[Depends(authenticate_user)])
app.include_router(ingestion_router)
app.include_router(digestion_router)
app.include_router(query_router)

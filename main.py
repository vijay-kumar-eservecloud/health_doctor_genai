# main.py

from fastapi import FastAPI, Request
from apps.routers import router
from database.models import Base
from database.connection import engine
from fastapi.middleware.cors import CORSMiddleware
from loggers.logger import setup_logger
from apps.exceptions import AppError  
from fastapi.responses import JSONResponse

app = FastAPI(title=" Health system API", 
              version="1.0.0", 
              description="API for managing users and health system.",
              contact={
                  "name": "Support Team",})

logger = setup_logger("api")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables once on startup
Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the health API!"}



@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    logger.error(f"AppError: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
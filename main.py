import logging
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from api.petrol_station_api import router as petrol_station_router
from api.petrol_price_api import router as petrol_price_router
from requsts.petrol_spy_request import read_local_spy_petrol_file
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn

app = FastAPI()

# CORS configuration
origins = [
    "*",
]

# Initialize scheduler
scheduler = AsyncIOScheduler()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(petrol_station_router, prefix="/api/v1", tags=["Petrol Stations"])
app.include_router(petrol_price_router, prefix="/api/v1", tags=["Petrol Price"])

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.on_event("startup")
async def startup_event():
    # Set SQLAlchemy log level
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    logging.info("Starting the scheduler")
    # Configure scheduled task with immediate execution
    scheduler.add_job(
        read_local_spy_petrol_file, 
        trigger=IntervalTrigger(hours=1),
        next_run_time=datetime.now()  # Execute immediately on startup
    )

    # Start the scheduler
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown the scheduler when the app stops
    scheduler.shutdown()

if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True    # Enable hot reload for development
    )

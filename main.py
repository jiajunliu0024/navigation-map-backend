import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import engine, Base
from api.petrol_station_api import router as petrol_station_router
from api.petrol_price_api import router as petrol_price_router
from requsts.petrol_spy_request import read_local_spy_petrol_file
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = FastAPI()

origins = [
    "*",
]
# Scheduler setup
scheduler = AsyncIOScheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(petrol_station_router, prefix="/api/v1", tags=["Petrol Stations"])
app.include_router(petrol_price_router, prefix="/api/v1", tags=["Petrol Price"])

# Scheduler setup
scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    Base.metadata.create_all(bind=engine)

    # Schedule the task to run every hour
    scheduler.add_job(read_local_spy_petrol_file, IntervalTrigger(hours=1))

    # Start the scheduler
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown the scheduler when the app stops
    scheduler.shutdown()

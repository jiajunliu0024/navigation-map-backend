from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import engine, Base
from api.petrol_station_api import router as petrol_station_router
from api.petrol_price_api import router as petrol_price_router
from requsts.petrol_spy_request import read_local_spy_petrol_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your frontend's URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(petrol_station_router, prefix="/api/v1", tags=["Petrol Stations"])
app.include_router(petrol_price_router, prefix="/api/v1", tags=["Petrol Price"])

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    # read_local_spy_petrol_file()

from fastapi import HTTPException

class PetrolStationNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Petrol station not found")

class InvalidCoordinatesException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid coordinates provided") 
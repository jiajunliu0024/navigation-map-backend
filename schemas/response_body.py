from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ResponseBody(BaseModel, Generic[T]):
    body: Optional[T] = None
    message: str
    size: int = 0
    code: int
    errors: Optional[list[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "body": None,
                "message": "success",
                "size": 0,
                "code": 200,
                "errors": None
            }
        }
"""Common schemas used across the application"""
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination parameters"""
    skip: int = 0
    limit: int = 100


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""
    items: List[T]
    total: int
    skip: int
    limit: int


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    app_name: str
    version: str
    database: str
    ml_model: str


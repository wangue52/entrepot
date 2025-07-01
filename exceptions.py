# exceptions.py
from fastapi import HTTPException, status

class ProductNotFound(HTTPException):
    def __init__(self, product_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id '{product_id}' not found"
        )

class SalePointNotFound(HTTPException):
    def __init__(self, sale_point_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sale point with id '{sale_point_id}' not found"
        )

class PriceNotFound(HTTPException):
    def __init__(self, product_id: str, sale_point_id: str, date_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Price not found for product '{product_id}', sale point '{sale_point_id}', and date '{date_id}'"
        )

class DateNotFound(HTTPException):
    def __init__(self, date_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Date with id '{date_id}' not found"
        )

class DuplicateEntry(HTTPException):
    def __init__(self, entity: str, identifier: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{entity} with identifier '{identifier}' already exists"
        )

class DatabaseError(HTTPException):
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )

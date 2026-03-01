# src/api/v1/endpoints/databases.py
from fastapi import APIRouter, Depends

from src.api.dependencies import get_database_service
from src.services.database_service import DatabaseService

router = APIRouter(prefix="/databases", tags=["Databases"])


@router.post("/recreate", status_code=200)
async def recreate_databases(
    db_service: DatabaseService = Depends(get_database_service),
):
    await db_service.recreate_databases()
    return {"message": "Databases have been recreated successfully."}

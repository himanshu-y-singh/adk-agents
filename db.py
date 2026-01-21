from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repository.postgres_db.crud import add_user, get_transactions, add_transaction, get_users
from repository.postgres_db.session import get_db, list_tables, delete_table, create_tables
from config import get_logger
from typing import Annotated
from repository.schemas.users import User
from repository.schemas.transactions import Transaction
from datetime import datetime

logger = get_logger(__name__)

router = APIRouter()

@router.post("/add/user")
async def add_user_endpoint(request: User, db: Annotated[AsyncSession, Depends(get_db)]):
    return await add_user(db, request)

@router.post("/transactions")
async def get_transactions_endpoint(request: User, db: Annotated[AsyncSession, Depends(get_db)]):
    user_id = request.name
    return await get_transactions(db, user_id)

@router.post("/add/transaction")
async def add_transaction_endpoint(request: Transaction, db: Annotated[AsyncSession, Depends(get_db)]):
    return await add_transaction(db, request)

@router.get("/users")
async def get_users_endpoint(db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        return await get_users(db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/create_tables")
async def create_tables_endpoint():
    try:
        await create_tables()
        tables = await list_tables()
        return {"status": "success", "message": "Tables created successfully", "tables": tables}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/tables")
async def get_tables():
    return await list_tables()

@router.delete("/{table_name}")
async def delete_table_endpoint(table_name: str):   
    try:
        await delete_table(table_name)
        return {"status": "success", "message": f"Table '{table_name}' deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, inspect
from repository.config import db_config
from repository.postgres_db.base import Base

engine = create_async_engine(
    db_config.url,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def list_tables():
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        return tables

async def delete_table(table_name: str):
    async with engine.begin() as conn:
        await conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
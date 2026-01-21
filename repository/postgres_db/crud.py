from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from repository.postgres_db.models import User, Transaction

async def add_user(
    db: AsyncSession,
    user: any
):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def add_transaction(
    db: AsyncSession,
    transaction: any
):
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_transactions(
    db: AsyncSession,
    name: str,
):
    stmt = (
        select(Transaction)
        .where(
            Transaction.from_user == name,
        )
        .order_by(Transaction.created_at)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_users(
    db: AsyncSession,
):
    stmt = (
        select(User)
        .order_by(User.created_at)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


import asyncio
from repository.postgres_db.session import create_tables
# Import models to register them with Base
from repository.postgres_db.models import WorkLog, JobApplication, User, Transaction

async def main():
    print("Creating tables...")
    await create_tables()
    print("Tables created.")

if __name__ == "__main__":
    asyncio.run(main())

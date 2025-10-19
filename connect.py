from sqlalchemy.ext.asyncio import  create_async_engine,async_sessionmaker
from sqlalchemy.orm import declarative_base




SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:13801211@localhost:5432/task_shipping"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = async_sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()



async def create_db_and_tables():
    # این دستور تمام مدل‌های ارث‌برده از Base را به جداول در دیتابیس تبدیل می‌کند.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
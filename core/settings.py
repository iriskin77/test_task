from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import POSTGRES_HOST, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER


#DATABASE_URL_POSTGRES = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DATABASE_URL_SQLITE = f"sqlite+aiosqlite:///task_db.sqlite3"

engine = create_async_engine(DATABASE_URL_SQLITE, echo=False, future=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine, class_=AsyncSession)



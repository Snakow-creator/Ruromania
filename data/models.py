from sqlalchemy import create_engine, BigInteger, String
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

async_engine = create_async_engine(url="sqlite+aiosqlite:///users.sqlite3", echo=True)
async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


class Usersbase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str] = mapped_column(String(60))
    money_value: Mapped[int | None]


async def async_main():
    async with async_engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

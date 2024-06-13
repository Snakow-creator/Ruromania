from data.models import async_session
from data.models import Usersbase
from sqlalchemy import select


async def download_users(tg_id: int, name: str, fullname: str):
    async with async_session() as session:
        user_tg_id = await session.scalar(
            select(Usersbase).where(Usersbase.tg_id == tg_id)
        )
        if not user_tg_id:
            session.add(
                Usersbase(tg_id=tg_id, name=name, fullname=fullname, money_value=10000)
            )
            await session.commit()


async def daily_change_users(tg_id: int, name: str, fullname: str):
    async with async_session() as session:
        stmt = await session.scalar(select(Usersbase).where(Usersbase.tg_id == tg_id))
        stmt.name = name
        stmt.fullname = fullname
        user_money = stmt.money_value
        stmt.money_value = user_money + 10000
        await session.commit()


async def money_load(tg_money: int, tg_id: int):
    async with async_session() as session:
        user_id = await get_id(tg_id)
        stmt = await session.get(Usersbase, user_id)
        stmt.money_value = tg_money
        await session.commit()


async def get_id(tg_id):
    async with async_session() as session:
        user_find = await session.scalar(
            select(Usersbase).where(Usersbase.tg_id == tg_id)
        )
        stmt = user_find.id
        return stmt


async def check_balance(tg_id):
    async with async_session() as session:
        user_find = await session.scalar(
            select(Usersbase).where(Usersbase.tg_id == tg_id)
        )
        stmt = user_find.money_value
        return stmt


async def change_balance(text_money, tg_id):
    async with async_session() as session:
        stmt = await session.scalar(select(Usersbase).where(Usersbase.tg_id == tg_id))
        user_money = stmt.money_value
        stmt.money_value = user_money + text_money
        await session.commit()


async def deprive_balance(text_money, tg_id):
    async with async_session() as session:
        stmt = await session.scalar(select(Usersbase).where(Usersbase.tg_id == tg_id))
        user_money = stmt.money_value
        stmt.money_value = user_money - text_money
        await session.commit()


async def top_users():
    async with async_session() as session:
        return await session.scalars(select(Usersbase))

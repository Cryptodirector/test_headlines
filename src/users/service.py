from aiogram import Router, types
from sqlalchemy import insert, select, and_, update

from src.database.config import async_session_maker
from src.news.models import Site
from src.users.models import Users
from sqlalchemy.exc import IntegrityError

router = Router()


async def registration_user(
        message: types.Message
):
    id_tg = int(message.from_user.id)
    name_tg = message.from_user.username

    async with async_session_maker() as session:
        stmt = insert(Users).values(
            name=name_tg,
            id_tg=id_tg,
            subscription=1
        )
        try:
            await session.execute(stmt)
            await session.commit()
            return True

        except IntegrityError as ex:
            return False


# Получаем свой кабинет

async def get_my_office(callback: types.CallbackQuery):
    my_id = str(callback.from_user.id)
    async with async_session_maker() as session:
        query = select(
            Users.id_tg,
            Users.name,
            Site.url,
            Users.pagination
        ).join(Site).where(
            and_(
                Users.id_tg == my_id,
                Users.subscription == Site.id
            )
        )
        result = await session.execute(query)
        return result.all()


async def update_pagination(
        message: types.Message,
        page: int
):
    my_id = str(message.from_user.id)
    async with async_session_maker() as session:
        if page < 10 or page > 1:
            stmt = update(Users).values(pagination=page).where(
                Users.id_tg == my_id
            )
            await session.execute(stmt)
            await session.commit()
        else:
            print('Недопустимое число!')

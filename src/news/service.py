from sqlalchemy import select, update

from src.database.config import async_session_maker
from src.news.models import Site, News
from src.users.models import Users
from aiogram import types


# Получаем названия сайтов из базы

async def get_all_site():
    async with async_session_maker() as session:
        query = select(Site)
        result = await session.execute(query)
        return result.scalars().all()


# Получаем все новости из выбранного сайта

async def get_my_news(my_id: str):
    list_result = ""
    async with async_session_maker() as session:
        subquery = select(Users.subscription).where(Users.id_tg == str(my_id))  # получаем id своей подписки
        subscription = await session.execute(subquery)
        sub = subscription.scalar()

        lim = select(Users.pagination).where(Users.id_tg == str(my_id))  # получаем свою настройку пагинации
        limit = await session.execute(lim)

        query = select(News).limit(limit.scalar()).where(News.id_site == int(sub))  # Получаем все новости с учетом
        result = await session.execute(query)                                       # с учетом ограничений
        for results in result.scalars().all():
            if sub == 1:
                list_result += (f'<i>{results.title}</i>\n<a href="{results.link_to_news}">'
                                f'ru.investing.com</a>\n\n')
            elif sub == 2:
                list_result += (f'<i>{results.title}</i>\n<a href="{results.link_to_news}">'
                                f'cryptonews.net</a>\n\n')
            elif sub == 3:
                list_result += (f'<i>{results.title}</i>\n<a href="{results.link_to_news}">'
                                f'investfunds.ru</a>\n\n')

    return list_result


# обновляем свою подписку на новости

async def update_subscription(
        my_id: str,
        callback: types.CallbackQuery
):
    async with async_session_maker() as session:
        query = select(Site.id).where(Site.url == callback.data)  # Получаем id своей подписки
        result = await session.execute(query)

        stmt = update(Users).where(Users.id_tg == my_id).values(
            subscription=result.scalar()  # Обновляем свою подписку
        )
        await session.execute(stmt)
        await session.commit()

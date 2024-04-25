import asyncio

import aiohttp
from bs4 import BeautifulSoup as bs
from sqlalchemy import insert

from src.database.config import async_session_maker
from src.news.models import News
from sqlalchemy.exc import IntegrityError


# Получаем информацию с сайта ru.investing.com

class Investing:
    def __init__(self):
        self.investing = 'https://ru.investing.com/news/latest-news'
        self.lst_news = {}

    async def get_news(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.investing) as response:
                soup = bs(await response.text(), 'html.parser')
                cards = soup.find_all('li', {
                    'class': 'list_list__item__dwS6E !mt-0 border-t border-solid border-[#E6E9EB] py-6'
                })
                for card in cards:
                    title = card.find('div', {
                        'class': 'news-analysis-v2_content__z0iLP w-full text-xs sm:flex-1'
                    }).find('a', {
                        'class': 'text-secondary hover:text-secondary hover:underline'
                                 ' focus:text-secondary focus:underline whitespace-normal'
                                 ' text-sm font-bold leading-5 !text-[#181C21] sm:text-base'
                                 ' sm:leading-6 lg:text-lg lg:leading-7'
                    })

                    url = 'https://ru.investing.com' + title['href']
                    self.lst_news.update({url: title.text})
                return self.lst_news

    # добаляем в базу

    async def add_to_database(self):
        async with async_session_maker() as session:
            try:
                news = await self.get_news()
                for url, title in news.items():
                    stmt = insert(News).values(
                        link_to_news=url,
                        title=title,
                        id_site=1
                    )
                    await session.execute(stmt)
                    await session.commit()

            except IntegrityError:
                print('Новость уже есть!')


# Получаем информацию с сайта https://cryptonews.net/ru/

class CryptoNews:
    def __init__(self):
        self.rbk = 'https://cryptonews.net/ru/'
        self.lst_news = {}

    async def get_news(self):
        async with aiohttp.ClientSession() as session:

            async with session.get(self.rbk) as response:
                soup = bs(await response.text(), 'html.parser')
                cards = soup.find_all('div', {'class': 'row news-item start-xs'})
                for card in cards:

                    title = card.find('div', {'class': 'desc col-xs'}).find('a')
                    new_title = ' '.join(title.text.split())  # Убираем лишние пробелы

                    url = 'https://cryptonews.net/ru' + title['href']
                    self.lst_news.update({url: new_title})

        return self.lst_news

    async def add_to_database(self):
        async with async_session_maker() as session:
            try:
                news = await self.get_news()
                for url, title in news.items():
                    stmt = insert(News).values(
                        link_to_news=url,
                        title=title,
                        id_site=2
                    )
                    await session.execute(stmt)
                    await session.commit()

            except IntegrityError:
                print('Новость уже есть!')


# Получаем информацию с сайта https://investfunds.ru

class InvestFunds:
    def __init__(self):
        self.invest_funds = 'https://investfunds.ru/news/'
        self.lst_news = {}

    async def get_news(self):
        async with aiohttp.ClientSession() as session:

            async with session.get(self.invest_funds) as response:
                soup = bs(await response.text(), 'html.parser')
                cards = soup.find('ul', {'class': 'news_list'}).find_all('li', {'class': 'item'})

                for card in cards:
                    title = card.find('a', {'class': 'indent_right_10 left'})
                    new_title = ' '.join(title.text.split())
                    url = 'https://investfunds.ru' + title['href']
                    self.lst_news.update({url: new_title})

        return self.lst_news

    async def add_to_database(self):
        async with async_session_maker() as session:
            try:
                news = await self.get_news()
                for url, title in news.items():
                    stmt = insert(News).values(
                        link_to_news=url,
                        title=title,
                        id_site=3
                    )
                    await session.execute(stmt)
                    await session.commit()

            except IntegrityError:
                print('Новость уже есть!')


parser = InvestFunds()
asyncio.run(parser.add_to_database())

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.news.service import get_all_site


class NewsKeyboards:
    builder = None

    @classmethod
    async def view_menu(
            cls,
            message: types.Message

    ):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(
                text='🏠 Мой кабинет',
                callback_data='my_office'
            ),
            types.InlineKeyboardButton(
                text='✅ Подписаться на новости',
                callback_data='news'
            ),
            types.InlineKeyboardButton(
                text='🫴 Получить новости',
                callback_data='get_news'
            ),
            types.InlineKeyboardButton(
                text='⚜ Инструкция',
                callback_data='instructions'
            ),

        ]
        builder.add(*buttons)
        builder.adjust(1)
        await message.answer(
            'Выберите интересующую \n'
            ' вас категорию!',
            reply_markup=builder.as_markup()
        )
        return builder

    @classmethod
    async def view_list_site(
            cls,
            callback: types.CallbackQuery,

    ):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(
                text='⬅ Назад',
                callback_data='back'
            ),
        ]
        for site in await get_all_site():
            buttons_site = [
                types.InlineKeyboardButton(
                    text=f'⚡ {site.url}',
                    callback_data=f'{site.url}'
                ),
            ]
            builder.add(*buttons_site)
        builder.add(*buttons)
        builder.adjust(1)
        await callback.message.edit_text(
            'Выберите подписку!', reply_markup=builder.as_markup()
        )
        return builder

    @classmethod
    async def view_instruction(
            cls,
            callback: types.CallbackQuery

    ):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(
                text='⬅ Назад',
                callback_data='back2'
            ),

        ]
        builder.add(*buttons)
        builder.adjust(1)
        await callback.message.edit_text(
            '<i>Инструкция:\n'
            '1.Кнопка мой кабинет - в кабинете можно посмотреть свой ник, id,\n'
            'на что подписан(по умолчанию сайт ru.investing.com),\n'
            'количество получаемых новостей за раз\n'
            '(по умолчанию 5), там же можно поменять '
            'колчичество получаемых новостей(кнопка: "изменить пагинацию")\n'
            '2. Кнопка подписаться на новости - в выпадющем меню есть 3 варианта\n'
            'ru.investing.com, cryptonews.net, investfunds.ru,\n'
            'при нажатии на кнопку вы выбираете откуда хотите получать новости\n'
            '3. Кнопка получить новости - при нажатии на кнопку вы получаете\n'
            'все новости</i>',
            reply_markup=builder.as_markup(), parse_mode='html'

        )
        return builder

    @classmethod
    async def view_news(
            cls,
    ):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(
                text='⬅ Назад',
                callback_data='back4'
            ),

        ]
        builder.add(*buttons)
        builder.adjust(1)

        return builder.as_markup()









from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


class BackButtons:

    @staticmethod
    async def view_menu(
            callback: types.CallbackQuery

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
        await callback.message.edit_text(
            'Выберите интересующую \n'
            ' вас категорию!',
            reply_markup=builder.as_markup()
        )
        return builder
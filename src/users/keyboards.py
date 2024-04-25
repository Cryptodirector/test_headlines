from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.users.service import get_my_office


class UserKeyboards:
    builder = None

    @classmethod
    async def view_my_office(
            cls,
            callback: types.CallbackQuery,

    ):
        builder = InlineKeyboardBuilder()
        buttons = [
            types.InlineKeyboardButton(text='Изменить пагинацию', callback_data='pagination'),
            types.InlineKeyboardButton(text='⬅  Назад', callback_data='back3'),


        ]
        builder.add(*buttons)
        builder.adjust(2)
        for user_info in await get_my_office(callback):
            await callback.message.edit_text(f'Мой ник: {user_info[0]}\n'
                                             f'Мой ID: {user_info[1]}\n'
                                             f'Ваша подписка: {user_info[2]}\n'
                                             f'Пагинация: {user_info[3]}',
                                             reply_markup=builder.as_markup())
        return builder

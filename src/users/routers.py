import asyncio
import os

from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.news.service import update_subscription
from src.news.utils import site
from src.users.service import update_pagination
from src.news.keyboards import NewsKeyboards

router = Router()
API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)


# состояние юзера
class UserMSG(StatesGroup):
    user_info = State()


# Принимаем от юзера сообщение

@router.callback_query(F.data == 'pagination')
async def my_office(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(UserMSG.user_info)
    await callback.answer(
        'Введите желаемое количество новостей за раз!', show_alert=True
    )

# обрабатываем сообщение от юзера


@router.message(UserMSG.user_info)
async def fun(message: types.Message):
    await message.delete()

    # Валидация

    if int(message.text) < 1 or int(message.text) > 10:
        delete_msg = await message.answer('Число должно быть не меньше 1\n'
                             'или не больше 10')

        await NewsKeyboards.view_menu(message)
        await asyncio.sleep(4)
        await bot.delete_message(chat_id=message.from_user.id, message_id=delete_msg.message_id)

    else:
        await update_pagination(  # Обновляем пагинацию
            message,
            page=int(message.text)
        )
        await NewsKeyboards.view_menu(message)


# Обновляем свою подписку

@router.callback_query(lambda call: [x for x in site])
async def update_my_subscription(callback: types.CallbackQuery):
    my_id = callback.from_user.id
    await update_subscription(str(my_id), callback)
    await callback.answer(
        f'Вы подписались на : {callback.data}',
        show_alert=True
    )

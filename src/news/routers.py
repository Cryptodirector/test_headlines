from aiogram import Router, types, F
from src.news.keyboards import NewsKeyboards
from src.news.buttons_back import BackButtons
from src.news.service import get_my_news
from src.users.keyboards import UserKeyboards


router = Router()


class MenuRouters:

    # роутер для выбора подписки

    @staticmethod
    @router.callback_query(F.data == 'news')
    async def get_list_site(callback: types.CallbackQuery):
        return await NewsKeyboards.view_list_site(callback)

    # Роутер для поулуения инструкции

    @staticmethod
    @router.callback_query(F.data == 'instructions')
    async def get_instructions(callback: types.CallbackQuery):
        return await NewsKeyboards.view_instruction(callback)

    # Роутер для перехода в личный кабинет

    @staticmethod
    @router.callback_query(F.data == 'my_office')
    async def get_instructions(callback: types.CallbackQuery):
        return await UserKeyboards.view_my_office(callback)

    # Роутер для получения новостей

    @staticmethod
    @router.callback_query(F.data == 'get_news')
    async def get_news(callback: types.CallbackQuery):
        my_id = callback.from_user.id
        result = await get_my_news(str(my_id))

        await callback.message.edit_text(
            text=f'{result}',
            parse_mode='html',
            reply_markup=await NewsKeyboards.view_news()
        )


# Класс для кнопок назад во всем приложении

class BackButtonsRouter:

    @staticmethod
    @router.callback_query(F.data == 'back')
    async def back_buttons(callback: types.CallbackQuery):
        return await BackButtons.view_menu(callback)

    @staticmethod
    @router.callback_query(F.data == 'back2')
    async def back_buttons(callback: types.CallbackQuery):
        return await BackButtons.view_menu(callback)

    @staticmethod
    @router.callback_query(F.data == 'back3')
    async def back_buttons(callback: types.CallbackQuery):
        return await BackButtons.view_menu(callback)

    @staticmethod
    @router.callback_query(F.data == 'back4')
    async def back_buttons(callback: types.CallbackQuery):
        return await BackButtons.view_menu(callback)

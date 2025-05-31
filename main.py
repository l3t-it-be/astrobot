import asyncio
import html
import logging
import random

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from config import Config, load_config
from kind_of_oracle.oracle_handler import get_zodiac_signs
from kind_of_oracle.useful_for_everybody import predictions

logger = logging.getLogger(__name__)


main_menu_buttons = [
    [
        InlineKeyboardButton(
            text='Получить прогноз',
            callback_data='oracle',
        )
    ],
    [
        InlineKeyboardButton(text='О разработчике', callback_data='about_me'),
        InlineKeyboardButton(text='О разработке', callback_data='libraries'),
    ],
]
main_menu = InlineKeyboardMarkup(inline_keyboard=main_menu_buttons)


def get_welcome_text(user_name: str, bot_name: str) -> str:
    return (
        f'✨ Добро пожаловать, <b>{html.escape(user_name)}</b>! ✨\n\n'
        f'Я - <b>{html.escape(bot_name)}</b>, ваш персональный астрологический гид! '
        f'Выберите действие ниже ⬇️'
    )


async def start_message(message: Message, bot: Bot):
    bot_info = await bot.get_me()
    await message.answer(
        get_welcome_text(message.from_user.full_name, bot_info.full_name),
        reply_markup=main_menu,
    )


async def back_to_menu(call: CallbackQuery, bot: Bot) -> None:
    bot_info = await bot.get_me()
    await call.message.answer(
        get_welcome_text(call.from_user.full_name, bot_info.full_name),
        reply_markup=main_menu,
    )
    await call.answer()


async def get_prediction(call: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(
                text='Ещё один прогноз', callback_data='zodiac'
            ),
            InlineKeyboardButton(
                text='🔙 Вернуться в Меню', callback_data='menu'
            ),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text(
        random.choice(predictions), reply_markup=keyboard
    )


async def get_about_me_info(call: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(
                text='📩 Написать в Telegram', url='https://t.me/l3t_it_be'
            )
        ],
        [
            InlineKeyboardButton(
                text='🔙 Вернуться в Меню', callback_data='menu'
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text(
        '''👋 <b>Привет!</b>

Меня зовут <b>Екатерина</b> ✨

🔧 Занимаюсь разработкой и автоматизацией на Python
💡 Создаю эффективные решения для ваших задач''',
        reply_markup=keyboard,
    )


async def get_libraries_info(call: CallbackQuery, bot: Bot):
    bot_info = await bot.get_me()
    button = [
        [
            InlineKeyboardButton(
                text='🔙 Вернуться в Меню', callback_data='menu'
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    await call.message.edit_text(
        f'<b>{html.escape(bot_info.full_name)}</b> написан на Python 3 🐍 и aiogram 3⚡',
        reply_markup=keyboard,
    )


def register_handlers(dp: Dispatcher):
    dp.message.register(start_message, CommandStart())
    dp.callback_query.register(get_zodiac_signs, F.data == 'oracle')
    dp.callback_query.register(back_to_menu, F.data == 'menu')
    dp.callback_query.register(get_prediction, F.data == 'zodiac')
    dp.callback_query.register(get_about_me_info, F.data == 'about_me')
    dp.callback_query.register(get_libraries_info, F.data == 'libraries')


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    logger.error('Starting bot')

    config: Config = load_config()
    BOT_TOKEN: str = config.tg_bot.token

    astro_bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    register_handlers(dp)
    await dp.start_polling(astro_bot)


if __name__ == '__main__':
    asyncio.run(main())

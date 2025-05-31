from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

zodiac_buttons = [
    [
        InlineKeyboardButton(text='Овен ♈', callback_data='zodiac'),
        InlineKeyboardButton(text='Телец ♉', callback_data='zodiac'),
        InlineKeyboardButton(text='Близнецы ♊', callback_data='zodiac'),
    ],
    [
        InlineKeyboardButton(text='Рак ♋', callback_data='zodiac'),
        InlineKeyboardButton(text='Лев ♌', callback_data='zodiac'),
        InlineKeyboardButton(text='Дева ♍', callback_data='zodiac'),
    ],
    [
        InlineKeyboardButton(text='Весы ♎', callback_data='zodiac'),
        InlineKeyboardButton(text='Скорпион ♏', callback_data='zodiac'),
        InlineKeyboardButton(
            text='Стрелец ♐',
            callback_data='zodiac',
        ),
    ],
    [
        InlineKeyboardButton(text='Козерог ♑', callback_data='zodiac'),
        InlineKeyboardButton(text='Водолей ♒', callback_data='zodiac'),
        InlineKeyboardButton(text='Рыбы ♓', callback_data='zodiac'),
    ],
    [InlineKeyboardButton(text='🔙 Вернуться в Меню', callback_data='menu')],
]

zodiac_menu = InlineKeyboardMarkup(inline_keyboard=zodiac_buttons)


async def get_zodiac_signs(call: CallbackQuery):
    await call.message.answer(
        'Выберите знак зодиака или вернитесь в Меню:',
        reply_markup=zodiac_menu,
    )

    await call.answer()

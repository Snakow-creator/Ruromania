from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

# Главные кнопки
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Игры🎮"), KeyboardButton(text="Баланс💰")],
        [KeyboardButton(text="Вывод средств💸"), KeyboardButton(text="Информация♟")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите список ниже:",
)

# Игры
main_games = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Случайное число🎲"), KeyboardButton(text="Рулетка🏵")],
        [KeyboardButton(text="Блекджек♠️"), KeyboardButton(text="Слоты🎰")],
        [KeyboardButton(text="Топ пользователей🏆"), KeyboardButton(text="Назад⬅️")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите игру ниже:",
)


# Кнопки под сообщением, пополнение баланса
def keyboard_money():
    button = [
        [
            types.InlineKeyboardButton(text="Да", callback_data="get_yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="get_no"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard


# Информация, ответы на вопросы.
def info_keyboard():
    button = [
        [InlineKeyboardButton(text='Как играть в "Блекджек"?', callback_data="info_1")],
        [
            InlineKeyboardButton(
                text='Как работает диапазон в "Случайное число?"',
                callback_data="info_2",
            )
        ],
        [
            InlineKeyboardButton(
                text='Сколько дает иксов "Слоты"?', callback_data="info_3"
            )
        ],
        [
            InlineKeyboardButton(
                text='Правда ли казино "Руромания" выводит деньги?',
                callback_data="info_4",
            )
        ],
        [
            InlineKeyboardButton(
                text='Можно ли заработать кучу денег в "Руромания"?',
                callback_data="info_5",
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=button)
    return keyboard


back = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад⬅️", callback_data="back")]]
)


# Случайное число(dice)
rnumbutton = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Как водить числа🆘", callback_data="faq_num")]
    ]
)


rnumbutton_con = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Попробовать еще раз▶️", callback_data="confirm_rn")]
    ]
)


rnumbutton_end = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Очистить❌", callback_data="clear_rn"),
            InlineKeyboardButton(text="Подтвердить✅", callback_data="confirm_rn"),
        ]
    ]
)


# Рулетка
def r_keyboard():
    roulette = [
        [
            InlineKeyboardButton(text="100🟢", callback_data="numr_hundred"),
            InlineKeyboardButton(text="500🟡", callback_data="numr_fivehundred"),
            InlineKeyboardButton(text="1.000🔴", callback_data="numr_thousand"),
            InlineKeyboardButton(text="5.000🟣", callback_data="numr_fivethousand"),
        ],
        [
            InlineKeyboardButton(text="10.000🟠", callback_data="numr_tenthousand"),
            InlineKeyboardButton(text="50.000🔵", callback_data="numr_fiftythousand"),
            InlineKeyboardButton(
                text="100.000⚪️", callback_data="numr_hundredthousand"
            ),
            InlineKeyboardButton(
                text="500.000🟤", callback_data="numr_fivehundredthousand"
            ),
        ],
        [
            InlineKeyboardButton(text="Очистить ставку", callback_data="numr_clearbet"),
            InlineKeyboardButton(
                text="Подтвердить ставку", callback_data="numr_confirmbet"
            ),
        ],
    ]
    r_bet = types.InlineKeyboardMarkup(inline_keyboard=roulette)
    return r_bet


def rvalue_keyboard():
    kb_value = [
        [
            InlineKeyboardButton(text="Четные", callback_data="button_even"),
            InlineKeyboardButton(text="1-12", callback_data="button_112"),
            InlineKeyboardButton(text="13-24", callback_data="button_1324"),
            InlineKeyboardButton(text="25-36", callback_data="button_2536"),
            InlineKeyboardButton(text="Нечетные", callback_data="button_odd"),
        ],
        [
            InlineKeyboardButton(text="1-18", callback_data="button_118"),
            InlineKeyboardButton(text="Красный", callback_data="button_red"),
            InlineKeyboardButton(text="0", callback_data="button_0"),
            InlineKeyboardButton(text="Черный", callback_data="button_black"),
            InlineKeyboardButton(text="19-36", callback_data="button_1936"),
        ],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb_value)


def r_continue():
    kb_button = [
        [
            InlineKeyboardButton(
                text="Сбросить значения🔚.", callback_data="rgame_clear"
            ),
            InlineKeyboardButton(
                text="Поменять направление🔙.", callback_data="rgame_changevalue"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Попробовать еще раз🔄.", callback_data="rgame_continue"
            )
        ],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kb_button)


# Блекджек
def bj_keyboard():
    bj = [
        [
            InlineKeyboardButton(text="100🟢", callback_data="num_hundred"),
            InlineKeyboardButton(text="500🟡", callback_data="num_fivehundred"),
            InlineKeyboardButton(text="1.000🔴", callback_data="num_thousand"),
            InlineKeyboardButton(text="5.000🟣", callback_data="num_fivethousand"),
        ],
        [
            InlineKeyboardButton(text="10.000🟠", callback_data="num_tenthousand"),
            InlineKeyboardButton(text="50.000🔵", callback_data="num_fiftythousand"),
            InlineKeyboardButton(text="100.000⚪️", callback_data="num_hundredthousand"),
            InlineKeyboardButton(
                text="500.000🟤", callback_data="num_fivehundredthousand"
            ),
        ],
        [
            InlineKeyboardButton(text="Очистить ставку", callback_data="num_clearbet"),
            InlineKeyboardButton(
                text="Подтвердить ставку", callback_data="num_confirmbet"
            ),
        ],
    ]
    bj_bet = types.InlineKeyboardMarkup(inline_keyboard=bj)
    return bj_bet


bj_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Взять карту🃏", callback_data="hit"),
            InlineKeyboardButton(text="Оставить🌟", callback_data="stand"),
        ]
    ]
)

# Слоты
slot_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Попробовать еще раз▶️", callback_data="confirm_slot"
            )
        ]
    ]
)

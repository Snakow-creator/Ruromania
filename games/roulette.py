from aiogram.types import Message, CallbackQuery
from aiogram import types
import apps.keyboards as kb
import data.requests as rq
import random
import time

data_bet = {}
data_text = {}
data_cof = {}
data_value = {}


# Приветствие, принятие ставок.
async def message_roulette(message: Message):
    data_text[message.from_user.id] = "Ваши фишки:"
    data_bet[message.from_user.id] = 0
    await message.answer(
        "Ты выбрал игру Рулетка. Твоя ставка: 0" "\nТвои фишки:",
        reply_markup=kb.r_keyboard(),
    )


async def callback_roulette(callback: CallbackQuery):
    data_text[callback.from_user.id] = "Твои фишки:"
    data_bet[callback.from_user.id] = 0
    await callback.message.answer(
        "Ты выбрал игру Рулетка. Твоя ставка: 0" "\nТвои фишки:",
        reply_markup=kb.r_keyboard(),
    )


async def edit_bet(callback: types.CallbackQuery, bet: float):
    roulette_text = data_text.get(callback.from_user.id, "")
    await callback.message.edit_text(
        f"Ты выбрал игру Рулетка. Твоя ставка: {bet:,} " f"\n{roulette_text}",
        reply_markup=kb.r_keyboard(),
    )


async def value_text(callback: types.CallbackQuery, bet: float):
    await callback.message.edit_text(
        f"Хорошо твоя ставка: {bet:,}." f"\nВыбери направление куда попадет шарик:",
        reply_markup=kb.rvalue_keyboard(),
    )


# Крутка рулетки.
async def roullete_roullette(callback: CallbackQuery, c, range_text):
    data_cof[callback.from_user.id] = c
    data_value[callback.from_user.id] = range_text
    user_bet = data_bet.get(callback.from_user.id, 0)
    user_money = await rq.check_balance(callback.from_user.id)
    if user_money >= user_bet:
        await callback.message.edit_text("Крутим рулетку")
        time.sleep(0.3)
        await callback.message.edit_text("Крутим рулетку.")
        time.sleep(0.2)
        await callback.message.edit_text("Крутим рулетку..")
        time.sleep(0.2)
        await callback.message.edit_text("Крутим рулетку...")
        time.sleep(0.5)
        value = random.randint(0, 36)
        if value in range_text:
            bet_win = c * user_bet
            await roullete_end_win(callback=callback, bet=bet_win, value=value)
        else:
            await roullete_end_lose(callback=callback, bet=user_bet, value=value)
    else:
        await callback.message.edit_text(
            "Эй! Ты поставил ставку больше чем твой баланс."
            "\nЕсли ты проиграешь, я не хочу тратиться на коллекторов🥱."
        )


# Конец рулетки(Обработка проигрыша и выйгрыша)
async def roullete_end_win(callback: CallbackQuery, bet, value):
    await rq.change_balance(text_money=bet, tg_id=callback.from_user.id)
    await callback.message.edit_text(
        f"Поздравляю ты выйграл: <b>{bet:,}</b>!"
        f"\nВыпало число: {value}."
        f"\nХочешь сыграть ещё раз?",
        reply_markup=kb.r_continue(),
    )


async def roullete_end_lose(callback: CallbackQuery, bet, value):
    await rq.deprive_balance(text_money=bet, tg_id=callback.from_user.id)
    await callback.message.edit_text(
        f"К сожалению тебе не повезло и проиграл {bet:,}."
        f"\nВыпало число: {value}."
        f"\nХочешь слить ещё раз?",
        reply_markup=kb.r_continue(),
    )


# Обработчик кнопок
async def rbet_callback(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    func = actions[action]
    await func(callback)


async def rvalue_callback(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "even":
        await roullete_roullette(callback, 2, bets_dict["even"])
    elif action == "112":
        await roullete_roullette(callback, 3, range(1, 13))
    elif action == "1324":
        await roullete_roullette(callback, 3, range(13, 25))
    elif action == "2536":
        await roullete_roullette(callback, 3, range(25, 37))
    elif action == "odd":
        await roullete_roullette(callback, 2, bets_dict["odd"])
    elif action == "118":
        await roullete_roullette(callback, 2, range(1, 19))
    elif action == "red":
        await roullete_roullette(callback, 2, bets_dict["red"])
    elif action == "0":
        await roullete_roullette(callback, 37, [0])
    elif action == "black":
        await roullete_roullette(callback, 2, bets_dict["black"])
    elif action == "1936":
        await roullete_roullette(callback, 2, range(19, 37))


async def change_game(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    user_bet = data_bet.get(callback.from_user.id, 0)
    if action == "clear":
        await callback_roulette(callback)
    elif action == "changevalue":
        await value_text(callback=callback, bet=user_bet)
    elif action == "continue":
        await roullete_roullette(
            callback, data_cof[callback.from_user.id], data_value[callback.from_user.id]
        )


# Кнопки ставок
async def one_hundred(callback: types.CallbackQuery):
    roulette_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = roulette_text + "🟢"
    data_bet[callback.from_user.id] = user_bet + 100
    await edit_bet(callback, user_bet + 100)


async def five_hundred(callback: types.CallbackQuery):
    roulette_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = roulette_text + "🟡"
    data_bet[callback.from_user.id] = user_bet + 500
    await edit_bet(callback, user_bet + 500)


async def one_thousand(callback: types.CallbackQuery):
    roulette_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = roulette_text + "🔴"
    data_bet[callback.from_user.id] = user_bet + 1000
    await edit_bet(callback, user_bet + 1000)


async def five_thousand(callback: types.CallbackQuery):
    roulette_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = roulette_text + "🟣"
    data_bet[callback.from_user.id] = user_bet + 5000
    await edit_bet(callback, user_bet + 5000)


async def ten_thousand(callback: types.CallbackQuery):
    roulette_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = roulette_text + "🟠"
    data_bet[callback.from_user.id] = user_bet + 10000
    await edit_bet(callback, user_bet + 10000)


async def fifty_thousand(callback: types.CallbackQuery):
    roulette_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = roulette_text + "🔵"
    data_bet[callback.from_user.id] = user_bet + 50000
    await edit_bet(callback, user_bet + 50000)


async def one_hundred_thousand(callback: types.CallbackQuery):
    roulette_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = roulette_text + "⚪️"
    data_bet[callback.from_user.id] = user_bet + 100000
    await edit_bet(callback, user_bet + 100000)


async def five_hundred_thousand(callback: types.CallbackQuery):
    roulette_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = roulette_text + "🟤"
    data_bet[callback.from_user.id] = user_bet + 500000
    await edit_bet(callback, user_bet + 500000)


async def clear_bet(callback: types.CallbackQuery):
    data_bet[callback.from_user.id] = 0
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = "Твои фишки:"
    await edit_bet(callback, user_bet + 0)


async def confirm(callback: types.CallbackQuery):
    user_bet = data_bet.get(callback.from_user.id, 0)
    await value_text(callback, user_bet + 0)


actions = {
    "hundred": one_hundred,
    "fivehundred": five_hundred,
    "thousand": one_thousand,
    "fivethousand": five_thousand,
    "tenthousand": ten_thousand,
    "fiftythousand": fifty_thousand,
    "hundredthousand": one_hundred_thousand,
    "fivehundredthousand": five_hundred_thousand,
    "clearbet": clear_bet,
    "confirmbet": confirm,
}

bets_dict = {
    "even": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36],
    "odd": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35],
    "red": [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
    "black": [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
}

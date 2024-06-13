from aiogram import types

import data.requests as rq
import apps.keyboards as kb
import random
import time

# Переменные
data_count = {}
data_count_bot = {}
data_deck = []
data_bet = {}
data_text = {}


# Функции функций(текст)
async def edit_bet(callback: types.CallbackQuery, bet: float):
    blackjack_text = data_text.get(callback.from_user.id, "")
    await callback.message.edit_text(
        f"Ты выбрал игру Блекджек. Твоя ставка: {bet:,} " f"\n{blackjack_text}",
        reply_markup=kb.bj_keyboard(),
    )


async def bet_clear(message: types.Message):
    data_bet[message.from_user.id] = 0
    data_text[message.from_user.id] = "Твои фишки:"
    await message.answer(
        "Ты выбрал игру Блекджек. Твои ставка: 0" "\nТвои фишки:",
        reply_markup=kb.bj_keyboard(),
    )


async def user_counts(callback: types.CallbackQuery):
    global data_count, data_count_bot, user_count, user_count_bot
    user_count = data_count.get(callback.from_user.id, 0)
    user_count_bot = data_count_bot.get(callback.from_user.id, 0)
    await callback.message.answer(
        f"У тебя {user_count} очков."
        f"\nУ дилера {user_count_bot} очков."
        f"\n➖➖➖➖➖➖➖"
        f"\nБудешь брать карту?",
        reply_markup=kb.bj_button,
    )


# Функции функций(обработчик)
async def bet_check(callback: types.CallbackQuery, bet: float):
    user_money = await rq.check_balance(callback.from_user.id)
    if user_money >= bet:
        await callback.message.edit_text("Ставка принята, идет запуск.")
        await random_blackjack(callback)
    else:
        await callback.message.edit_text(
            "Эй! Ты поставил ставку больше чем твой баланс. "
            "\nЕсли ты проиграешь, я не хочу тратиться на коллекторов🥱."
        )
    time.sleep(3)
    await callback.message.delete()


# Функции функций(подсчет карт, раздача)
async def random_blackjack(callback: types.CallbackQuery):
    global data_deck, data_count, data_count_bot
    count = 0
    count_bot = 0
    deck = [6, 7, 8, 9, 10, 2, 3, 4, 11] * 4
    random.shuffle(deck)
    time.sleep(0.8)
    await callback.message.answer("Успешно.")
    while True:
        if count < 11:
            current = deck.pop()
            count += current
            continue

        elif count_bot < 1:
            current = deck.pop()
            count_bot += current
            continue

        else:
            data_count[callback.from_user.id] = count
            data_count_bot[callback.from_user.id] = count_bot
            data_deck = deck

            await user_counts(callback)
            await callback.message.delete()
            break


async def user(callback: types.CallbackQuery, count: int):
    global user_count_bot, data_count_bot
    user_count_bot = data_count_bot.get(callback.from_user.id, 0)
    if count == 21:
        await callback.message.answer("Blackjack! Ты выйграл.")
        await win_bj(callback)
    elif count >= 21:
        await callback.message.answer("Проигрыш, ты набрал больше 21 очка😓.")
        await loss_bj(callback)
    elif user_count_bot == 21:
        await callback.message.answer("Ты проиграл, бот выйграл Blackjack😓.")
        await loss_bj(callback)
    elif count == user_count_bot:
        await callback.message.answer(
            "Ничья, ты набрал одинаковое количество очков🙌🏻."
        )
    else:
        await callback.message.answer(
            f"У тебя {count} очков."
            f"\nУ дилера {user_count_bot} очков."
            f"\n➖➖➖➖➖➖➖"
            f"\nБудешь брать карту?",
            reply_markup=kb.bj_button,
        )


async def bot_bj(callback: types.CallbackQuery, count_bot: int):
    global user_count, data_count
    user_count = data_count.get(callback.from_user.id, 0)
    if user_count == 21:
        await callback.message.answer("Blackjack! Ты выйграл.")
        await win_bj(callback)
    elif count_bot == 21:
        await callback.message.answer("Ты проиграли, бот выйграл Blackjack😓.")
        await loss_bj(callback)
    elif count_bot >= 21:
        await callback.message.answer("Победа, бот набрал больше 21 очка.")
        await win_bj(callback)
    elif count_bot > user_count:
        await callback.message.answer("Проигрыш, бот набрал больше очков😓.")
        await loss_bj(callback)
    elif count_bot == user_count:
        await callback.message.answer(
            "Ничья, ты набрал одинаковое количество очков🙌🏻."
        )
    else:
        await callback.message.answer(
            f"У тебя {user_count} очков."
            f"\nУ дилера {count_bot} очков."
            f"\n➖➖➖➖➖➖➖"
            f"\nБудешь брать карту?",
            reply_markup=kb.bj_button,
        )


# Функции функций(зачисление ставок)
async def win_bj(callback: types.CallbackQuery):
    user_bet = data_bet.get(callback.from_user.id, 0)
    await rq.change_balance(tg_id=callback.from_user.id, text_money=user_bet)


async def loss_bj(callback: types.CallbackQuery):
    user_bet = data_bet.get(callback.from_user.id, 0)
    await rq.deprive_balance(tg_id=callback.from_user.id, text_money=user_bet)


# Хендлеры(кнопки)
async def blackjack(message: types.Message):
    await bet_clear(message)


# Обработчик кнопок
async def bet_callback(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    func = actions[action]
    await func(callback)


async def hit(callback: types.CallbackQuery):
    await callback.answer("")
    global data_count, user_count
    user_count = data_count.get(callback.from_user.id, 0)
    current = data_deck.pop()
    time.sleep(0.3)
    await callback.message.edit_text(f"Тебе выпала карта достоинством: {current} очков")
    data_count[callback.from_user.id] = user_count + current
    await user(callback, user_count + current)


async def stand(callback: types.CallbackQuery):
    await callback.answer("")
    global data_count_bot, user_count_bot
    user_count_bot = data_count_bot.get(callback.from_user.id, 0)
    current = data_deck.pop()
    time.sleep(0.3)
    await callback.message.edit_text(
        f"Дилеру выпала карта достоинством: {current} очков"
    )
    data_count_bot[callback.from_user.id] = user_count_bot + current
    await bot_bj(callback, user_count_bot + current)


# Кнопки ставок
async def one_hundred(callback: types.CallbackQuery):
    blackjack_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = blackjack_text + "🟢"
    data_bet[callback.from_user.id] = user_bet + 100
    await edit_bet(callback, user_bet + 100)


async def five_hundred(callback: types.CallbackQuery):
    blackjack_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = blackjack_text + "🟡"
    data_bet[callback.from_user.id] = user_bet + 500
    await edit_bet(callback, user_bet + 500)


async def one_thousand(callback: types.CallbackQuery):
    blackjack_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = blackjack_text + "🔴"
    data_bet[callback.from_user.id] = user_bet + 1000
    await edit_bet(callback, user_bet + 1000)


async def five_thousand(callback: types.CallbackQuery):
    blackjack_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = blackjack_text + "🟣"
    data_bet[callback.from_user.id] = user_bet + 5000
    await edit_bet(callback, user_bet + 5000)


async def ten_thousand(callback: types.CallbackQuery):
    blackjack_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = blackjack_text + "🟠"
    data_bet[callback.from_user.id] = user_bet + 10000
    await edit_bet(callback, user_bet + 10000)


async def fifty_thousand(callback: types.CallbackQuery):
    blackjack_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = blackjack_text + "🔵"
    data_bet[callback.from_user.id] = user_bet + 50000
    await edit_bet(callback, user_bet + 50000)


async def one_hundred_thousand(callback: types.CallbackQuery):
    blackjack_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = blackjack_text + "⚪️"
    data_bet[callback.from_user.id] = user_bet + 100000
    await edit_bet(callback, user_bet + 100000)


async def five_hundred_thousand(callback: types.CallbackQuery):
    blackjack_text = data_text.get(callback.from_user.id, "")
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = blackjack_text + "🟤"
    data_bet[callback.from_user.id] = user_bet + 500000
    await edit_bet(callback, user_bet + 500000)


async def clear_bet(callback: types.CallbackQuery):
    data_bet[callback.from_user.id] = 0
    user_bet = data_bet.get(callback.from_user.id, 0)
    data_text[callback.from_user.id] = "Твои фишки:"
    await edit_bet(callback, user_bet + 0)


async def confirm(callback: types.CallbackQuery):
    user_bet = data_bet.get(callback.from_user.id, 0)
    await bet_check(callback, user_bet + 0)


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

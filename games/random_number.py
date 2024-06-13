from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import types
import apps.handlers as h
import apps.keyboards as kb
import data.requests as rq
import random

num = {}
num2 = {}
coefficient: float = {}
data_bet = {}
random_num: int = 0


# Функции функций(текст)
async def dep_text(message: types.Message, bet: float, state: FSMContext):
    user_money = await rq.check_balance(message.from_user.id)
    if 100 > bet:
        await message.answer("Минимальная ставка: 100 золота🫸.")
    elif user_money >= bet:
        await state.set_state(h.Game.randomnum_c)
        await message.answer(
            f"Хорошо твоя ставка: <b>{bet:,}</b>."
            "\nЧисло может выпасть от 1 до 1.000.000."
            "\n➖➖➖❌➖➖➖➖➖➖▪️➖➖➖"
            "\nВыбери минимальное число диапазона:",
            reply_markup=kb.rnumbutton,
        )
    else:
        await message.answer(
            "Эй! Ты поставил ставку больше чем твой баланс. "
            "\nЕсли ты проиграешь, я не хочу тратиться на коллекторов🥱."
        )
        await state.clear()


async def bet_change(message: Message, state: FSMContext):
    data_bet[message.from_user.id] = 0
    await state.set_state(h.Game.randomnum_bet)
    await message.answer(
        "Ты в игре случайное число!"
        "\n🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰"
        "\nНапиши ставку которую ты готов поставить🫰:"
    )


# FSM хендлеры
async def bet_end(message: types.Message, state: FSMContext):
    try:
        user_bet = data_bet.get(message.from_user.id, 0)
        message_bet = int(message.text)
        data_bet[message.from_user.id] = user_bet + message_bet
        await dep_text(message, user_bet + message_bet, state)
    except ValueError:
        await message.answer("Эу, не ломай бота! Введи ставку в числах а не буквах!")
        await state.clear()


async def input_num(message: types.Message, state: FSMContext):
    try:
        global num
        message_num = int(message.text)
        num[message.from_user.id] = message_num + 0
        await state.set_state(h.Game.randomnum_c1)
        await message.answer(
            "Число может выпасть от 1 до 1.000.000."
            "\n➖➖➖⚫️➖➖➖➖➖➖❌➖➖➖"
            "\nВыбери максимальное число диапазона:",
            reply_markup=kb.rnumbutton,
        )
    except ValueError:
        await message.answer("Эй, не ломай бота! Введи число а не буквы!")
        await state.clear()


async def input_num2(message: types.Message, state: FSMContext):
    try:
        global num, num2
        message_num = int(message.text)
        num2[message.from_user.id] = message_num + 0
        user_num2 = num2.get(message.from_user.id, 0)
        user_num = num.get(message.from_user.id, 0)
        user_bet = data_bet.get(message.from_user.id, 0)
        if user_num2 > user_num:
            gen_range = user_num2 - user_num
            x = gen_range / 10000
            s_coefficient = x * 0.01
            x_cof = 1 / s_coefficient
            coefficient[message.from_user.id] = round(x_cof, 2)
            user_cof = coefficient.get(message.from_user.id, 0)
            await state.clear()
            await message.answer(
                f"Все успешно, подтверди ставку."
                f"\nСтавка: <b>{user_bet:,}</b>."
                f"\nКоэффициент: <b>x{user_cof}</b>."
                f"\nДиапазон: <b>{user_num:,}/{user_num2:,}</b>.",
                reply_markup=kb.rnumbutton_end,
            )
        else:
            await message.answer(
                "По-моему ты перепутал! Поставь второе число больше чем первое."
            )
    except ValueError:
        await message.answer(
            "Эй, последний раз предупреждаю! не ломай бота!\nВведи число а не буквы!"
        )
        await state.clear()


# Команды кнопок
async def clear_rn(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(h.Game.randomnum_bet)
    await callback.message.answer(
        "Ты стер значения.\nНапиши ставку которую ты готов поставить:"
    )


async def confirm_rn(callback: types.CallbackQuery):
    user_money = await rq.check_balance(callback.from_user.id)
    user_bet = data_bet.get(callback.from_user.id, 0)
    await rq.deprive_balance(tg_id=callback.from_user.id, text_money=user_bet)
    if user_money >= user_bet:
        global random_num
        await callback.answer("")
        user_num = num.get(callback.from_user.id, 0)
        user_num2 = num2.get(callback.from_user.id, 0)
        random_num = random.randint(1, 1_000_000)
        if (random_num >= user_num) and (random_num <= user_num2):
            await win_bet(callback)

        else:
            await loss_bet(callback)
    else:
        await callback.message.answer(
            "Эй! Ты поставил ставку больше чем твой баланс. "
            "\nЕсли ты проиграешь, я не хочу тратиться на коллекторов🥱."
        )


# Функции функций(зачисление ставок)
async def loss_bet(callback: types.CallbackQuery):
    user_bet = data_bet.get(callback.from_user.id, 0)
    await callback.message.edit_text(
        f"К сожалению ты проиграли:{user_bet:,}😿."
        f"\n➖➖➖➖➖➖➖➖➖➖"
        f"\nСлучайное число: {random_num:,}",
        reply_markup=kb.rnumbutton_con,
    )


async def win_bet(callback: types.CallbackQuery):
    user_bet = data_bet.get(callback.from_user.id, 0)
    user_cof = coefficient.get(callback.from_user.id, 0)
    coefficient_bet = user_cof * user_bet
    await rq.change_balance(tg_id=callback.from_user.id, text_money=coefficient_bet)
    await callback.message.edit_text(
        f"Поздравляю ты выйграли:{coefficient_bet:,}🎉."
        f"\n➖➖➖➖➖➖➖➖➖➖"
        f"\nСлучайное число: {random_num:,}",
        reply_markup=kb.rnumbutton_con,
    )

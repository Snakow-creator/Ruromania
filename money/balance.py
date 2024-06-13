from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import data.requests as rq
import apps.keyboards as kb
import apps.handlers as h


# Функции функций:
async def get_balance_text(message: types.Message, balance: float):
    await message.answer(
        f"Твой баланс: <b>{balance:,}</b>. \nХочешь пополнить?",
        reply_markup=kb.keyboard_money(),
    )


async def dep_balance_text(message: types.Message, balance: float):
    await message.answer(
        f"Твой баланс: <b>{balance:,}</b>. \nУкажи сколько ты хочешь вывести:"
    )


# Баланс, пополнение:
async def check_money(message: Message):
    user_money = await rq.check_balance(message.from_user.id)
    await get_balance_text(message, user_money)


async def get_money(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    if action == "yes":
        await callback.answer("")
        await state.set_state(h.Bot.money_get)
        await callback.message.edit_text(
            "Напиши мне сколько денег хочешь влить в меня:"
        )
    elif action == "no":
        await callback.answer("")
        await callback.message.edit_text("Ты отказался отдавать нам свои денюжки😢.")


async def get_balance_two(message: types.Message, state: FSMContext):
    try:
        user_money = await rq.check_balance(message.from_user.id)
        message_money = int(message.text)
        await state.clear()
        if user_money <= 1_000_000:
            if message_money <= 1_000_000:
                await rq.change_balance(
                    text_money=message_money, tg_id=message.from_user.id
                )
                await get_balance_text(message, user_money + message_money)
            else:
                await message.answer(
                    "Ошибка, ты не можешь к сожалению положить больше 1 миллиона."
                )
        else:
            await message.answer(
                "Ошибка! У тебя слишком много денег!\nСлей их в казино!"
            )
    except ValueError:
        await message.answer(
            "Ошибка, не пиши белеберду которую я не смогу понять, ведь моя программа расчитана на числа."
        )


# Вывод средств:
async def dep_balance(message: Message, state: FSMContext):
    user_money = await rq.check_balance(message.from_user.id)
    await state.set_state(h.Bot.dep_summa)
    await dep_balance_text(message, user_money)

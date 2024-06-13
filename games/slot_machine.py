from aiogram.types import Message, CallbackQuery
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.fsm.context import FSMContext
import apps.handlers as h
import apps.keyboards as kb
import data.requests as rq
import time

value_data = {}
bet = {}


# Начало
async def input_bet(message: Message, state: FSMContext):
    await state.set_state(h.Game.slot)
    await message.answer(
        "Приветствую в режиме слоты!"
        "\n🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰🟰"
        "\nВведите сумму ставки(cтавить много):"
    )


# Обработчик ставок, запуск слота
async def slot(message: Message, state: FSMContext):
    await state.clear()
    try:
        bet[message.from_user.id] = int(message.text)
        user_bet = bet.get(message.from_user.id, 0)
        user_money = await rq.check_balance(message.from_user.id)
        if user_money >= user_bet:
            value = await message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
            value_data[message.from_user.id] = value.dice.value
            await rq.deprive_balance(tg_id=message.from_user.id, text_money=user_bet)
            await slot_checker(message)
        else:
            await message.answer(
                "Тебе не хватает денег. Хватит сливать бабло иди на работу за новым!"
            )
    except ValueError:
        await message.answer("Ошибка! Тебе нужно водить только числа, понял?")


# Проверка выйгрыша
async def slot_checker(message: Message):
    user_bet = bet.get(message.from_user.id, 0)
    user_value = value_data.get(message.from_user.id, 0)
    time.sleep(2.5)
    if user_value == 64:
        await message.answer("ДЖЖЖЖЕКККПОТ!", reply_markup=kb.slot_button)
        user_bet *= 10
        await rq.change_balance(tg_id=message.from_user.id, text_money=user_bet)
    elif user_value in (52, 63, 62, 61, 60, 56, 48, 32, 16):
        time.sleep(0.5)
        user_bet *= 3
        await rq.change_balance(tg_id=message.from_user.id, text_money=user_bet)
        await message.answer(
            f"2 семерки ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    elif user_value == 1:
        user_bet *= 5
        await rq.change_balance(tg_id=message.from_user.id, text_money=user_bet)
        await message.answer(
            f"3 Бара, ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    elif user_value in (2, 3, 4, 5, 9, 13, 17, 33, 49):
        user_bet *= 1.5
        await rq.change_balance(tg_id=message.from_user.id, text_money=user_bet)
        await message.answer(
            f"2 Бара, ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )

    elif user_value == 22:
        user_bet *= 3
        await rq.change_balance(tg_id=message.from_user.id, text_money=user_bet)
        await message.answer(
            f"3 черники, ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    elif user_value == 33:
        user_bet *= 2
        await rq.change_balance(tg_id=message.from_user.id, text_money=user_bet)
        await message.answer(
            f"3 лимона, ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    else:
        await message.answer("К сожалению ты проиграл☹️.", reply_markup=kb.slot_button)


# Коллбеки, повторный запуск
async def slot_callback(callback: CallbackQuery):
    await callback.answer("")
    user_bet = bet.get(callback.from_user.id, 0)
    user_money = await rq.check_balance(callback.from_user.id)
    if user_money >= user_bet:
        value = await callback.message.answer_dice(emoji=DiceEmoji.SLOT_MACHINE)
        value_data[callback.from_user.id] = value.dice.value
        await rq.deprive_balance(tg_id=callback.from_user.id, text_money=user_bet)
        await slot_checker_callback(callback)
    else:
        await callback.message.edit_text(
            "Тебе не хватает денег. Хватит сливать бабло иди на работу за новым!"
        )


async def slot_checker_callback(callback: CallbackQuery):
    user_bet = bet.get(callback.from_user.id, 0)
    user_value = value_data.get(callback.from_user.id, 0)
    time.sleep(2.5)
    if user_value == 64:
        await callback.message.answer("ДЖЖЖЖЕКККПОТ!", reply_markup=kb.slot_button)
        user_bet *= 10
        await rq.change_balance(tg_id=callback.from_user.id, text_money=user_bet)
    elif user_value in (52, 63, 62, 61, 60, 56, 48, 32, 16):
        user_bet *= 3
        await rq.change_balance(tg_id=callback.from_user.id, text_money=user_bet)
        await callback.message.answer(
            f"2 семерки ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    elif user_value in (2, 3, 4, 5, 9, 13, 17, 33, 49):
        user_bet *= 1.5
        await rq.change_balance(tg_id=callback.from_user.id, text_money=user_bet)
        await callback.message.answer(
            f"2 Бара, ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    elif user_value == 1:
        user_bet *= 5
        await rq.change_balance(tg_id=callback.from_user.id, text_money=user_bet)
        await callback.message.answer(
            f"3 Бара, ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    elif user_value == 22:
        user_bet *= 3
        await rq.change_balance(tg_id=callback.from_user.id, text_money=user_bet)
        await callback.message.answer(
            f"3 черники, ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    elif user_value == 43:
        user_bet *= 2
        await rq.change_balance(tg_id=callback.from_user.id, text_money=user_bet)
        await callback.message.answer(
            f"3 лимона, ты выйграл:<b>{user_bet:,}</b>", reply_markup=kb.slot_button
        )
    else:
        await callback.message.answer(
            "К сожалению ты снова слил☹️.", reply_markup=kb.slot_button
        )

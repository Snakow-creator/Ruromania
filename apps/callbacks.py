from aiogram import types, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from games.blackjack import hit, stand, bet_callback
from games.slot_machine import slot_callback
from games.roulette import rbet_callback, rvalue_callback, change_game
from info.help import info_text

import games.random_number as rn
import money.balance as b
import apps.keyboards as kb


router = Router()


# Кнопки команды help
@router.callback_query(F.data.startswith("info_"))
async def help(callback: CallbackQuery):
    await info_text(callback)


@router.callback_query(F.data == "back")
async def callback_info(callback: CallbackQuery):
    await callback.message.edit_text(
        "Информация обо мне." "\nНиже я ответил на все популярные вопросы:",
        reply_markup=kb.info_keyboard(),
    )


# Пополнение баланса
@router.callback_query(F.data.startswith("get_"))
async def get_balance(callback: CallbackQuery, state: FSMContext):
    await b.get_money(callback, state)


# Случайное число, информация
@router.callback_query(F.data == "faq_num")
async def faq_text(callback: types.CallbackQuery):
    await callback.message.answer(
        "Диапазон в случайных числах - это диапазон чисел которое вы можете выбрать в надежде на то, что в ваш диапазон попадет число."
        "\nПервым число выбирают наименьшее число в диапазоне(минимальное, а вторым уже наибольшее(максимальное)."
        "\nПример: Зона попадения числа составлена от 100.000(минимальная) до 600.000(максимальная), коэффициент <b>x2</b>"
        "\nЧем меньше зона попадения числа тем больше коэффициент выйгрыша, но и шанс выйгрыша уменьшается."
    )


# Случайное число, обработчик кнопок
@router.callback_query(F.data == "clear_rn")
async def fsm_clear(callback: types.CallbackQuery, state: FSMContext):
    await rn.clear_rn(callback, state)


@router.callback_query(F.data == "confirm_rn")
async def fsm_confirm(callback: types.CallbackQuery):
    await rn.confirm_rn(callback)


# Рулетка
@router.callback_query(F.data.startswith("numr_"))
async def r_kb(callback: types.CallbackQuery):
    await rbet_callback(callback)


@router.callback_query(F.data.startswith("button_"))
async def value_kb(callback: types.CallbackQuery):
    await rvalue_callback(callback)


@router.callback_query(F.data.startswith("rgame_"))
async def rgame(callback: types.CallbackQuery):
    await change_game(callback)


# Блекджек, обработчик ставок
@router.callback_query(F.data.startswith("num_"))
async def bj_bet(callback: types.CallbackQuery):
    await bet_callback(callback)


# Блекджек, кнопки взаимодействия
@router.callback_query(F.data == "hit")
async def hit_callback(callback: types.CallbackQuery):
    await hit(callback)


@router.callback_query(F.data == "stand")
async def stand_callback(callback: types.CallbackQuery):
    await stand(callback)


# Слоты: повтор слота
@router.callback_query(F.data == "confirm_slot")
async def retry_slot(callback: types.CallbackQuery):
    await slot_callback(callback)

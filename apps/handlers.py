from aiogram import F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from games.blackjack import blackjack
from games.random_number import bet_end, input_num, input_num2, bet_change
from games.slot_machine import slot, input_bet
from games.roulette import message_roulette
from info.top import top_balance

import time
import apps.keyboards as kb
import data.requests as rq
import money.balance as b


class Bot(StatesGroup):
    dep_summa = State()
    dep_card = State()
    money_get = State()


class Game(StatesGroup):
    randomnum_bet = State()
    randomnum_c = State()
    randomnum_c1 = State()
    slot = State()


x = 0
router = Router()


# Команды
@router.message(CommandStart())
async def start(message: Message):
    await rq.download_users(
        tg_id=message.from_user.id,
        name=message.from_user.first_name,
        fullname=message.from_user.username,
    )
    await message.answer(
        f"Хей {message.from_user.first_name}, добро пожаловать в казино Руромания!"
        f"\nДля начала ознакомься с кнопками ниже⬇️",
        reply_markup=kb.main,
    )


@router.message(Command("help"))
async def help_text(message: Message):
    await message.answer(
        "Информация обо мне." "\nНиже я ответил на все популярные вопросы:",
        reply_markup=kb.info_keyboard(),
    )


@router.message(Command("daily"))
async def daily(message: Message):
    pass


# Кнопки, раздел с играми
@router.message(F.text == "Игры🎮")
async def games(message: Message):
    await message.answer("Выбери игру👇🏻:", reply_markup=kb.main_games)


# Игры, и их фсм обработчики
@router.message(F.text == "Случайное число🎲")
async def random_num(message: Message, state: FSMContext):
    await bet_change(message, state)


@router.message(Game.randomnum_bet)
async def random_fsm(message: types.Message, state: FSMContext):
    await bet_end(message, state)


@router.message(Game.randomnum_c)
async def fsm_rn(message: types.Message, state: FSMContext):
    await input_num(message, state)


@router.message(Game.randomnum_c1)
async def rn_fsm_end(message: types.Message, state: FSMContext):
    await input_num2(message, state)


@router.message(F.text == "Рулетка🏵")
async def message_text_roulette(message: Message):
    await message_roulette(message)


@router.message(F.text == "Блекджек♠️")
async def blackjack_game(message: Message):
    await blackjack(message)


@router.message(F.text == "Слоты🎰")
async def dice_game(message: Message, state: FSMContext):
    await input_bet(message, state)


@router.message(Game.slot)
async def slot_fsm(message: Message, state: FSMContext):
    await slot(message, state)


@router.message(F.text == "Назад⬅️")
async def back(message: Message):
    await message.answer(
        "Ты вернулся назад, выбери кнопку(рекомендую дать нам деняг😝)",
        reply_markup=kb.main,
    )


# Пополнение баланса.
@router.message(F.text == "Баланс💰")
async def balans(message: Message):
    await b.check_money(message)


@router.message(Bot.money_get)
async def get_balance2(message: types.Message, state: FSMContext):
    await b.get_balance_two(message, state)


# Вывод средств
@router.message(F.text == "Вывод средств💸")
async def question(message: Message, state: FSMContext):
    await b.dep_balance(message, state)


@router.message(Bot.dep_summa)
async def card(message: Message, state: FSMContext):
    await state.set_state(Bot.dep_card)
    await message.answer("Укажи номер карты на которую поступят средства:")


@router.message(Bot.dep_card)
async def scam(message: Message, state: FSMContext):
    await message.answer(
        "Деньги поступят в течение 3 рабочих дней, ждите в порядке очереди."
    )
    time.sleep(2.5)
    await message.answer(
        "(Казино находится в Финляндии, могут быть задержки в переводе, ждите.)"
    )
    await state.clear()


# Инфо
@router.message(F.text == "Информация♟")
async def dep_money(message: Message):
    await message.answer(
        "Версия бота -- 1.0.0 release."
        '\n\n"Можно долго ждать обновлений, а можно играть в казино руромания."'
    )


@router.message(F.text == "Топ пользователей🏆")
async def top_text(message: Message):
    await top_balance(message)


# Обработка хендлера на ошибочный текст
@router.message(F.text)
async def text(message: Message):
    await message.answer(
        "Похоже ты что-то не то написал. \nЛучше нажми на кнопку👇🏻👇🏻"
    )

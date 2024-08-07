from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.insert(button)
kb.insert(button2)
kb.insert(button3)

kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button_in = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data="calories")
button_in2 = InlineKeyboardButton(text='Формулы расчёта', callback_data="formulas")
kb_in.insert(button_in)
kb_in.insert(button_in2)


kb_buy = InlineKeyboardMarkup(resize_keyboard=True)
button_buy = InlineKeyboardButton(text='Смеситель', callback_data="product_buying")
button_buy2 = InlineKeyboardButton(text='Полотенцесушитель', callback_data="product_buying")
button_buy3 = InlineKeyboardButton(text='Ванна', callback_data="product_buying")
button_buy4 = InlineKeyboardButton(text='Унитаз', callback_data="product_buying")
kb_buy.insert(button_buy)
kb_buy.insert(button_buy2)
kb_buy.insert(button_buy3)
kb_buy.insert(button_buy4)

s = 0
@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def  main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb_in)


@dp.callback_query_handler(text="formulas")
async def  get_formulas(call):
    await call.message.answer("Формула Миффлина-Сан Жеора для мужчин: 10 х вес (кг) + 6,25 x рост (см)"
                              " – 5 х возраст (г) + 5")


@dp.message_handler(text="Купить")
async def  get_buying_list(message):
    with open("AQ1080CR.jpg", "rb") as img:
        await message.answer_photo(img, "Название: Смеситель | Описание: Смеситель для кухни | Цена: 9028 руб.")
    with open("AQ_KP0760CH.jpg", "rb") as img:
        await message.answer_photo(img, "Название: Полотенцесушитель |"
                                        " Описание: Полотенцесушитель водяной | Цена: 16146 руб.")
    with open("a032039f44b57ee1116a524dd65ef88d.jpg", "rb") as img:
        await message.answer_photo(img, "Название: Ванна |"
                                        " Описание:  Ванна акриловая | Цена: 28170 руб.")
    with open("unitaz_podvesnoy_aquatek_vega_aq1905_mb_s_sidenem_soft_close_chernyy_matovyy.jpg", "rb") as img:
        await message.answer_photo(img, "Название: Унитаз |"
                                        " Описание:  Унитаз подвесной | Цена: 28094 руб.")


    await message.answer("Выберите продукт для покупки:", reply_markup=kb_buy)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(ag=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(grow=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weig=message.text)
    data = await state.get_data()
    norma = int(10 * int(data['weig']) + 6.25 * int(data['grow']) - 5 * int(data['ag']) + 5)
    await message.answer(f"Ваша норма в сутки {norma} ккал")
    await state.finish()


#     для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

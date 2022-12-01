import nest_asyncio
import random
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile, ReplyKeyboardRemove
from aiogram.dispatcher import Dispatcher, FSMContext
import statistics

token_file = open("token.txt", 'r', encoding='UTF8')
my_token = token_file.readline()
token_file.close()
definitions_files = open("defenitions.txt", "r", encoding="UTF8")
lines = definitions_files.readlines()
definition_length = len(lines)
nest_asyncio.apply()
bot = Bot(token=my_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    definit = State()
    answer = State()
    correct = State()
    start = State()


#функция старта
@dp.message_handler(commands=['help', 'start', 'reg'])
async def process_help_command(message: types.Message):
    kb = [[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="выберите")
    await bot.send_message(message.from_user.id,
                           "Привет, я бот для подготовки к экзамену по матанализу. Со мной ты без проблем "
                           "выучишь все определения на отлично. Во время работы тебе будут выдваться"
                           " рандомизированные определения. Твоя задача - максимально подробно его вспомнить."
                           "Начнем?", reply_markup=keyboard)
    await Form.start.set()


#Выбор определение или статистика
@dp.message_handler(state=Form.start)
async def process_help_command(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        kb = [[types.KeyboardButton(text="Новое определение"), types.KeyboardButton(text="Статистика")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                             input_field_placeholder="выберите")
        await bot.send_message(message.from_user.id,
                               "Отлично, теперь выберите", reply_markup=keyboard)
        await Form.definit.set()
    elif message.text.lower() == 'нет':
        await message.answer("Хорошего дня!", reply_markup=ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(state=Form.definit)
async def ShowDefinition(message: types.Message, state: FSMContext):
    if message.text.lower() == 'новое определение':
        idx = random.randrange(definition_length)
        def_name, def_path, def_ticket = lines[idx].split(" & ")
        def_ticket = def_ticket.replace('\n', '')
        kb = [[types.KeyboardButton(text="Показать правильный ответ")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                             input_field_placeholder="Когда будете готовы - нажмите кнопку")
        await bot.send_message(message.from_user.id, def_name, reply_markup=keyboard)
        await Form.answer.set()
        await state.update_data(path=def_path, name=def_name, ticket=def_ticket)
    elif message.text.lower() == "статистика":
        new_statistic = statistics.get_statistics(message.from_user.id)
        kb = [[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Продолжим?")
        await message.answer(new_statistic, reply_markup=keyboard)
        await Form.start.set()


@dp.message_handler(state=Form.answer)
async def show_answer(message: types.Message, state: FSMContext):
    if message.text.lower() == "показать правильный ответ":
        data = await state.get_data()
        definition = InputFile("definitions/" + data["path"])
        await bot.send_photo(message.from_user.id, photo=definition, caption=data["name"],
                             reply_markup=ReplyKeyboardRemove())
        kb = [[types.KeyboardButton(text="да, все верно"), types.KeyboardButton(text="Нет, ошибся/лась")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                             input_field_placeholder="выберите")
        await message.answer("Правильно ли вы записали определение?", reply_markup=keyboard)
        await Form.correct.set()


@dp.message_handler(state=Form.correct)
async def check_if_correct(message: types.Message, state: FSMContext):
    kb = [[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="выберите")
    data = await state.get_data()
    if message.text.lower() == "да, все верно":
        statistics.update_data(message.from_user.id, True, data["ticket"])
        await message.answer("Вы большой/ая молодец, продолжим?",
                             reply_markup=keyboard)
    elif message.text.lower() == 'нет, ошибся/лась':
        statistics.update_data(message.from_user.id, False, data["ticket"])
        await message.answer("Не стоит расстраиваться, продолжим?",
                             reply_markup=keyboard)
    await Form.start.set()

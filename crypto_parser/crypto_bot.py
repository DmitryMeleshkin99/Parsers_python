import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import message
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import time

bot = Bot(token='2102158434:AAF9CXY3hXEstC7PQ_RP_R9q2OfXIRrc2HI', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Узнать курсы криптовалют']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer('Этот бот показывает текущие курсы криптовалюты', reply_markup=keyboard)

@dp.message_handler(Text(equals='Узнать курсы криптовалют'))
async def crypto(message: types.Message):
    await message.answer('Ожидайте')

    with open('ready.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        for key,value in data.items():
            time.sleep(2)
            card = f"{hbold('Название: ')} {key}\n" \
                f"{hbold('Цена: ')} {value}🔥\n" \
            
            await message.answer(card)


def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()

            


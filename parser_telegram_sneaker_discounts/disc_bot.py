import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import message
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import time


bot = Bot(token='2081712760:AAEHBgsdrRpzLEXErlcMappq6UgnPsb3_dM', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Кроссовки SneakerHead со скидками 🤑','Кроссовки Multisport со скидкой 💰']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Discounted goods!\nThis bot supports commands such as:\n /start\n/sales ', reply_markup=keyboard)



@dp.message_handler(commands='sales')
async def sales(message: types.Message):
    await message.send_message("Select a store from the offered buttons")

@dp.message_handler(Text(equals='Кроссовки SneakerHead со скидками 🤑'))
async def get_discount_sneakerhead(message: types.Message):
    await message.answer('Please waiting...')


    with open('ready.json', 'r', encoding='utf-8') as file:
        data_sneakerhead = json.load(file)

    for item in data_sneakerhead:
        time.sleep(1)
        card_sneakerhead = f"{hlink(item.get('title'), item.get('link'))}\n" \
            f"{hbold('Цена со скидкой')} {item.get('sale')}🔥\n" \
            f"{hbold('Цена без скидки')} {item.get('price')}\n"

        await message.answer(card_sneakerhead)

@dp.message_handler(Text(equals='Кроссовки Multisport со скидкой 💰'))
async def get_discount_multisport(message: types.Message):
    await message.answer('Please waiting...')

    with open('ready_multisport.json', 'r', encoding='utf-8') as file:
        data_multisport = json.load(file)

    for item in data_multisport:
        time.sleep(1)
        card_multisport = f"{hlink(item.get('title'), item.get('link'))}\n" \
            f"{hbold('Цена со скидкой')} {item.get('price')}🔥\n" \
            f"{hbold('Цена без скидки')} {item.get('old_price')}\n"


        await message.answer(card_multisport)



        



def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()
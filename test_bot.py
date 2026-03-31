import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "8723535602:AAHM_9VBMBLu6mM_VfkvEgi885Sv_D4OhmE" 

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    print("BOT GOT /start")
    await message.answer("Бот працює! Напиши щось.")

@dp.message_handler()
async def echo(message: types.Message):
    print("BOT GOT:", message.text)
    await message.answer("Я отримав: " + message.text)

if __name__ == "__main__":
    print("BOT STARTED")
    executor.start_polling(dp, skip_updates=False)
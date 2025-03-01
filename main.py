import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv
import os
from aiogram.utils.markdown import hbold
from googletrans import Translator


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()
translator = Translator()

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    kb = [
        [
            KeyboardButton(text="Слова"),
            KeyboardButton(text="Грамматика"),
            KeyboardButton(text="Переводчик")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите.."
    )
    await message.answer('Привет!\nВыбири, что ты хочешь учить:\n-Слова\n-Грамматика', reply_markup=keyboard)


@dp.message(F.text == 'Слова')
async def word_message(message: Message):
    await message.answer( text="Сейчас пришлю список слов которые тебе нужно выучить")

@dp.message(F.text == 'Грамматика')
async def word_message2(message: Message):
    await message.answer( text="Сейчас пришлю задание по грамматике")

@dp.message(F.text == 'Переводчик')
async def word_message3(message: Message):
    await message.answer( text="Запускаю режим переводчика")




@dp.message(F.text == 'Переводчик')
async def user_text(message):
    translator = Translator()

    # Определение языка ввода.
    lang = translator.detect(message.text)
    lang = lang.lang

    # Если ввод по русски, то перевести на английский по умолчанию.
    # Если нужен другой язык, измени <message.text> на <message.text, dest='нужный язык'>.
    if lang == 'ru':
        send = translator.translate(message.text)
        await bot.reply_to(message, '------\n'+ send.text +'\n------')

    # Иначе другой язык перевести на русский {dest='ru'}.
    else:
        send = translator.translate(message.text, dest='ru')
        await bot.reply_to(message, '------\n'+ send.text +'\n------')





@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


dp.message.register(word_message, F.text)
dp.message.register(word_message2, F.text)
dp.message.register(word_message3, F.text)
dp.message.register(user_text, F.text)
asyncio.run(bot.infinity_polling())

if __name__ == '__main__':
    dp.run_polling(bot)

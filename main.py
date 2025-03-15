from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv
import os
import logging
from translate import Translator

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

ru_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
en_letters = 'abcdefghigkopqrstuvwxyz'



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
async def echo(message: Message):
    await message.answer( text="Запускаю режим переводчика")
    text = message.text
    if text[0].lower() in ru_letters:
        translator = Translator(from_lang="russion", to_lang="english")
    elif text[0].lower() in en_letters:
        translator = Translator(from_lang="english", to_lang="russion")
    else:
        await message.answer('Я тебя не понимаю')
        return
    
    translation = translator.translate(text)
    await message.answer(translation)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


dp.message.register(word_message, F.text)
dp.message.register(word_message2, F.text)
dp.message.register(echo, F.text)

if __name__ == '__main__':
    dp.run_polling(bot)
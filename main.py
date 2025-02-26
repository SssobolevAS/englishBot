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

@dp.message(text=Message.text)
async def translate(message:Message):
    try:
        translated = translator.translate(message.text, dest="en")
        await message.answer(
            f"Перевод:\n{hbold(translated.text)}"
        )
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


async def main():
    await dp.start_polling()




@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


dp.message.register(word_message, F.text)
dp.message.register(word_message2, F.text)
dp.message.register(word_message3, F.text)


if __name__ == '__main__':
    dp.run_polling(bot)

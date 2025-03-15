from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os
from dotenv import load_dotenv
import logging
from translate import Translator

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

ru_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
en_letters = 'abcdefghigkopqrstuvwxyz'

# Dictionary to track translation mode state for each user
translation_mode = {}

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
    await message.answer(text="Сейчас пришлю список слов которые тебе нужно выучить")

@dp.message(F.text == 'Грамматика')
async def word_message2(message: Message):
    await message.answer(text="Сейчас пришлю задание по грамматике")

@dp.message(F.text == 'Переводчик')
async def activate_translation_mode(message: Message):
    user_id = message.from_user.id
    translation_mode[user_id] = True
    await message.answer(text="Режим переводчика активирован. Отправьте текст для перевода. Чтобы выйти, используйте команду /stop_translate.")

@dp.message(Command(commands=['stop_translate']))
async def deactivate_translation_mode(message: Message):
    user_id = message.from_user.id
    if user_id in translation_mode:
        del translation_mode[user_id]
    await message.answer(text="Режим переводчика деактивирован.")

@dp.message()
async def handle_messages(message: Message):
    user_id = message.from_user.id
    if user_id in translation_mode:
        text = message.text
        try:
            if text[0].lower() in ru_letters:
                translator = Translator(from_lang="russian", to_lang="english")
            elif text[0].lower() in en_letters:
                translator = Translator(from_lang="english", to_lang="russian")
            else:
                await message.answer('Я тебя не понимаю')
                return

            translation = translator.translate(text)
            await message.answer(translation)
        except RuntimeError:
            await message.answer('Произошла ошибка при переводе. Пожалуйста, попробуйте еще раз.')
    else:
        await message.answer("Я не понимаю команду. Пожалуйста, выберите действие или используйте /help для получения справки.")

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )

if __name__ == '__main__':
    dp.run_polling(bot)

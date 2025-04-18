from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
import os
from dotenv import load_dotenv
import logging
from translate import Translator
from word import *
from w_test import *
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from aiogram.utils.markdown import text, bold, italic
from gr import grammar_a, grammar_a1, grammar_a2, grammar_b1, grammar_b2, grammar_c1, grammar_c2

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

ru_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
en_letters = 'abcdefghigkopqrstuvwxyz'

translation_mode = {}
user_levels = {}
user_data = {}

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    kb = [
        [InlineKeyboardButton(text="Тест на уровень английского", callback_data="english_test")],
        [InlineKeyboardButton(text="A - Basic User", callback_data="level_A")],
        [InlineKeyboardButton(text="A1 - Beginner", callback_data="level_A1"), InlineKeyboardButton(text="A2 - Elementary", callback_data="level_A2")],
        [InlineKeyboardButton(text="B - Independent User", callback_data="level_B")],
        [InlineKeyboardButton(text="B1 - Intermediate", callback_data="level_B1"), InlineKeyboardButton(text="B2 - Upper-Intermediate", callback_data="level_B2")],
        [InlineKeyboardButton(text="C - Proficient User", callback_data="level_C")],
        [InlineKeyboardButton(text="C1 - Advanced", callback_data="level_C1"), InlineKeyboardButton(text="C2 - Proficiency", callback_data="level_C2")],
        [InlineKeyboardButton(text="Переводчик", callback_data="translator")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer('Привет! Я бот который поможет тебе учить английский в сфере IT, или просто помогу тебе перевести любое слово через кнопку "Переводчик".\n Для начала выбери свой уровень.\nЕсли не знаешь какой уровень у тебя, пройди тест', reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('level_'))
async def process_level_command(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_levels[user_id] = callback_query.data
    kb = [
        [InlineKeyboardButton(text="Слова", callback_data="words"), InlineKeyboardButton(text="Грамматика", callback_data="grammar"), InlineKeyboardButton(text="Переводчик", callback_data="translator")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await callback_query.message.answer('Отлично!\nВыбири, что ты хочешь учить:\n-Слова\n-Грамматика\n-Переводчик', reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == 'english_test')
async def start_english_test(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_data[user_id] = {"score": 0, "answered_questions": set()}
    await ask_question(user_id, 0, callback_query.message)
    await callback_query.answer()

async def ask_question(user_id, question_index, message: Message):
    if question_index < len(questions):
        question = questions[question_index]
        kb = [
            [InlineKeyboardButton(text=answer, callback_data=f"answer_{question_index}_{answer}")]
            for answer in question["answers"]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer(question["question"], reply_markup=keyboard)
    else:
        await calculate_result(user_id, message)

@dp.callback_query(lambda c: c.data.startswith('answer'))
async def process_answer(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    _, question_index, answer = callback_query.data.split('_')
    question_index = int(question_index)

    if question_index in user_data[user_id]["answered_questions"]:
        await callback_query.answer("Ответ нельзя исправить", show_alert=True)
    else:
        user_data[user_id]["answered_questions"].add(question_index)
        if question_index < len(questions):
            correct_answer = questions[question_index]["correct_answer"]
            if answer == correct_answer:
                user_data[user_id]["score"] += 1

            await ask_question(user_id, question_index + 1, callback_query.message)
            await callback_query.answer()

async def calculate_result(user_id, message: Message):
    score = user_data[user_id]["score"]
    total_questions = len(questions)
    result_message = f"Вы ответили правильно на {score} из {total_questions} вопросов."

    if score == total_questions:
        user_levels[user_id] = "level_C2"
        result_message += " Ваш уровень английского языка - C2 - Proficiency!"
    elif score >= total_questions * 0.8:
        user_levels[user_id] = "level_C1"
        result_message += " Ваш уровень английского языка - C1 - Advanced."
    elif score >= total_questions * 0.6:
        user_levels[user_id] = "level_B2"
        result_message += " Ваш уровень английского языка - B2 - Upper-Intermediate."
    elif score >= total_questions * 0.4:
        user_levels[user_id] = "level_B1"
        result_message += " Ваш уровень английского языка - B1 - Intermediate."
    elif score >= total_questions * 0.2:
        user_levels[user_id] = "level_A2"
        result_message += " Ваш уровень английского языка - A2 - Elementary."
    else:
        user_levels[user_id] = "level_A1"
        result_message += " Ваш уровень английского языка - A1 - Beginner."

    kb = [
        [InlineKeyboardButton(text="Слова", callback_data="words")],
        [InlineKeyboardButton(text="Грамматика", callback_data="grammar")],
        [InlineKeyboardButton(text="Переводчик", callback_data="translator")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    await message.answer(result_message, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == 'words')
async def word_message(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_level = user_levels.get(user_id)

    if user_level:
        words_map = {
            "level_A": word_a1,
            "level_A1": word_a1,
            "level_A2": word_a2,
            "level_B": word_b1,
            "level_B1": word_b1,
            "level_B2": word_b2,
            "level_C": word_c1,
            "level_C1": word_c1,
            "level_C2": word_c2
        }

        words = words_map.get(user_level, [])
        words_text = "\n".join(words)
        await callback_query.message.answer(text=f"Вот список слов для уровня {user_level}:\n\n{words_text}\n Тест по словам будет отправлен вам в 13:00.")
        await callback_query.answer()

        # Schedule the word test for 13:00
        scheduler.add_job(send_word_test, 'cron', hour=13, minute=0, args=[user_id, user_level], id=f"test_job_{user_id}")

async def send_word_test(user_id, user_level):
    kb = [
        [InlineKeyboardButton(text="Да", callback_data="ready_for_test")],
        [InlineKeyboardButton(text="Нет", callback_data="not_ready_for_test")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(user_id, "Готов ли ты проходить тест?", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == 'ready_for_test')
async def start_test(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_level = user_levels.get(user_id)

    test_questions = word_tests.get(user_level, [])
    user_data[user_id] = {"score": 0, "incorrect_answers": [], "current_question": 0}

    await send_next_question(user_id, user_level)

async def send_next_question(user_id, user_level):
    user_data_entry = user_data.get(user_id)
    if not user_data_entry:
        return

    current_question = user_data_entry["current_question"]
    test_questions = word_tests.get(user_level, [])

    if current_question < len(test_questions):
        question_data = test_questions[current_question]
        kb = [
            [InlineKeyboardButton(text=option, callback_data=f"word_test_{current_question}_{option}")]
            for option in question_data["options"]
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

        for row in kb:
            for button in row:
                if len(button.callback_data) > 64:
                    raise ValueError(f"Callback data is too long: {button.callback_data}")

        message = await bot.send_message(user_id, text=f"Вопрос {current_question + 1}: {question_data['question']}", reply_markup=keyboard)
        user_data[user_id]["current_message_id"] = message.message_id
    else:
        await finish_test(user_id, user_level)

@dp.callback_query(lambda c: c.data == 'not_ready_for_test')
async def repeat_readiness_check(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    kb = [
        [InlineKeyboardButton(text="Да", callback_data="ready_for_test")],
        [InlineKeyboardButton(text="Нет", callback_data="not_ready_for_test")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await bot.send_message(user_id, "Готов ли ты проходить тест?", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith('word_test'))
async def process_word_test_answer(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    _, question_index, answer = callback_query.data.rsplit('_', 2)
    question_index = int(question_index)

    user_level = user_levels.get(user_id)
    test_questions = word_tests.get(user_level, [])
    correct_answer = test_questions[question_index]["correct"]

    if answer != correct_answer:
        user_data[user_id]["incorrect_answers"].append((test_questions[question_index]["question"], correct_answer))

    await bot.edit_message_reply_markup(chat_id=str(user_id), message_id=user_data[user_id]["current_message_id"], reply_markup=None)

    user_data[user_id]["current_question"] += 1
    await send_next_question(user_id, user_level)

async def finish_test(user_id, user_level):
    incorrect_answers = user_data[user_id]["incorrect_answers"]
    if incorrect_answers:
        incorrect_text = "\n".join([f"{question}: {answer}" for question, answer in incorrect_answers])
        await bot.send_message(user_id, f"Вот список слов, в которых вы ошиблись:\n\n{incorrect_text}")

        # Reschedule the test for the next day at 13:00
        scheduler.add_job(send_word_test, 'cron', hour=13, minute=0, args=[user_id, user_level], id=f"test_job_{user_id}")
    else:
        await bot.send_message(user_id, "Поздравляю! Вы ответили правильно на все вопросы!")

        # Move to the next level
        next_level = get_next_level(user_level)
        if next_level:
            user_levels[user_id] = next_level
            await word_message(CallbackQuery(from_user=types.User(id=user_id), data='words'))

def get_next_level(current_level):
    level_order = ["level_A1", "level_A2", "level_B1", "level_B2", "level_C1", "level_C2"]
    if current_level in level_order:
        current_index = level_order.index(current_level)
        if current_index < len(level_order) - 1:
            return level_order[current_index + 1]
    return None

async def on_startup(dp):
    scheduler.start()

grammar_map = {
    "level_A": grammar_a,
    "level_A1": grammar_a1,
    "level_A2": grammar_a2,
    "level_B": grammar_b1,
    "level_B1": grammar_b1,
    "level_B2": grammar_b2,
    "level_C": grammar_c1,
    "level_C1": grammar_c1,
    "level_C2": grammar_c2
}

@dp.callback_query(F.text == 'grammar')
async def word_message2(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user_level = user_levels.get(user_id)

    if user_level:
        grammar_material = grammar_map.get(user_level, "Материал по грамматике недоступен для вашего уровня.")

        # Отправляем текстовое сообщение
        await callback_query.message.answer(text=f"Вот материал по грамматике для уровня *{user_level}*:\n\n{grammar_material}", parse_mode="Markdown")

        # Отправляем картинку для уровней A2 и C1
        if user_level in ["level_A2", "level_C1"]:
            photo_path = os.path.abspath(f'images/grammar_{user_level}.jpg')  # Абсолютный путь к картинке
            if not os.path.exists(photo_path):
                await callback_query.message.answer("Извините, картинка не найдена.")
                return
            photo = FSInputFile(photo_path)  # Используем FSInputFile
            await callback_query.message.answer_photo(photo=photo, caption=f"Вот дополнительный материал по грамматике для уровня {user_level}.")
    else:
        await callback_query.message.answer(text="Пожалуйста, выберите свой уровень, чтобы получить материал по грамматике.")

    await callback_query.answer()

@dp.callback_query(lambda c: c.data == 'translator')
async def activate_translation_mode(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    translation_mode[user_id] = True
    await callback_query.message.answer(text="Режим переводчика активирован. Отправьте текст для перевода. Чтобы выйти, используйте команду /stop_translate.")
    await callback_query.answer()

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
    dp.run_polling(bot, timeout=60)
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)
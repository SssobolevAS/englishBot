from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
from dotenv import load_dotenv
import logging
from translate import Translator

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

questions = [
    {"question": "What is the correct form of the question?", "answers": ["Where are you from?", "What is your from?", "What from are you?", "Where you from?"], "correct_answer": "Where are you from?"},
    {"question": "_____ Alex work for BMW?", "answers": ["Do", "Does", "Has", "Is"], "correct_answer": "Does"},
    {"question": "Where _____ yesterday at 10 p.m. ?", "answers": ["did you be", "were you", "was you", "are you"], "correct_answer": "were you"},
    {"question": "I don’t have _____ money.", "answers": ["some", "many", "much", "any"], "correct_answer": "any"},
    {"question": "What’s that noise? The neighbour’s  son _____ the violin.?", "answers": ["plays", "play", "is playing", "played"], "correct_answer": "is playing"},
    {"question": "Jake _____ off his bike when he was cycling home.", "answers": ["has fallen", "was falling", "fell", "is falling"], "correct_answer": "fell"},
    {"question": " Moscow is _____ city in Russia.", "answers": ["biggest", "the bigger", "the biggest", "big"], "correct_answer": "the biggest"},
    {"question": "_____ the Republic of Kalmykia?.", "answers": ["Do you ever be in", "Have you ever been to", "Have you ever been in", "Has you ever been in"], "correct_answer": "Have you ever been to"},
    {"question": " If you  _____ well, you’ll speak English fluently.", "answers": ["would study", "study", "will study", "will be stading"], "correct_answer": "study"},
    {"question": "_____ to have short hair when she was young?", "answers": ["Did she use", "Did she used", "Was she used", "Does she use"], "correct_answer": "Did she use"},
    {"question": "Marty asked me _____ .", "answers": ["what did the time was", "what was the time", "what the time was", "what does the time be"], "correct_answer": "is what the time was"},
    {"question": "My son loves _____ chocolate cake.", "answers": [" - ", "the", "a", "an"], "correct_answer": " - "},
    {"question": " The show _____ when we arrived.", "answers": ["had already finished", "the has already finish", "has already finished", "had already finish"], "correct_answer": "had already finifed"},
    {"question": "Mum! You have red eyes. _____ Titanic again?", "answers": ["Have you been watching", "Did you watch", "Were you watching", "Have you watched"], "correct_answer": "Have you been watching"},
    {"question": " Fred _____ late yesterday, I saw his car next to the office.", "answers": ["can have worked", "must have worked", "should have worked", "must work"], "correct_answer": "must have worked"}
]

ru_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
en_letters = 'abcdefghigkopqrstuvwxyz'

# Dictionary to track translation mode state for each user
translation_mode = {}

# Storage for user answers and scores
user_data = {}

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    kb = [
        [KeyboardButton(text="Тест на уровень английского")],
        [KeyboardButton(text="A - Basic User")],
        [KeyboardButton(text="A1 - Beginner"), KeyboardButton(text="A2 - Elementary")],
        [KeyboardButton(text="B - Independent User")],
        [KeyboardButton(text="B1 - Intermediate"), KeyboardButton(text="B2 - Upper-Intermediate")],
        [KeyboardButton(text="C - Proficient User")],
        [KeyboardButton(text="C1 - Advanced"), KeyboardButton(text="C2 - Proficiency")],
        [KeyboardButton(text="Переводчик")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите.."
    )
    await message.answer('Привет! Я бот который поможет тебе учить английский в сфере IT, или просто помогу тебе перевести любое слово через кнопку "Переводчик".\n Для начала выбери свой уровень.\nЕсли не знаешь какой уровень у тебя, пройди тест', reply_markup=keyboard)

@dp.message(F.text == 'A - Basic User')
@dp.message(F.text == 'A1 - Beginner')
@dp.message(F.text == 'A2 - Elementary')
@dp.message(F.text == 'B - Independent User')
@dp.message(F.text == 'B1 - Intermediate')
@dp.message(F.text == 'B2 - Upper-Intermediate')
@dp.message(F.text == 'C - Proficient User')
@dp.message(F.text == 'C1 - Advanced')
@dp.message(F.text == 'C2 - Proficiency')
async def process_level_command(message: Message):
    kb = [
        [KeyboardButton(text="Слова"), KeyboardButton(text="Грамматика"), KeyboardButton(text="Переводчик")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите.."
    )
    await message.answer('Отлично!\nВыбири, что ты хочешь учить:\n-Слова\n-Грамматика\n-Переводчик', reply_markup=keyboard)

@dp.message(F.text == 'Тест на уровень английского')
async def start_english_test(message: Message):
    user_id = message.from_user.id
    user_data[user_id] = {"score": 0, "current_question": 0}
    await ask_question(user_id, 0, message)

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
        result_message += " Ваш уровень английского языка - C2 - Proficiency!"
    elif score >= total_questions * 0.8:
        result_message += " Ваш уровень английского языка - C1 - Advanced."
    elif score >= total_questions * 0.6:
        result_message += " Ваш уровень английского языка - B2 - Upper-Intermediate."
    elif score >= total_questions * 0.4:
        result_message += " Ваш уровень английского языка - B1 - Intermediate."
    elif score >= total_questions * 0.2:
        result_message += " Ваш уровень английского языка - A2 - Elementary."
    else:
        result_message += " Ваш уровень английского языка - A1 - Beginner."

    await message.answer(result_message)

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
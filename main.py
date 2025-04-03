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

word_a1 = [
    "computer - компьютер", "internet - интернет", "email - электронная почта",
    "website - веб-сайт", "software - программное обеспечение",
    "hardware - аппаратное обеспечение", "mouse - мышь",
    "keyboard - клавиатура", "screen - экран", "laptop - ноутбук",
    "phone - телефон", "app - приложение", "browser - браузер",
    "download - скачивать", "upload - загружать", "file - файл",
    "folder - папка", "save - сохранять", "delete - удалять",
    "copy - копировать"
]

word_a2 = [
    "paste - вставлять", "password - пароль",
    "user - пользователь", "account - аккаунт", "login - вход",
    "logout - выход", "search - поиск", "link - ссылка",
    "click - кликать", "double-click - двойной клик", "icon - иконка",
    "window - окно", "desktop - рабочий стол", "printer - принтер",
    "scan - сканировать", "print - печатать", "memory - память",
    "storage - хранилище", "Wi-Fi (Wireless Fidelity) - технология беспроводной локальной сети", "cable - кабель"
]

word_b1 = [
    
    "network - сеть", "server - сервер", "database - база данных",
    "firewall - межсетевой экран", "router - маршрутизатор",
    "modem - модем", "bandwidth - пропускная способность",
    "IP address (Internet Protocol) -  уникальный числовой идентификатор устройства", "domain - домен", "host - хост",
    "protocol - протокол", "HTTP (HyperText Transfer Protocol) - протокол передачи данных в интернете", "HTTPS (HyperText Transfer Protocol Secure) -  расширение протокола HTTP",
    "FTP (File Transfer Protocol) - протокол для передачи файлов между клиентом и сервером", " URL (Uniform Resource Locator) - унифицированный указатель ресурса", "DNS (Domain Name System) - система доменных имён", 
    "proxy -  промежуточный сервер между пользователем интернета и серверами",
    "VPN (Virtual Private Network) - виртуальная частная сеть", "encryption - шифрование", "decryption - дешифрование", "analytics - аналитика"
]
    
word_b2 = [
    "algorithm - алгоритм", "backup - резервное копирование",
    "restore - восстановление", "patch - фрагмент кода", "update - обновление",
    "driver - драйвер", "interface - интерфейс", "framework - фреймворк",
    "library - библиотека", " API (Application Programming Interface) - набор правил и протоколов, который позволяет различным программным приложениям взаимодействовать друг с другом", "cloud - облако",
    "virtual - виртуальный", "cluster - кластер", "load - нагрузка",
    "balance - баланс", "cache - кэш", "cookie - небольшой текстовый файл",
    "session -  определённый промежуток времени", "authentication - аутентификация",
    "authorization - авторизация", "permission - разрешение",
    "role - роль", "administrator - администратор"
    ]

word_c1 = [
    "cybersecurity - кибербезопасность", "malware - вредоносное ПО",
    "virus - вирус", "trojan - вид вредоносного программного обеспечения", "ransomware - программа-вымогатель",
    "phishing - фишинг", "exploit - эксплойт", "vulnerability - уязвимость",
    "penetration - проникновение", "intrusion - вторжение",
    "forensics - судебная экспертиза", "cryptography - криптография",
    "blockchain - блокчейн", "quantum computing - квантовые вычисления",
    "artificial intelligence - искусственный интеллект",
    "machine learning - машинное обучение", "deep learning - глубокое обучение",
    "neural network - нейронная сеть", "data mining - майнинг данных",
    "big data - большие данные"
]
word_c2 = [
    "visualization - визуализация", "dashboard - панель управления",
    "pipeline - конвейер", "ETL (Extract, transform, load) -  трёхэтапный вычислительный процесс", "data warehouse - хранилище данных",
    "OLAP (On-Line Analytical Processing) - анализ данных в реальном времени", "business intelligence - бизнес-аналитика",
    "agile - гибкий", "scrum - скрам (методика гибкого управления проектами)", "sprint - спринт (небольшой фиксированный отрезок времени)",
    "backlog - бэклог (список задач, требований и функций, которые нужно выполнить для достижения целей проекта)", "kanban - канбан ( методология для управления задачами в IT-сфере)", "DevOps (Development Operations) - DevOps (методология взаимодействия разработчиков)",
    "CI/CD (Continuous Integration, Continuous Delivery) - непрерывная интеграция и доставка", "containerization - контейнеризация",
    "orchestration - оркестровка", "microservices - микросервисы",
    "serverless - безсерверный", "edge computing - вычисления на краю",
    "IoT (internet of things) - интернет вещей", "wearable - носимое устройство",
    "augmented reality - дополненная реальность",
    "virtual reality - виртуальная реальность"
]

ru_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
en_letters = 'abcdefghigkopqrstuvwxyz'

# Dictionary to track translation mode state for each user
translation_mode = {}

# Track the selected level for each user
user_levels = {}

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
    user_id = message.from_user.id
    user_levels[user_id] = message.text
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
    user_id = message.from_user.id
    user_level = user_levels.get(user_id)

    if user_level:
        words_map = {
            "A - Basic User": word_a1,
            "A1 - Beginner": word_a1,
            "A2 - Elementary": word_a2,
            "B - Independent User": word_b1,
            "B1 - Intermediate": word_b1,
            "B2 - Upper-Intermediate": word_b2,
            "C - Proficient User": word_c1,
            "C1 - Advanced": word_c1,
            "C2 - Proficiency": word_c2
        }

        words = words_map.get(user_level, [])
        words_text = "\n".join(words)
        await message.answer(text=f"Вот список слов для уровня {user_level}:\n\n{words_text}\n Завтра в 13.00 я пришлю тебе тест по словам)")
        
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
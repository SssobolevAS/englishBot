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

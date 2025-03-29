import sqlite3

def init_db():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            english_word TEXT NOT NULL,
            translation TEXT NOT NULL,
            level TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_words_to_db():
    words = [
        ('apple', 'яблоко', 'A1'),
        ('banana', 'банан', 'A1'),
        ('carrot', 'морковь', 'A2'),
        ('dog', 'собака', 'A2'),
        ('elephant', 'слон', 'B1'),
        ('computer', 'компьютер', 'B1'),
        ('programming', 'программирование', 'B2'),
        ('algorithm', 'алгоритм', 'B2'),
        ('database', 'база данных', 'C1'),
        ('optimization', 'оптимизация', 'C1')
    ]
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO words (english_word, translation, level) VALUES (?, ?, ?)', words)
    conn.commit()
    conn.close()

def get_words_by_level(level):
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute('SELECT english_word, translation FROM words WHERE level = ?', (level,))
    words = cursor.fetchall()
    conn.close()
    return words
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Список задач 📃'),
            KeyboardButton(text='Выполнение задачи ✅')
        ],
        [
            KeyboardButton(text='Статистика 📈'),
            KeyboardButton(text='Помогать Автором 🖤')
        ],
        [
            KeyboardButton(text='Помощь 📌'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='выберите элемент ниже'
)

main = main_kb

from aiogram import Router, F
from aiogram.types import Message
from app.keybords import main

router = Router()
task_lists = {}

@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer("""
    👋 Добро пожаловать в @MyTasksManager_bot!

✨ Мы рады приветствовать вас здесь. @MyTasksManager_bot - это ваш дружелюбный и универсальный бот-спутник, созданный, чтобы сделать ваш опыт в Telegram еще лучше. Будь то организация задач, получение информации, развлечения или просто общение, у нас есть все необходимое!

🚀 Основные функции:

✅ Управление задачами: Создавайте и управляйте задачами с легкостью. 📅✏️


🤖 Открытый исходный код: @MyTasksManager_bot - это проект с открытым исходным кодом, и вы можете внести свой вклад в его развитие на GitHub. 🐙🛠️
https://github.com/Fxyexe/TaskTelgramBot

🎉 Начнем!
Для начала использования @MyTasksManager_bot просто введите /start или исследуйте наши команды, введя /help. Если у вас есть вопросы или нужна помощь, просто отправьте нам сообщение. Мы здесь, чтобы сделать ваш опыт в Telegram более приятным и удобным. Наслаждайтесь общением с @MyTasksManager_bot! 🎈🤖""", reply_markup=main)

@router.message(F.text == 'Список задач 📃')
async def cmd_taskList(message: Message):
    user_id = message.from_user.id
    if user_id in task_lists and task_lists[user_id]:
        tasks = "\n".join([f"✅ {task}" if done else f"❌ {task}" for task, done in task_lists[user_id]])
        await message.answer(f"Ваши задачи:\n{tasks}")
    else:
        await message.answer('Список задач пуст. Добавьте задачи с помощью команды /addItem')

@router.message(F.text.startswith('/createList '))
async def cmd_createList(message: Message):
    user_id = message.from_user.id
    list_name = message.text[len('/createList '):]
    if list_name:
        task_lists[user_id] = []
        await message.answer(f'Создан список задач "{list_name}"')
    else:
        await message.answer('Пожалуйста, укажите название списка. Пример: `/createList Мой список`')

@router.message(F.text.startswith('/addItem '))
async def cmd_addItem(message: Message):
    user_id = message.from_user.id
    parts = message.text[len('/addItem '):].split('-')
    if len(parts) == 2 and parts[0].strip() and parts[1].strip():
        if user_id in task_lists:
            task_lists[user_id].append((parts[0].strip(), False))
            await message.answer(f'Задача "{parts[0].strip()}" добавлена в список "{parts[1].strip()}"')
        else:
            await message.answer('У вас нет созданных списков. Создайте список с помощью команды /createList')
    else:
        await message.answer('Пожалуйста, используйте формат `/addItem Задача - Список`. Пример: `/addItem Покупки - Мой список`')

@router.message(F.text == '/viewLists')
async def cmd_viewLists(message: Message):
    user_id = message.from_user.id
    if user_id in task_lists and task_lists[user_id]:
        lists = "\n".join([f"📃 {list_name}" for list_name, _ in task_lists[user_id]])
        await message.answer(f"Ваши списки задач:\n{lists}")
    else:
        await message.answer('У вас нет созданных списков. Создайте список с помощью команды /createList')

@router.message(F.text.startswith('/viewItems '))
async def cmd_viewItems(message: Message):
    user_id = message.from_user.id
    list_name = message.text[len('/viewItems '):]
    if user_id in task_lists:
        tasks = [(task, done) for task, done in task_lists[user_id] if list_name == task]
        if tasks:
            tasks_text = "\n".join([f"✅ {task}" if done else f"❌ {task}" for task, done in tasks])
            await message.answer(f'Задачи в списке "{list_name}":\n{tasks_text}')
        else:
            await message.answer(f'Список задач "{list_name}" пуст или не существует.')
    else:
        await message.answer('У вас нет созданных списков. Создайте список с помощью команды /createList')


@router.message(F.text.startswith('/done '))
async def cmd_done(message: Message):
    user_id = message.from_user.id
    task_name = message.text[len('/done '):]
    if user_id in task_lists:
        for idx, (task, done) in enumerate(task_lists[user_id]):
            if task_name == task:
                task_lists[user_id][idx] = (task, True)
                await message.answer(f'Задача "{task}" в списке помечена как выполненная.')
                return
        await message.answer(f'Задача "{task_name}" не найдена в ваших списках.')
    else:
        await message.answer('У вас нет созданных списков. Создайте список с помощью команды /createList')

@router.message(F.text.startswith('/removeItem '))
async def cmd_removeItem(message: Message):
    user_id = message.from_user.id
    parts = message.text[len('/removeItem '):].split('-')
    if len(parts) == 2 and parts[0].strip() and parts[1].strip():
        if user_id in task_lists:
            list_name = parts[1].strip()
            task_name = parts[0].strip()
            tasks = task_lists[user_id]

            if any(task_name == task for task, _ in tasks):
                task_lists[user_id] = [(task, done) for task, done in tasks if task != task_name]
                await message.answer(f'Задача "{task_name}" удалена из списка "{list_name}"')
            else:
                await message.answer(f'Задача "{task_name}" не найдена в списке "{list_name}" или список не существует.')
        else:
            await message.answer('У вас нет созданных списков. Создайте список с помощью команды /createList')

@router.message((F.text == '/help') | (F.text == 'Помощь 📌'))

async def cmd_help(message: Message):
    help_text = """
📋 Бот для списков 🤖

Привет! Я твой дружелюбный Бот для списков, здесь, чтобы помочь тебе управлять своими списками и задачами с ноткой веселья. 😄

Вот, что я могу сделать для тебя:

📝 **Создать список**: Просто отправь мне сообщение вида:
   `/createList Мой список покупок`

✏️ **Добавить элементы**: Добавь элементы в свой список с помощью:
   `/addItem Мой список покупок - Молоко, Яйца, Хлеб`

📑 **Посмотреть списки**: Посмотреть все свои списки можно командой:
   `/viewLists`

📄 **Посмотреть элементы**: Проверить элементы в списке:
   `/viewItems Мой список покупок`

✅ **Пометить как выполнено**: Когда задача выполнена, отметь её как выполненную:
   `/done Мой список покупок - Яйца`

❌ **Удалить элементы**: Удали элементы из своего списка:
   `/removeItem Мой список покупок - Хлеб`

🗑️ **Удалить список**: Удали список, когда ты закончишь с ним:
   `/deleteList Мой список покупок`

Нужна помощь с какой-то из этих команд? Просто напиши `/help` в любой момент, и я помогу тебе разобраться.

Давайте вместе организуемся! 😊
"""
    await message.answer(help_text)

@router.message((F.text == '/completed_tasks') | (F.text == 'Выполнение задачи ✅'))
async def cmd_completed_tasks(message: Message):
    user_id = message.from_user.id
    if user_id in task_lists and task_lists[user_id]:
        completed_task_list = [task for task, done in task_lists[user_id] if done]

        if completed_task_list:
            completed_tasks_text = "\n".join([f"✅ {task}" for task in completed_task_list])
            await message.answer(f'Выполненные задачи:\n{completed_tasks_text}')
        else:
            await message.answer('У вас нет выполненных задач.')
    else:
        await message.answer('У вас нет созданных списков задач.')


@router.message((F.text == '/statistics') | (F.text == 'Статистика 📈'))
async def cmd_statistics(message: Message):
    user_id = message.from_user.id
    if user_id in task_lists and task_lists[user_id]:
        total_tasks = len(task_lists[user_id])
        completed_tasks = sum(1 for _, done in task_lists[user_id] if done)
        incomplete_tasks = total_tasks - completed_tasks

        statistics_text = f"Статистика задач:\n" \
                          f"Всего задач: {total_tasks}\n" \
                          f"Выполнено: {completed_tasks}\n" \
                          f"Осталось: {incomplete_tasks}"

        await message.answer(statistics_text)
    else:
        await message.answer('У вас нет задач для отображения статистики.')


@router.message(lambda message: not message.text.startswith('/'))
async def cmd_invalid(message: Message):
    await message.answer('Команда недействительна. Для просмотра доступных команд напишите /help.')

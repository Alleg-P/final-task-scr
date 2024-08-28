
from telebot import TeleBot
from telebot.types import Message
from dotenv import load_dotenv
import os

load_dotenv(".env")
TG_TOKEN = os.getenv("TG_TOKEN")

bot = TeleBot(TG_TOKEN)

# Хранилище данных пользователей
tasks: list[list[str]] = []


@bot.message_handler(commands=['start', 'help'])
def sed_welcome(message: Message) -> None:
    """Отправляет приветственное сообщение и помощь по использованию бота."""
    welcome_text = """
    Привет! Я бот для управления задачами. Вот как со мной работать:
    - Чтобы добавить задачу, отправьте в  одном сообщении /add_task Название. Описание.
    - Чтобы посмотреть ваши задачи, отправьте /show_tasks
    - Чтобы удалить задачу, отправьте в  одном сообщении /delete_task Номер задачи.
    - Чтобы очистить список задач, отправьте /clear_tasks
    - Чтобы посмотреть эту памятку снова, отправьте /help
    """
    user_id: int = message.chat.id
    bot.send_message(user_id, welcome_text)


@bot.message_handler(commands=['add_task'])
def add_task(message: Message) -> None:
    """Обрабатывает команду /add_task."""
    user_id: int = message.chat.id
    text: str = message.text[9:].strip()  # Берём слайс после '/add_task'

    if not text:
        bot.send_message(user_id, text, "Вы не указали задачу. Памятка - /help")
        return

    task_parts = text.split('.')
    tasks.append(task_parts)


@bot.message_handler(commands=['show_tasks'])
def show_tasks(message: Message) -> None:
    """Выводит все текущие задачи пользователя."""
    user_id: int = message.chat.id

    message_text = "Ваши задачи:\n"
    for i, task in enumerate(tasks, start=1):
        message_text += f"{i}. {task[0]} - {task[1]}\n"

    bot.send_message(user_id, message_text)


@bot.message_handler(commands=['delete_task'])
def delete_task(message: Message) -> None:
    """Обрабатывает команду /delete_task для удаления задачи."""
    user_id: int = message.chat.id
    task_index = int(message.text.split()[1]) - 1

    if len(tasks) > task_index >= 0:
        del tasks[task_index]
        bot.send_message(user_id, "Задача успешно удалена.")
    else:
        bot.send_message(user_id, "Задачи с таким номером не существует. Проверьте список командой /show_tasks")


@bot.message_handler(commands=['clear_tasks'])
def clear_tasks(message: Message) -> None:
    """Обрабатывает команду /clear_tasks для очистки списка задач."""
    user_id: int = message.chat.id
    tasks.clear()
    bot.send_message(user_id, "Список задач очищен.")


if __name__ == "__main__":
    bot.infinity_polling()

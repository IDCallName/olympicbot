import os
import telegram
import telegram.ext
import psycopg2
import threading
import random
from time import sleep

## Токен
BOT_TOKEN = os.environ.get('BOT_TOKEN')

## Константы с номерами тем разговора
STATE_QUESTION = 0
STATE_ANSWER = 1

## Всякая фигня
updater = telegram.ext.Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

## Подключение к БД
#DATABASE = psycopg2.connect(dbname='dc9mv72g5rq199', user='expfuoggsoeeqp', password='', host='ec2-54-220-170-192.eu-west-1.compute.amazonaws.com')
#CURSOR = DATABASE.cursor()

# Команды
from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

# Команды
def cmd_start(update, context):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Выбрать уровень", callback_data="settings_level")], [InlineKeyboardButton("Выбрать класс", callback_data="settings_grade")]])
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я олимпиадный бот! ", reply_markup=markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите /go для получения задания")

# Диалог
def msg_question(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Текст задания. Введите /stop чтобы прекратить решать задания")
    
    return STATE_ANSWER

def msg_answer(update, context):
    if(update.effective_message.text == "/stop"):
        cmd_start(update, context)
    else:
        right_answer = 'a'
        
        if(update.effective_message.text == right_answer):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Правильный ответ")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Неверно! Правильный вариант: "+right_answer)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Текст задания. Введите /stop чтобы прекратить решать задания")

        return STATE_ANSWER

# Кнопки
def inline_function(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.callback_query)
    
## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import InlineQueryHandler
from telegram.ext import filters

start_handler = CommandHandler('start', cmd_start)
conversation_handler = ConversationHandler(
    entry_points = [CommandHandler('go', msg_question)],
    
    states = {
        STATE_QUESTION: [MessageHandler(filters.Filters.text, msg_question)],
        STATE_ANSWER: [MessageHandler(filters.Filters.text, msg_answer)],
    },

    fallbacks = []
)
inline_handler = InlineQueryHandler(inline_function)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)
dispatcher.add_handler(conversation_handler)
dispatcher.add_handler(inline_handler)

## Запускаем бота
updater.start_polling()

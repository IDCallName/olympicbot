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

def cmd_start(update, context):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Выбрать уровень", callback_data="settings_level")], [InlineKeyboardButton("Выбрать класс", callback_data="settings_grade")]])
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я олимпиадный бот! ", reply_markup=markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите /go для получения задания", reply_markup=markup)

def cmd_stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы вышли. Введите /go для получения новых заданий", reply_markup=markup)
    
# Когда привет
def msg_question(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Текст задания. Введите /stop чтобы прекратить решать задания")
    
    return STATE_ANSWER

# Ответы на вопрос об эрмитаже
def msg_answer(update, context):
    right_answer = 'a'
    if(update.effective_message.text == right_answer):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Правильный ответ")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверно! Правильный вариант: "+right_answer)
    
    return STATE_QUESTION

## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

start_handler = CommandHandler('start', cmd_start)
conversation_handler = ConversationHandler(
    entry_points = [CommandHandler('go', msg_question],
    
    states = {
        STATE_QUESTION: [MessageHandler(filters.Filters.text, msg_question)],
        STATE_ANSWER: [MessageHandler(filters.Filters.text, msg_answer)],
    },

    fallbacks = [CommandHandler('stop', cmd_start)]
)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)
dispatcher.add_handler(conversation_handler)

## Запускаем бота
updater.start_polling()

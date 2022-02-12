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
ERMITAZH_REPLY, ARAMZAS_REPLY = range(2)

## Всякая фигня
updater = telegram.ext.Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

## Подключение к БД
DATABASE = psycopg2.connect(dbname='dc9mv72g5rq199', user='expfuoggsoeeqp', password='8be9b873d53b0b38ba8fb3b7a0274db21e934813af12ecf4ed0bdee244422707', host='ec2-54-220-170-192.eu-west-1.compute.amazonaws.com')
CURSOR = DATABASE.cursor()

# Создать чайный гриб
from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

def cmd_start(update, context):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Выбрать уровень", callback_data="settings_level")]])
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я олимпиадный бот!", reply_markup=markup)

# Когда привет
def msg_greetings(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ф")
    context.bot.send_message(chat_id=update.effective_chat.id, text="б")
    
    return ERMITAZH_REPLY

# Ответы на вопрос об эрмитаже
def msg_ermitazh_reply(update, context):
    if(update.effective_message.text == "Да"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="а")
        return ConversationHandler.END
    elif(update.effective_message.text == "Нет"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="б")
        return ARAMZAS_REPLY
    
# Ответы на вопрос о арамзамзам
def msg_aramzas_reply(update, context):
    if(update.effective_message.text == "Да"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="а")
        return ConversationHandler.END
    elif(update.effective_message.text == "Нет"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="б")
        return ConversationHandler.END


## Устанавливаем какие-то держатели
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters

start_handler = CommandHandler('start', cmd_start)
conversation_handler = ConversationHandler(
    entry_points = [MessageHandler(filters.Filters.regex('^(Привет)$'), msg_greetings)],
    
    states = {
        ERMITAZH_REPLY: [MessageHandler(filters.Filters.regex('^(Да|Нет)$'), msg_ermitazh_reply)],
        ARAMZAS_REPLY: [MessageHandler(filters.Filters.regex('^(Да|Нет)$'), msg_aramzas_reply)]
    },

    fallbacks = []
)

# Устанавливаем какие-то держатели окончательно
dispatcher.add_handler(start_handler)
dispatcher.add_handler(conversation_handler)

## Запускаем бота
updater.start_polling()

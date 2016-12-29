# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

from commands import *
from commands.decorators import commands, descriptions
from settings import *

import random, logging

updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

@run_async
def start(bot, update):
    reply_keyboard = [['/aide', "/{0}".format(random.choice(list(commands))), "/{0}".format(random.choice(list(commands)))]]
    update.message.reply_text('Bonjour, Je suis Laurence. \n\n Par ou commencer ?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    # return commands_handler

@run_async
def commands_handler(bot, update):
    try:
        commande = update.message.text.split(' ')
        commande = commande[0]

        if commande.startswith("/"):
            commande = commande[1:]

        attrs = {"user_name": update.message.from_user, "text": [update.message.text]}

        if commande in commands:
            retour = commands[commande](attrs)
            if retour != "" and retour is not None:
                #bot.sendMessage(chat_id=update.message.chat_id, text=retour)
                update.message.reply_text(retour, reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_text("Désolé, je ne comprend pas encore votre demande… La liste des commandes est disponible via /aide", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        print (e)
        pass

def unknown_handler(bot, update):
    update.message.reply_text("Désolé, je ne comprend pas encore votre demande… La liste des commandes est disponible via /aide", reply_markup=ReplyKeyboardRemove())

def register_slash_commands():
    for command in commands:
        dispatcher.add_handler(CommandHandler(command, commands_handler))

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


dispatcher.add_handler(CommandHandler('start', start))
register_slash_commands()

# Gestion des /command inconnue
unknown_handler = MessageHandler(Filters.command, commands_handler)
dispatcher.add_handler(unknown_handler)

# Gestion du text comme commande
# echo_handler = MessageHandler(Filters.text, commands_handler)
# dispatcher.add_handler(echo_handler)

# log all errors
dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()

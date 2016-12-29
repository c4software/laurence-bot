# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from commands import *
from commands.decorators import commands, descriptions
from settings import *

import random, logging, os, sys

# Set up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.getenv('LAURENCE_TOKEN')
if not token:
    logging.critical('Token absent')
    sys.exit()

updater = Updater(token=token)
dispatcher = updater.dispatcher

@run_async
def start(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id,
    text="Bonjour, Je suis Laurence. Pour avoir la liste des commandes tapez /aide")
    #reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

@run_async
def commands_handler(bot, update, args):
    try:
        commande = update.message.text.split(' ')
        commande = commande[0]

        if commande.startswith("/"):
            commande = commande[1:]

        attrs = {"user_name": [update.message.from_user.username], "text": [update.message.text]}

        if commande in commands:
            bot.sendChatAction(chat_id=update.message.chat_id, action="typing")
            retour = commands[commande](attrs)
            if retour != "" and retour is not None:
                bot.sendMessage(chat_id=update.message.chat_id, text=retour, reply_markup=ReplyKeyboardRemove())#, parse_mode="Markdown")
                # update.message.reply_text(retour, reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_text("Désolé, je ne comprend pas encore votre demande… La liste des commandes est disponible via /aide", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        print (e)
        pass

def unknown_handler(bot, update):
    update.message.reply_text("Désolé, je ne comprend pas encore votre demande… La liste des commandes est disponible via /aide", reply_markup=ReplyKeyboardRemove())

def register_slash_commands():
    for command in commands:
        dispatcher.add_handler(CommandHandler(command, commands_handler, pass_args=True))

def help_slash_handler(bot, update):
    command_list = "\n"
    for group in descriptions:
        for command in descriptions[group]:
            command_list = command_list+"/{0} - {1} \n".format(command, descriptions[group][command])

    update.message.reply_text(command_list)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
dispatcher.add_handler(CommandHandler('help', help_slash_handler))

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

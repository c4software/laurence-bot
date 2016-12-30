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
def commands_handler(bot, update, args, no_fail_reply=False):
    try:
        commande = update.message.text.split(' ')
        commande = commande[0]

        if commande.startswith("/"):
            commande = commande[1:]

        # Suppression du nom du bot exemple /gif@laurence_le_bot
        if bot.name in commande:
            commande = commande.replace(bot.name, "").replace(" ", "")

        attrs = {"user_name": [update.message.from_user.username], "text": [update.message.text], "query": " ".join(args), "telegram": {"bot": bot, "update": update, "args": args}}

        if commande in commands:
            if no_fail_reply == False:
                # Si pas de réponse en cas d’erreur, on indique jamais que laurence écrit
                bot.sendChatAction(chat_id=update.message.chat_id, action="typing")

            # Execution de la commande en question
            retour = commands[commande](attrs)

            # Réponse
            if retour != "" and retour is not None:
                bot.sendMessage(chat_id=update.message.chat_id, text=retour, reply_markup=ReplyKeyboardRemove())#, parse_mode="Markdown")
                # update.message.reply_text(retour, reply_markup=ReplyKeyboardRemove())
        elif no_fail_reply == False:
            # Cas d’erreur uniquement si on est dans le cas ou l’on doit pas répondre en cas d’erreur
            update.message.reply_text("Désolé, je ne comprend pas encore votre demande… La liste des commandes est disponible via /aide", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        pass

@run_async
def text_handler(bot, update):
    # Temporaire fait fonctionner le bot en mode « texte » également.
    args = update.message.text.split(' ')
    commands_handler(bot, update, args[1:], no_fail_reply=True)

def unknown_handler(bot, update):
    update.message.reply_text("Désolé, je ne comprend pas encore votre demande… La liste des commandes est disponible via /aide", reply_markup=ReplyKeyboardRemove())

def register_slash_commands():
    for command in commands:
        dispatcher.add_handler(CommandHandler(command, commands_handler, pass_args=True))

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
register_slash_commands()

# Gestion des /command inconnue
# unknown_handler = MessageHandler(Filters.command, commands_handler)
# dispatcher.add_handler(unknown_handler)

# Gestion du text comme commande (Temporaire)
dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

# log all errors
dispatcher.add_error_handler(error)

print ("Laurence is ready.")

updater.start_polling()
# updater.idle()

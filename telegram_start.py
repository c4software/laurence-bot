# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from emoji import emojize, demojize

from commands import *
from commands.decorators import commands, descriptions
from commands.history import add_history, write_history, load_history
from settings import *

from tools.text import analyze_text
from tools.libs import *

from shared import save_data, clean_data

import random, logging, os, sys, atexit, threading

# Set up basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

token = os.getenv('LAURENCE_TOKEN')
if not token:
    logging.critical('Token absent')
    sys.exit()

updater = Updater(token=token)
dispatcher = updater.dispatcher

test = load_history()
@atexit.register
def final_handler():
    write_history()

@run_async
def start(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id,
    text="Bonjour, Je suis Laurence. Pour avoir la liste des commandes tapez /aide")

@run_async
def commands_handler(bot, update, args, no_fail_reply=False):
    try:
        get_debug_user_id(update.message.from_user)
        commande = get_probable_command(update.message.text, bot.name)
        attrs = make_attrs(update.message.from_user.username, update.message.text, args, update.message.chat.title, {"bot": bot, "update": update, "args": args})

        # Si c’est en mode « Salon », alors l’historique est enregistré
        # pour le salon sinon c’est pour le pseudo de l’utilisateur
        add_history(pseudo=username_or_channel(attrs), command="{0} {1}".format(commande, attrs["query"]))

        if commande in commands:
            if no_fail_reply == False:
                # Si pas de réponse en cas d’erreur, on indique jamais que laurence écrit
                bot.sendChatAction(chat_id=update.message.chat_id, action="typing")

            # Execution de la commande en question
            retour = commands[commande](attrs)

            # Réponse
            if retour != "" and retour is not None:
                if type(retour) is not str:
                    retour = " ".join(retour)

                retour = emojize(retour)
                bot.sendMessage(chat_id=update.message.chat_id, text=retour, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")
                # update.message.reply_text(retour, reply_markup=ReplyKeyboardRemove())
        elif no_fail_reply == False:
            # Cas d’erreur uniquement si on est dans le cas ou l’on doit pas répondre en cas d’erreur
            update.message.reply_text("Désolé, je ne comprend pas encore votre demande… La liste des commandes est disponible via /aide", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        import traceback
        traceback.print_exc()

@run_async
def text_handler(bot, update):
    get_debug_user_id(update.message.from_user)
    update.message.text = update.message.text.replace(bot.name, "").lstrip()
    commande = get_probable_command(update.message.text)
    if commande not in commands:
        bot, update, args, no_fail_reply = analyze_text(bot, update, do_google_search=is_private_channel(update))
        if bot:
            commands_handler(bot, update, args, no_fail_reply)
    else:
        args = update.message.text.split(" ")
        commands_handler(bot, update, args[1:], False)

@run_async
def location_handler(bot, update):
    args = update.message.text.split(' ')
    update.message.text = "/proche"
    commands_handler(bot, update, args[1:], no_fail_reply=True)

@run_async
def voice_handler(bot, update):
    update.message.reply_text(emojize("Très jolie voix ! Mais je ne comprend pas encore la parole :cry:.", use_aliases=True), reply_markup=ReplyKeyboardRemove())

def unknown_handler(bot, update):
    update.message.reply_text("Désolé, je ne comprend pas encore votre demande… La liste des commandes est disponible via /aide", reply_markup=ReplyKeyboardRemove())

def register_slash_commands():
    for command in commands:
        dispatcher.add_handler(CommandHandler(command, commands_handler, pass_args=True))

def error(bot, update, error):
    logging.warn('Update "%s" caused error "%s"' % (update, error))

dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
register_slash_commands()

# Gestion des /command inconnue
# unknown_handler = MessageHandler(Filters.command, commands_handler)
# dispatcher.add_handler(unknown_handler)

# Gestion du text comme commande (Temporaire)
dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

# Gestion des envois type « position »
dispatcher.add_handler(MessageHandler(Filters.location, location_handler))

# Gestion des envois type « Voice »
dispatcher.add_handler(MessageHandler(Filters.voice, voice_handler))

# log all errors
dispatcher.add_error_handler(error)

print ("Laurence is ready.")

updater.start_polling()
# updater.idle()

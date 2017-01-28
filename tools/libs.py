from settings import DEBUG_USER
from commands.decorators import commands

from models.models import User
from database import db_session

import logging

def is_debug(username):
    return username in DEBUG_USER

def is_telegram(msg):
    return "telegram" in msg

def is_private_channel(update):
    return update.message.chat.type is "private"

def get_username(msg):
    return msg["user_name"][0]

def send_message_debug_users(bot, message=""):
    for user in DEBUG_USER:
        bot.sendMessage(chat_id=get_userid_from_username(user), text="DEBUG: {0}".format(message))

def username_or_channel(attrs):
    if attrs["channel"]:
        pseudo = "channel_{0}".format(attrs["channel"])
    else:
        pseudo = get_username(attrs)

    return pseudo

def get_probable_command(text, bot_name=None):
    commande = text.lower().split(' ')
    commande = commande[0]

    if commande.startswith("/"):
        commande = commande[1:]

    # Suppression du nom du bot exemple /gif@laurence
    if bot_name and bot_name in commande:
        commande = commande.replace(bot_name, "").replace(" ", "")

    if commande in commands:
        # Commande existante
        return commande.lower()
    else:
        # Commande non existante
        return None

def save_new_user(username, userid):
    try:
        user = User(userid, username)
        db_session.add(user)
        db_session.commit()
    except:
        logging.debug("Utilisateur déjà connu. On ignore")
        pass

def get_userid_from_username(username):
    user = User.query.filter_by(username=username).one()
    if user:
        return user.iduser
    else:
        return None

def make_attrs_from_telegram(update, bot, args):
    return make_attrs(update.message.from_user.username, update.message.text, args, update.message.chat.title, {"bot": bot, "update": update, "args": args})


def make_attrs(username, text, args, channel=None, telegram=None):
    attrs = {"user_name": [username], "text": [text], "channel": channel, "query": " ".join(args)}
    if telegram:
        attrs["telegram"] = telegram

    return attrs

def make_message(username, icon_url, fallback, pretext, title, title_link, text, color="#7CD197"):
    return {"username": username, "icon_url":icon_url, "attachments": [{"fallback": fallback, "pretext": pretext, "title": title, "title_link": title_link, "text": text, "color": color}]}

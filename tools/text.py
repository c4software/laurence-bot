# -*- coding: utf-8 -*-

from emoji import emojize, demojize
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from commands.decorators import commands

from settings import DEBUG_USER

import difflib
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer

from commands.history import save_last_tags

from commands.context import get_awaiting_response

from .libs import is_debug, send_message_debug_users, username_or_channel, make_attrs_from_telegram

from database import db_session
from models.models import Learning_command

tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

def add_alias(command, tags):
    learning_command = Learning_command(tags, command)
    db_session.add(learning_command)
    db_session.commit()

def find_closest(tags):
    tag_length = str(len(tags))
    match = []
    matcher = difflib.SequenceMatcher(None, tags, [])
    learning_commands = Learning_command.query.filter_by(part_number=tag_length).all()
    for lc in learning_commands:
        matcher.set_seq2(tuple([(x[0], x[1]) for x in lc.tags]))
        ratio = matcher.ratio()
        if ratio >= 0.5:
            match.append((ratio, lc.commande))

    return sorted(match)

def analyze_text(bot, update, do_google_search=False):
    text = demojize(update.message.text)

    # Analyse du texte en mode POS TAGGER
    blob = tb(text)
    text_keywords = [(x[0].lower(),x[1]) for x in blob.tags]

    # Création de l’objet qui gère un peu tout
    attrs = make_attrs_from_telegram(update, bot, {})
    username = username_or_channel(attrs)

    save_last_tags(username, text_keywords)

    closest = find_closest(text_keywords)
    send_message_debug_users(bot, closest)

    if closest:
        update.message.text = closest[0][1]
    else:
        # On regarde si dans le context actuel on a un message en attente
        awaiting_command = get_awaiting_response(username)
        if awaiting_command:
            # Il y avait une commande en attente alors on append celle-ci pour une l’executer
            update.message.text = "/{0} {1}".format(awaiting_command["commande"], update.message.text)
        elif do_google_search:
            # Rien ne match alors on fallback en mode « Recherche Google »
            update.message.text = "/google {0}".format(update.message.text)

    # Une fois les traitements sur le texte éffectué, on remet en place les infos pour la suite
    args = update.message.text.split(' ')
    text = demojize(update.message.text)

    if ":cry" in text or ":thumbs_down_sign:" in text:
        update.message.reply_text(emojize("Oh :pensive_face: Un soucis ?"), reply_markup=ReplyKeyboardRemove())
        update.message.text = "/giphy"
        return (bot, update, ["cute"], False)
    elif ":zzz:" in text or ":sleep" in text:
        update.message.text = random.choice(["/gif","/cute", "/chuck", "/random", "/top10"])
        return (bot, update, [], False)
    elif "kiss:" in text:
        update.message.reply_text(emojize(":kiss:"), reply_markup=ReplyKeyboardRemove())
    elif ":poop:" in text or ":shit:" in text:
        update.message.reply_text(emojize("Jolie :poop: !"), reply_markup=ReplyKeyboardRemove())
    elif ":thumbs_up_sign:" in text:
        update.message.reply_text(emojize("YEAH ! :thumbs_up_sign:"), reply_markup=ReplyKeyboardRemove())
    elif "_heart" in text:
        update.message.reply_text(emojize(":face_throwing_a_kiss:"), reply_markup=ReplyKeyboardRemove())
    else:
        return (bot, update, args[1:], True)

    return None, None, None, None

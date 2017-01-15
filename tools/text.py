# -*- coding: utf-8 -*-

from emoji import emojize, demojize
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from commands.decorators import commands

from settings import DEBUG_USER

import difflib
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer

from commands.history import save_last_tags

from .libs import is_debug

aliases = {}
tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())


def save_alias(command, tags):
    tag_length = len (tags)
    if tag_length not in aliases:
        aliases[tag_length] = []

    aliases[tag_length].append((tags, command))

def find_closest(tags):
    tag_length = len(tags)
    matcher = difflib.SequenceMatcher(None, tags, [])
    match = []
    if tag_length in aliases:
        for alias, command in aliases[tag_length]:
            matcher.set_seq2(alias)
            ratio = matcher.ratio()
            if ratio >= 0.5:
                match.append((ratio, command))
    return sorted(match)

def analyze_text(bot, update):
    args = update.message.text.split(' ')
    text = demojize(update.message.text)

    # Analyse du texte en mode POS TAGGER
    blob = tb(text)
    text_keywords = [(x[0].lower(),x[1]) for x in blob.tags]

    save_last_tags(update.message.from_user.username, text_keywords)

    closest = find_closest(text_keywords)
    if is_debug(update.message.from_user.username):
         update.message.reply_text(closest)

    if closest:
        update.message.text = closest[0][1]

    # if update.message.from_user.username in DEBUG_USER:
    #     update.message.reply_text ("Keywords: {0}".format(",".join(text_keywords)))
    #     update.message.reply_text (blob.tags)
    #     update.message.reply_text (blob.sentiment)
    #     #print (difflib.get_close_matches(args[0], commands))

    # logging.debug(text)
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

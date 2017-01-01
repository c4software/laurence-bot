# -*- coding: utf-8 -*-

from emoji import emojize, demojize
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

def analyze_text(bot, update):
    args = update.message.text.split(' ')
    text = demojize(update.message.text)

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

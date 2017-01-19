# -*- coding: utf-8 -*-

import json

from .decorators import register_as_command
from settings import HISTORY_PATH
from tools.libs import get_username

history = {}
last_text = {}

def add_history(pseudo, command):
    command = command.rstrip()
    if pseudo not in history:
        history[pseudo] = []

    if len(history[pseudo]) == 0 or history[pseudo][-1] != command:
        history[pseudo].append(command)

def remove_last_history(pseudo):
    if pseudo in history:
        return history[pseudo].pop()
    else:
        return None

def get_history(pseudo):
    return history.get(pseudo, [])

def get_last_tags(pseudo):
    return last_text.get(pseudo, [])

def save_last_tags(pseudo, tags):
    last_text[pseudo] = tags

def write_history():
    fp = open(HISTORY_PATH, 'w')
    json.dump(history, fp)
    fp.close()

def load_history():
    global history
    try:
        fp = open(HISTORY_PATH, 'r')
        history = json.load(fp)
        fp.close()
    except:
        history = {}

def user_or_channel_history(msg):
    if msg["channel"]:
        pseudo = "channel_{0}".format(msg["channel"])
    else:
        pseudo = get_username(msg)

    return pseudo

def get_last_message(msg):
    try:
        pseudo = user_or_channel_history(msg)
        remove_last_history(pseudo)

        return get_history(pseudo)[-1]
    except:
        return ""

@register_as_command("historique", "Affiche votre historique de message", "Global")
def cmd_show_history(msg):
    username = get_username(msg)
    if username in history:
        return "- "+"\n- ".join(history[username])
    else:
        return "Aucun historique"

# -*- coding: utf-8 -*-

import json

from .decorators import register_as_command
from settings import HISTORY_PATH

history = {}

def add_history(pseudo, command):
    if pseudo not in history:
        history[pseudo] = []

    if len(history[pseudo]) == 0 or history[pseudo][-1] != command:
        history[pseudo].append(command)

def write_history():
    with open(HISTORY_PATH, 'w') as fp:
        json.dump(history, fp)

def load_history():
    try:
        with open(HISTORY_PATH, 'r') as fp:
            history = json.load(fp)
    except:
        history = {}

@register_as_command("historique", "Affiche votre historique de message", "Interne")
def cmd_show_history(msg):
    username = msg["user_name"][0]
    if username in history:
        return "- "+"\n- ".join(history[username])
    else:
        return "Aucun historique"

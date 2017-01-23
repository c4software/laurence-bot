# -*- coding: utf-8 -*-

import json

from .decorators import register_as_command
from settings import HISTORY_PATH
from tools.libs import get_username, username_or_channel

history = {}
last_text = {}

def add_history(pseudo, command):
    '''
    Ajout un historique
    :param pseudo: Pseudo de l’utilisateur en question.
    :param command: Commande à ajouter à l’historique.
    '''
    
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
    # Gestion des tags pour l’apprentissage
    return last_text.get(pseudo, [])

def save_last_tags(pseudo, tags):
    # Gestion des tags pour l’apprentissage
    last_text[pseudo] = tags

def write_history():
    # Sauvegarde de l’historique sur disque
    fp = open(HISTORY_PATH, 'w')
    json.dump(history, fp)
    fp.close()

def load_history():
    # Chargement de l’historique dans la mémoire.
    global history
    try:
        fp = open(HISTORY_PATH, 'r')
        history = json.load(fp)
        fp.close()
    except:
        history = {}

def get_last_message(msg):
    # Récupération du dernier message dans l’historique. (Utilisé pour le context)
    try:
        pseudo = username_or_channel(msg)
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

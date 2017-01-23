# -*- coding: utf-8 -*-

from .decorators import register_as_command
from commands.history import get_history, get_last_tags
from settings import DEBUG_USER, LEARN_PATH
from emoji import emojize
from tools.text import add_alias, load_aliases, get_aliases
from tools.libs import is_telegram, is_debug, get_username
import json

# Module d’ajout d’une correspondance entre un texte et une commande.
# Sauvegarde les mot ainsi que les tags

def load_learn():
    try:
        fp = open(LEARN_PATH, 'r')
        aliases = json.load(fp)
        fp.close()
    except:
        aliases = {}
    load_aliases(aliases)

def write_learn():
    try:
        # Sauvegarde de l’historique sur disque
        fp = open(LEARN_PATH, 'w')
        json.dump(get_aliases(), fp)
        fp.close()
    except Exception as e:
        print (e)

@register_as_command("learn", "", "Interne")
def cmd_do_learn(msg):
    username = get_username(msg)
    add_alias(get_history(username)[-2], get_last_tags(username))

    if is_telegram(msg) and is_debug(username):
        return emojize("Correspondance ajoutée :thumbs_up_sign:")
    else:
        return emojize("Désolé le learn n’est pas disponible :unamused_face:")

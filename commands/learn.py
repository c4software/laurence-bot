# -*- coding: utf-8 -*-

from commands.libs.decorators import register_as_command
from commands.libs.history import get_history, get_last_tags
from settings import DEBUG_USER
from emoji import emojize
from tools.text import add_alias
from tools.libs import is_telegram, is_debug, get_username
import json

# Module d’ajout d’une correspondance entre un texte et une commande.

@register_as_command("learn", "", "Interne")
def cmd_do_learn(msg):
    """
        Commande permettant de sauvegarder une correspondance Texte -> Commande.
        :param msg["query"]: (Optionnel) Commande à associer au texte précédent.

        ---------
        Ex (Avec fourniture de commande) :
        Vous : Laurence ?
        Vous : /learn /echo Oui ?
        Bot: Correspondance ajoutée « ('laurence', 'NNP') » -> « /echo Oui ? »
        …
        Vous : Laurence ?
        Bot Oui ?

        ---------
        Ex (Avec fourniture de commande) :
        Vous /echo Oui ?
        Bot : Oui ?
        Vous : Laurence ?
        Vous : /learn
        Bot: Correspondance ajoutée « ('laurence', 'NNP') » -> « /echo Oui ? »
        …
        Vous : Laurence ?
        Bot Oui ?

    """
    username    = get_username(msg)
    if not msg["query"]:
        command = get_history(username)[-3]
    else:
        command = msg["query"]

    tags = get_last_tags(username)

    if not tags:
        return "Vous devez avoir précédement dit une phrase à ajouter"

    if is_telegram(msg) and is_debug(username):
        # Ajout de l’alias
        add_alias(command, tags)
        return emojize("Correspondance ajoutée « {0} » -> « {1} » :thumbs_up_sign:".format(tags, command))
    else:
        return emojize("Désolé le learn n’est pas disponible :unamused_face:")

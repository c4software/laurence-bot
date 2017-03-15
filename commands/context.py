# -*- coding: utf-8 -*-
from .decorators import register_as_command
from commands.history import get_last_message
from tools.libs import get_probable_command, get_username, is_private_channel
from commands.decorators import commands

# Liste des commandes en attente de réponse.
# Le tableau contiendra la liste des utilisateurs et la commande associé
# {"pseudo": {"commande": "commande", "data": {}}
awaiting = {}

# Gestion des commandes en cours de process
def mark_for_awaiting_response(username, action, data={}):
    """
    Mémorise une action en attente pour l’utilisateur
    Parameters:
      :param username: pseudo de l’utilisateur
      :param action: Action en attente
    """
    awaiting[username] = {"commande": action, "data": data}

def get_awaiting_response(username):
    """
    Récupération et suppression de la commande en attente
    Parameters:
      :param username: pseudo de l’utilisateur
    """
    return awaiting.pop(username, None)

# Commande pour rejouer la dernière commande
@register_as_command("plus", None, keywords=["encore"])
def cmd_more(msg):
    previous_text = get_last_message(msg)

    # Réécriture des args avec la nouvelle commande
    msg["args"]     = previous_text.split(' ')[1:]
    msg["query"]    = " ".join(msg["args"])

    if previous_text:
        commande = get_probable_command(previous_text)
        if commande in commands:
            return commands[commande](msg)
        else:
            return ""
    else:
        return ""

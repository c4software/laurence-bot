# -*- coding: utf-8 -*-
from .decorators import register_as_command
from .history import get_last_message
from tools.libs import get_probable_command, get_username, is_private_channel

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
